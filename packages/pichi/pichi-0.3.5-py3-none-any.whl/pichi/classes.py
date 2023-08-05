#!/usr/bin/env python
# -*- coding: utf-8 -*-
import datetime
import gzip
import ipaddress
import logging
import os
import io
import re
import socket
import struct
import time
from typing import Any, BinaryIO, List, Optional, Set, TextIO, Tuple, Union

from pichi.utils import bytes_to_hr
from pichi.bloom import BloomFilter

MAGIC_NUMBER = b'\xc8\xd3\xf7\x3d'
FILE_SEPARATOR = b'\x0c\x07\x00\x00'
FOOTER_SEPARATOR = b'a\x07\x00\x00'
PCAP_HEADER = b'\xd4\xc3\xb2\xa1\x02\x00\x04' + (b'\x00' * 13) + b'\x01\x00\x00\x00'


class PichiFileError(ValueError):
    """ Raise for a file format or value error """
    pass


class PichiFilterError(ValueError):
    """ Raise for improper filter values or variables """
    pass


class PichiIndexerBase(object):
    """
    Base class for all Pichi indexers, handling initialization
    """

    __slots__ = ['input_pcaps', 'mode', 'output_path', 'index_name', 'output_compressed', 'out_open']

    def __init__(
            self,
            input_pcaps: List[str],
            output_path: Optional[str] = None,
            index_name: Optional[str] = None,
            mode: str = 'combined',
            output_compressed: bool = False
    ) -> None:
        self.input_pcaps = input_pcaps
        self.mode = mode
        if self.mode == 'individual':
            if not output_path:
                self.output_path = './'
            else:
                self.output_path = output_path
        elif self.mode == 'combined':
            if not output_path:
                self.output_path = f'{os.path.basename(self.input_pcaps[0])}.pi'
            else:
                self.output_path = output_path
        else:
            raise ValueError('Pichi mode must be one of (`individual`, `combined`)!')
        if not index_name:
            self.index_name = os.path.basename(self.output_path)
        else:
            self.index_name = index_name
        self.output_compressed = output_compressed
        if output_compressed:
            self.out_open = gzip.open
            if self.mode == 'combined' and self.output_path[-3:] != '.gz':
                self.output_path += '.gz'
        else:
            self.out_open = open

    def index(self):
        raise NotImplementedError


class PichiFileIndexBase(object):
    """
    Base class for Pichi file index classes, which act as an abstraction layer and group PichiRecordRows together by
      their source file
    """

    __slots__ = ['header_length', 'source_file', 'compressed', 'store', '_fp', '_rows', '_version']

    def __init__(
            self,
            source_file: str,
            header_length: int = 0,
            store: bool = False,
            fp: Union[TextIO, BinaryIO, None] = None,
            version: Optional[int] = None
    ) -> None:
        self.header_length = header_length
        self.source_file = source_file
        if self.source_file[-3:] == '.gz':
            self.compressed = True
        else:
            self.compressed = False
        self.store = store
        self._fp = fp
        self._rows = []
        self._version = version

    def __iter__(self) -> 'PichiFileIndexBase':
        return self

    def __next__(self):
        raise NotImplementedError

    @property
    def rows(self) -> list:
        return self._rows


class PichiRecordRowBase(object):
    """
    Base class for Pichi record rows extracted from indexes.
    """

    __slots__ = ['source_file', 'start', 'stop', '_version']

    def __init__(
            self,
            source_file: str,
            start: int,
            stop: int,
            version: Optional[int] = None,
            **kwargs
    ) -> None:
        self.source_file = source_file
        self.start = start
        self.stop = stop
        self._version = version

    @property
    def bytes(self) -> int:
        return self.stop - self.start

    @property
    def bytes_hr(self) -> str:
        return bytes_to_hr(self.bytes)

    @classmethod
    def from_text(cls, *args) -> Optional['PichiRecordRowBase']:
        raise NotImplementedError

    @classmethod
    def from_binary(cls, *args) -> Optional['PichiRecordRowBase']:
        raise NotImplementedError


class PichiFilterBase(object):
    """
    Base class for Pichi filter objects
    """

    __slots__ = ['variable', 'comparator', 'value_raw', 'value']

    VALID_VARIABLES = [
        'host',
        'src_host',
        'dst_host',
        'port',
        'src_port',
        'dst_port',
        'eth_type',
        'l2_proto'
    ]

    def __init__(
            self,
            variable: str,
            comparator: str,
            value_raw: str,
            value: Any,
            **kwargs
    ) -> None:
        self.variable = variable
        self.comparator = comparator
        self.value_raw = value_raw
        self.value = value

    def __hash__(self) -> int:
        return hash(self.variable) ^ hash(self.comparator) ^ hash(self.value_raw) ^ \
               hash((self.__class__.__name__, self.variable, self.comparator, self.value_raw))

    @classmethod
    def from_filter_statement(cls, *args, **kwargs) -> 'PichiFilterBase':
        raise NotImplementedError

    def row_passes_filter(self, row: PichiRecordRowBase) -> bool:
        raise NotImplementedError


class PichiPysharkIndexer(PichiIndexerBase):
    """
    The very first attempt at a parser for the text version of Pichi indexes. Very slow. Dead dove, do not eat.
    """
    def index(self) -> None:
        import pyshark
        capture = pyshark.FileCapture(self.input_pcaps, keep_packets=False)
        if self.output_compressed:
            index = gzip.open(self.output_path, 'wb')
        else:
            index = open(self.output_path, 'wb')
        offset = 24
        packet_count = 0
        for packet in capture:
            end_pos = offset + int(packet.length) + 16
            srcport = 0
            dstport = 0
            if hasattr(packet.layers[2], 'srcport'):
                srcport = packet.layers[2].srcport
            if hasattr(packet.layers[2], 'dstport'):
                dstport = packet.layers[2].dstport
            if hasattr(packet.layers[1], 'proto') and packet.layers[1].proto:
                l3_proto = packet.layers[1].proto
            else:
                try:
                    l3_proto = socket.getprotobyname(packet.layers[2].layer_name)
                except OSError:
                    l3_proto = 65535
            timestamp = '{}{}'.format(packet.sniff_timestamp, str(packet_count).zfill(10))
            index_row = '{}|{}|{}|{}|{}|{}|{}|{}|{}|{}|{}\n'.format(
                timestamp,
                self.input_pcaps,
                offset,
                end_pos,
                packet.layers[0].type,
                l3_proto,
                packet.layers[1].src_host,
                srcport,
                packet.layers[1].dst_host,
                dstport,
                int(packet.length)
            )
            logging.debug(index_row)
            offset = end_pos
            index.write(bytes(index_row, 'utf8'))
            packet_count += 1
        index.close()
        capture.close()


class PichiTextIndexer(PichiIndexerBase):
    """
    Generate Pichi text indexes from source pcaps
    """
    def index(self) -> None:
        index = None
        logging.info('Format is set to text')
        if self.mode == 'combined':
            logging.info('Mode is set to combined')
            if self.output_compressed:
                index = gzip.open(self.output_path, 'wb')
            else:
                index = open(self.output_path, 'wb')
        packet_count = 0
        file_count = 0
        for input_pcap in self.input_pcaps:
            logging.info(f'Indexing `{input_pcap}` . . .')
            if input_pcap[-3:] == '.gz':
                capture = gzip.open(input_pcap, 'rb')
            else:
                capture = open(input_pcap, 'rb')
            file_count += 1
            if self.mode == 'individual':
                logging.info('Mode is set to individual')
                if self.output_compressed:
                    index = gzip.open(
                        f'{self.output_path}/{os.path.basename(self.input_pcaps[0])}.pi.gz',
                        'wb'
                    )
                else:
                    index = open(f'{self.output_path}/{os.path.basename(self.input_pcaps[0])}.pi', 'wb')
            capture.seek(24)
            while True:
                try:
                    index.write(str(struct.unpack('I', capture.read(4))[0]).encode())  # timestamp in seconds
                except struct.error:
                    break
                packet_count += 1
                index.write(b'.')
                index.write(str(struct.unpack('I', capture.read(4))[0]).encode())  # milliseconds
                index.write(f'|{input_pcap}|'.encode())  # filename
                index.write(str(capture.tell() - 8).encode())  # start pos
                index.write(b'|')
                length = struct.unpack('I', capture.read(4))[0]
                index.write(str(capture.tell() + 4 + length).encode())  # end pos
                index.write(b'|')
                capture.seek(16, 1)
                eth_type = struct.unpack('!H', capture.read(2))[0]  # 16
                index.write(str(eth_type).encode())  # EtherType
                index.write(b'|')
                if eth_type == 2048:  # IPv4
                    ihl = ((struct.unpack('B', capture.read(1))[0] ^ 64) - 5) * 4  # get IHL
                    capture.seek(8, 1)
                    l2_proto = struct.unpack('B', capture.read(1))[0]
                    index.write(str(l2_proto).encode())  # IP Proto
                    index.write(b'|')
                    capture.seek(2, 1)
                    index.write(socket.inet_ntoa(capture.read(4)).encode())  # Source IP Addr
                    index.write(b'|')
                    index.write(socket.inet_ntoa(capture.read(4)).encode())  # Dest IP Addr
                    index.write(b'|')
                    capture.seek(ihl, 1)
                    if l2_proto in (1, 58):  # ICMP/ICMPv6
                        index.write(b'0|0\n')
                        capture.seek(4, 1)
                    else:
                        index.write(str(struct.unpack('!H', capture.read(2))[0]).encode())  # Source Port
                        index.write(b'|')
                        index.write(str(struct.unpack('!H', capture.read(2))[0]).encode())  # Dest Port
                        index.write(b'\n')
                    capture.seek(length - (38 + ihl), 1)
                elif eth_type == 2054:  # ARP
                    capture.seek(14, 1)
                    index.write(b'|0|')
                    index.write(socket.inet_ntoa(capture.read(4)).encode())  # Source IP Addr
                    index.write(b'|')
                    index.write(socket.inet_ntoa(capture.read(4)).encode())  # Dest IP Addr
                    index.write(b'|0|0\n')
                    capture.seek(length - 36, 1)
                elif eth_type == 34525:  # IPv6
                    capture.seek(6, 1)
                    index.write(str(struct.unpack('B', capture.read(1))[0]).encode())  # IP Proto
                    index.write(b'|')
                    capture.seek(1, 1)
                    index.write(socket.inet_ntop(socket.AF_INET6, capture.read(16)).encode())  # Source IP Addr
                    index.write(b'|')
                    index.write(socket.inet_ntop(socket.AF_INET6, capture.read(16)).encode())  # Dest IP Addr
                    index.write(b'|')
                    index.write(str(struct.unpack('!H', capture.read(2))[0]).encode())  # Source Port
                    index.write(b'|')
                    index.write(str(struct.unpack('!H', capture.read(2))[0]).encode())  # Dest Port
                    index.write(b'\n')
                    capture.seek(length - 58, 1)
                else:
                    logging.warning(f'Encountered unknown EtherType: `{eth_type}`')
                    index.write(b'0|0|0|0|0\n')
                    capture.seek(length - 14, 1)
            capture.close()
            if self.mode == 'individual':
                index.close()
        if self.mode == 'combined':
            index.close()
        logging.info(f'Indexing completed: {file_count} file(s) with {packet_count} packets')


class PichiBinaryIndexer(PichiIndexerBase):
    """
    Generate Pichi binary indexes from source pcaps
    """
    """
    Binary format:

    b'\xc8\xd3\xf7\x3d' - Magic number (CRC32 of 'Zaedyus')
    1 byte - PiB version (2 for this version)
    1 byte - Length of header
    4 byte - index creation time
    n bytes - index filename
        b'\x0c\x07\x00\x00' -- separator, yields '1804' (epoch time of Thursday, January 1, 1970 12:30:04 AM)
        1 byte - Length of file header
        n bytes - source filename
            8 bytes - timestamp w/ ms
            8 bytes - start position
            8 bytes - end position
            2 bytes - EtherType
            1 byte - L2 Proto
            4-16 bytes - source address
            4-16 bytes - dest address
            2 bytes - source port
            2 bytes - dest port
    1 byte - input file count
    4 bytes - packet count for index
    """
    PIB_VERSION = 3

    __slots__ = ['write_bloom_filter']

    def __init__(
            self,
            write_bloom_filter: bool = False,
            **kwargs
    ) -> None:
        super().__init__(**kwargs)
        self.write_bloom_filter = write_bloom_filter

    def index(self) -> None:
        index = None
        logging.info('Format is set to binary')
        bloom_filename = None
        source_ip = None
        dest_ip = None
        bloom_set = set()
        if self.write_bloom_filter:
            if self.mode == 'individual':
                bloom_filename = f'{self.output_path}{os.path.basename(self.input_pcaps[0])}.bf'
            elif self.mode == 'combined':
                bloom_filename = f'{self.output_path}.bf'
        if self.mode == 'combined':
            logging.info('Mode is set to combined')
            index = self.out_open(self.output_path, 'wb')
            index.write(MAGIC_NUMBER)
            index.write(struct.pack('BB', self.PIB_VERSION, len(self.index_name) + 6))
            index.write(struct.pack('I', int(time.time())))
            index.write(self.index_name.encode())
        packet_count = 0
        file_count = 0
        for input_pcap in self.input_pcaps:
            logging.info(f'Indexing `{input_pcap}` . . .')
            if input_pcap[-3:] == '.gz':
                capture = gzip.open(input_pcap, 'rb')
            else:
                capture = open(input_pcap, 'rb')
            file_count += 1
            if self.mode == 'individual':
                logging.info('Mode is set to individual')
                if self.output_compressed:
                    index = gzip.open(
                        f'{self.output_path}/{os.path.basename(self.input_pcaps[0])}.pi.gz',
                        'wb'
                    )
                else:
                    index = open(f'{self.output_path}/{os.path.basename(self.input_pcaps[0])}.pi', 'wb')
                index.write(MAGIC_NUMBER)
                index.write(struct.pack('BB', self.PIB_VERSION, len(input_pcap) + 9))
                index.write(struct.pack('I', int(time.time())))
                index.write(f'{input_pcap}.pi'.encode())
            index.write(FILE_SEPARATOR)
            index.write(struct.pack('B', len(input_pcap) + 1))
            index.write(input_pcap.encode())
            capture.seek(24)
            while True:
                ts = capture.read(4)
                ms = capture.read(4)
                sp = struct.pack('Q', capture.tell() - 8)
                try:
                    length = struct.unpack('I', capture.read(4))[0]
                except struct.error:
                    break
                packet_count += 1
                index.write(ts)  # timestamp in seconds
                index.write(ms)  # milliseconds
                index.write(sp)  # start pos
                index.write(struct.pack('Q', capture.tell() + 4 + length))  # end pos
                capture.seek(16, 1)
                eth_type = capture.read(2)  # 16
                index.write(eth_type)  # EtherType
                if eth_type == b'\x08\x00':  # IPv4
                    ihl = ((struct.unpack('B', capture.read(1))[0] ^ 64) - 5) * 4  # get IHL
                    capture.seek(8, 1)
                    l2_proto = capture.read(1)
                    index.write(l2_proto)  # IP Proto
                    capture.seek(2, 1)
                    source_ip = capture.read(4)
                    dest_ip = capture.read(4)
                    index.write(source_ip)  # Source IP Addr
                    index.write(dest_ip)  # Dest IP Addr
                    capture.seek(ihl, 1)
                    if l2_proto in (b'\x01', b':'):  # ICMP/ICMPv6
                        index.write(b'\x00\x00\x00\x00')  # 0 as ports
                        capture.seek(4, 1)
                    else:
                        index.write(capture.read(2))  # Source Port
                        index.write(capture.read(2))  # Dest Port
                    capture.seek(length - (38 + ihl), 1)
                elif eth_type == b'\x08\x06':  # ARP
                    capture.seek(14, 1)
                    index.write(b'\x00')
                    source_ip = capture.read(4)
                    dest_ip = capture.read(4)
                    index.write(source_ip)  # Source IP Addr
                    index.write(dest_ip)  # Dest IP Addr
                    index.write(b'\x00\x00\x00\x00')  # 0 as ports
                    capture.seek(length - 36, 1)
                elif eth_type == b'\x86\xdd':  # IPv6
                    capture.seek(6, 1)
                    index.write(capture.read(1))  # IP Proto
                    capture.seek(1, 1)
                    source_ip = capture.read(16)
                    dest_ip = capture.read(16)
                    index.write(source_ip)  # Source IP Addr
                    index.write(dest_ip)  # Dest IP Addr
                    index.write(capture.read(2))  # Source Port
                    index.write(capture.read(2))  # Dest Port
                    capture.seek(length - 58, 1)
                else:
                    logging.warning(
                        f'Encountered unknown EtherType: `{str(struct.unpack("!H", eth_type)[0]).encode()}`'
                    )
                    index.write(b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00')  # 0 for remaining fields
                    capture.seek(length - 14, 1)
                if self.write_bloom_filter and source_ip and dest_ip:
                    bloom_set.add(source_ip)
                    bloom_set.add(dest_ip)
            capture.close()
            if self.mode == 'individual':
                index.write(FOOTER_SEPARATOR)
                index.write(struct.pack('BI', file_count, packet_count))
                index.close()
        if self.mode == 'combined':
            index.write(FOOTER_SEPARATOR)
            index.write(struct.pack('BI', file_count, packet_count))
            index.close()
        if self.write_bloom_filter:
            bloom_filter = BloomFilter.from_num_entries(num_entries=len(bloom_set))
            logging.debug(f'Added {len(bloom_set)} IP addresses to the bloom filter')
            bloom_filter.update(bloom_set)
            if logging.getLogger().isEnabledFor(logging.DEBUG):
                bloom_stats = bloom_filter.check_efficiency(bloom_set)
                logging.debug(bloom_stats)
            logging.info(f'Writing bloom filter to `{bloom_filename}`')
            bloom_filter.write(bloom_filename)
        logging.info(f'Indexing completed: {file_count} file(s) with {packet_count} packets')


class PichiParser(object):
    """
    Handle Pichi parsing and provide methods for accessing PichiFileIndex objects and PichiTextRecordRow objects.

    This class is also iterable, yielding a PichiFileTextIndex or PichiFileBinaryIndex for each source file from the
      index. If self.store is set to True, PichiFileIndex objects are appended to self.input_files for later access.

    The entire index can be loaded and parsed at once using the .parse_whole() function. This forces self.store to True.

    When an entire index has been parsed, self.completed_index is set to True.
    """

    __slots__ = ['index_file', 'format', 'compressed', '_fp', 'version', 'header_length', 'index_creation_time',
                 'index_name', 'input_file_count', 'packet_count', 'input_files', 'store', 'completed_index',
                 'load_to_memory', '_header_checked']

    SUPPORTED_VERSIONS = (2, 3,)

    def __init__(
            self,
            index_file: str,
            load_to_memory: bool = False,
            store: bool = False
    ) -> None:
        self.index_file = index_file
        self.format, self.compressed = self._get_type()
        self._fp = None
        self.version = None
        self.header_length = None
        self.index_creation_time = None
        self.index_name = None
        self.input_file_count = 0
        self.packet_count = 0
        self.input_files = []
        self.store = store
        self.load_to_memory = load_to_memory
        self.completed_index = False
        self._header_checked = False
        self._parse_header()

    def __iter__(self) -> 'PichiParser':
        return self

    def __next__(self) -> Union['PichiTextFileIndex', 'PichiBinaryFileIndex']:
        """
        Yield files from the index
        """
        if self.format == 'bin':
            sep_check = self._fp.read(4)
            if sep_check == FOOTER_SEPARATOR:
                self._fp.seek(-4, 1)
                raise StopIteration
            elif sep_check != FILE_SEPARATOR:
                raise PichiFileError(f'Bad separator, `{sep_check}`!')
            file_header_length = struct.unpack('B', self._fp.read(1))[0]
            input_file = PichiBinaryFileIndex(
                header_length=file_header_length,
                source_file=self._fp.read(file_header_length - 1).decode(),
                store=self.store,
                fp=self._fp,
                version=self.version
            )
            if self.store:
                self.input_files.append(input_file)
            return input_file
        elif self.format == 'text':
            # do something magic here where we return rows instead of files, maybe? idk
            pre_line_tell = self._fp.tell()
            index_line = self._fp.readline()
            if index_line == '':
                raise StopIteration
            row_obj = PichiTextRecordRow.from_text(index_line)
            self._fp.seek(pre_line_tell)
            return PichiTextFileIndex(source_file=row_obj.source_file, fp=self._fp)
        else:
            logging.exception('I didn\'t put those in my bag?')

    def _parse_header(self) -> None:
        if self._header_checked:
            pass
        self._fp = self._cond_open()
        if self.format == 'bin':
            if self._fp.read(4) != MAGIC_NUMBER:
                raise PichiFileError('Bad magic number!')
            version = struct.unpack('B', self._fp.read(1))[0]
            if version not in self.SUPPORTED_VERSIONS:
                raise PichiFileError(f'Unsupported format version, `{version}`!')
            self.version = version
            self.header_length = struct.unpack('B', self._fp.read(1))[0]
            self.index_creation_time = datetime.datetime.utcfromtimestamp(struct.unpack('I', self._fp.read(4))[0])
            if self.header_length > 6:
                self.index_name = self._fp.read(self.header_length - 6).decode()
        if not self.index_name:
            self.index_name = self.index_file
        self._header_checked = True

    def _parse_footer(self) -> None:
        if self.completed_index:
            pass
        if self.format == 'bin':
            sep_check = self._fp.read(4)
            if sep_check == FOOTER_SEPARATOR:
                self.input_file_count = struct.unpack('B', self._fp.read(1))[0]
                self.packet_count = struct.unpack('I', self._fp.read(4))[0]
            else:
                raise PichiFileError(f'Bad footer separator `{sep_check}`!')
        self.completed_index = True

    def _get_type(self) -> Tuple[str, bool]:
        index_fp = open(self.index_file, 'rb')
        if index_fp.read(2) == b'\x1f\x8b':  # Gzip magic number
            compressed = True
        else:
            compressed = False
        index_fp.close()
        if compressed:
            index_fp = gzip.open(self.index_file, 'rb')
        else:
            index_fp = open(self.index_file, 'rb')
        if index_fp.read(4) == MAGIC_NUMBER:
            index_format = 'bin'
        else:
            index_format = 'text'
        index_fp.close()
        return index_format, compressed

    def _cond_open(self) -> Union[BinaryIO, TextIO]:
        if self.load_to_memory:
            logging.info('Loading index file to memory')
            if self.compressed:
                if self.format == 'bin':
                    with gzip.open(self.index_file, 'rb') as dfp:
                        fp = io.BytesIO(dfp.read())
                elif self.format == 'text':
                    with gzip.open(self.index_file, 'r') as dfp:
                        fp = io.StringIO(dfp.read())
                else:
                    raise PichiFileError
            else:
                if self.format == 'bin':
                    with open(self.index_file, 'rb') as dfp:
                        fp = io.BytesIO(dfp.read())
                elif self.format == 'text':
                    with open(self.index_file, 'r') as dfp:
                        fp = io.StringIO(dfp.read())
                else:
                    raise PichiFileError
        else:
            if self.compressed:
                if self.format == 'bin':
                    fp = gzip.open(self.index_file, 'rb')
                elif self.format == 'text':
                    fp = gzip.open(self.index_file, 'r')
                else:
                    raise PichiFileError
            else:
                if self.format == 'bin':
                    fp = open(self.index_file, 'rb')
                elif self.format == 'text':
                    fp = open(self.index_file, 'r')
                else:
                    raise PichiFileError
        return fp

    def parse_whole(self) -> None:
        self._parse_header()
        logging.info(f'Parsing index `{self.index_name}`')
        packet_count = 0
        for input_file in self:
            logging.info(f'Found file `{input_file.source_file}`')
            for input_row in input_file:
                packet_count += 1
        self._parse_footer()
        assert packet_count == self.packet_count
        logging.info(f'Found {self.packet_count} packets')


class PichiBinaryFileIndex(PichiFileIndexBase):
    """
    An abstraction for splitting PichiRecordRows from binary indexes into their original source files.
    """

    def __next__(self) -> None:
        """
        Yield record from the file
        """
        sep_check = self._fp.read(4)
        self._fp.seek(-4, 1)
        if sep_check in (FILE_SEPARATOR, FOOTER_SEPARATOR):
            raise StopIteration
        if self._version == 2:
            self._fp.seek(16, 1)
            eth_type = self._fp.read(2)
            self._fp.seek(-18, 1)
            if eth_type == b'\x86\xdd':  # IPv6 EtherType
                index_row = self._fp.read(55)
                if len(index_row) != 55:
                    raise PichiFileError(f'Malformed index row: `{index_row}`!')
            else:
                index_row = self._fp.read(31)
                if len(index_row) != 31:
                    raise PichiFileError(f'Malformed index row: `{index_row}`!')
        elif self._version == 3:
            self._fp.seek(24, 1)
            eth_type = self._fp.read(2)
            self._fp.seek(-26, 1)
            if eth_type == b'\x86\xdd':  # IPv6 EtherType
                index_row = self._fp.read(63)
                if len(index_row) != 63:
                    raise PichiFileError(f'Malformed index row: `{index_row}`!')
            else:
                index_row = self._fp.read(39)
                if len(index_row) != 39:
                    raise PichiFileError(f'Malformed index row: `{index_row}`!')
        row_obj = PichiBinaryRecordRow.from_binary(index_row, self.source_file, self._version)
        if self.store:
            self._rows.append(row_obj)
        return row_obj

    def add_row(self, data: bytes, pcap: str) -> None:
        if len(data) not in (31, 55, 63):
            raise PichiFileError(f'Malformed index row: `{data}`!')
        self._rows.append(PichiBinaryRecordRow.from_binary(data, pcap, self._version))


class PichiTextFileIndex(PichiFileIndexBase):
    """
    An abstraction for splitting PichiRecordRows from text indexes into their original source files.
    """

    def __next__(self) -> 'PichiTextRecordRow':
        """
        Yield record from the file
        """
        pre_line_tell = self._fp.tell()
        index_line = self._fp.readline()
        if index_line == '':
            raise StopIteration
        row_obj = PichiTextRecordRow.from_text(index_line)
        if row_obj.source_file != self.source_file:
            self._fp.seek(pre_line_tell)
            raise StopIteration
        if self.store:
            self._rows.append(row_obj)
        return row_obj

    def add_row(self, data: str) -> None:
        self._rows.append(PichiTextRecordRow.from_text(data))


class PichiTextRecordRow(PichiRecordRowBase):
    """
    A single record entry from a Pichi index file.
    """

    __slots__ = ['timestamp', 'ms', 'eth_type', 'l2_proto', 'src_host', 'dst_host', 'src_port', 'dst_port']

    def __init__(
            self,
            timestamp: 'datetime.datetime',
            ms: int,
            eth_type: int,
            l2_proto: int,
            src_host: Union['ipaddress.IPv4Address', 'ipaddress.IPv6Address'],
            dst_host: Union['ipaddress.IPv4Address', 'ipaddress.IPv6Address'],
            src_port: int,
            dst_port: int,
            **kwargs
    ) -> None:
        super().__init__(**kwargs)
        self.timestamp = timestamp
        self.ms = ms
        self.eth_type = eth_type
        self.l2_proto = l2_proto
        self.src_host = src_host
        self.dst_host = dst_host
        self.src_port = src_port
        self.dst_port = dst_port

    @classmethod
    def from_text(cls, text: str) -> Optional['PichiTextRecordRow']:
        fields = text.split('|')
        try:
            values = {
                'timestamp': datetime.datetime.utcfromtimestamp(int(fields[0].split('.')[0])),
                'ms': int(fields[0].split('.')[1]),
                'source_file': fields[1],
                'start': int(fields[2]),
                'stop': int(fields[3]),
                'eth_type': int(fields[4]),
                'l2_proto': int(fields[5]),
                'src_host': ipaddress.ip_address(fields[6]),
                'dst_host': ipaddress.ip_address(fields[7]),
                'src_port': int(fields[8]),
                'dst_port': int(fields[9])
            }
        except ValueError:
            return None
        return cls(**values)

    @classmethod
    def from_binary(cls, data: bytes, pcap: str, version: int) -> Optional['PichiTextRecordRow']:
        try:
            if version == 2:
                init_data = {
                    'source_file': pcap,
                    'version': version,
                    'timestamp': datetime.datetime.utcfromtimestamp(struct.unpack('I', data[0:4])[0]),
                    'ms': struct.unpack('I', data[4:8])[0],
                    'start': struct.unpack('I', data[8:12])[0],
                    'stop': struct.unpack('I', data[12:16])[0],
                    'eth_type': struct.unpack('!H', data[16:18])[0],
                    'l2_proto': struct.unpack('B', data[18:19])[0]
                }
                if init_data['eth_type'] == 34525:  # IPv6 EtherType
                    init_data['src_host'] = ipaddress.IPv6Address(data[19:35])
                    init_data['dst_host'] = ipaddress.IPv6Address(data[35:51])
                    init_data['src_port'] = struct.unpack('!H', data[51:55])[0]
                    init_data['dst_port'] = struct.unpack('!H', data[55:57])[0]
                else:
                    init_data['src_host'] = ipaddress.IPv4Address(data[19:23])
                    init_data['dst_host'] = ipaddress.IPv4Address(data[23:27])
                    init_data['src_port'] = struct.unpack('!H', data[27:29])[0]
                    init_data['dst_port'] = struct.unpack('!H', data[29:31])[0]
            elif version == 3:
                init_data = {
                    'source_file': pcap,
                    'version': version,
                    'timestamp': datetime.datetime.utcfromtimestamp(struct.unpack('I', data[0:4])[0]),
                    'ms': struct.unpack('I', data[4:8])[0],
                    'start': struct.unpack('Q', data[8:16])[0],
                    'stop': struct.unpack('Q', data[16:24])[0],
                    'eth_type': struct.unpack('!H', data[24:26])[0],
                    'l2_proto': struct.unpack('B', data[26:27])[0]
                }
                if init_data['eth_type'] == 34525:  # IPv6 EtherType
                    init_data['src_host'] = ipaddress.IPv6Address(data[27:43])
                    init_data['dst_host'] = ipaddress.IPv6Address(data[43:59])
                    init_data['src_port'] = struct.unpack('!H', data[59:63])[0]
                    init_data['dst_port'] = struct.unpack('!H', data[63:65])[0]
                else:
                    init_data['src_host'] = ipaddress.IPv4Address(data[27:31])
                    init_data['dst_host'] = ipaddress.IPv4Address(data[31:35])
                    init_data['src_port'] = struct.unpack('!H', data[35:37])[0]
                    init_data['dst_port'] = struct.unpack('!H', data[37:39])[0]
            else:
                raise PichiFileError(f'Unsupported format version, `{version}`!')
        except struct.error:
            return None
        return cls(**init_data)


class PichiBinaryRecordRow(PichiRecordRowBase):
    """
    A single record entry from a Pichi index file.
    """

    __slots__ = ['timestamp', 'ms', 'eth_type', 'l2_proto', 'src_host', 'dst_host', 'src_port', 'dst_port', '_version']

    def __init__(
            self,
            timestamp: bytes,
            ms: bytes,
            eth_type: bytes,
            l2_proto: bytes,
            src_host: bytes,
            dst_host: bytes,
            src_port: bytes,
            dst_port: bytes,
            version: int,
            **kwargs
    ) -> None:
        super().__init__(**kwargs)
        self.timestamp = timestamp
        self.ms = ms
        self.eth_type = eth_type
        self.l2_proto = l2_proto
        self.src_host = src_host
        self.dst_host = dst_host
        self.src_port = src_port
        self.dst_port = dst_port
        self._version = version

    def __str__(self):
        ms_timestamp = datetime.datetime.utcfromtimestamp(
            float(str(struct.unpack('I', self.timestamp)[0]) + '.' + str(struct.unpack('I', self.ms)[0]))
        )
        return f"\033[33m{self.source_file} - " \
            f"{ms_timestamp} ({self.start} -> {self.stop})\033[35m [{struct.unpack('!H', self.eth_type)[0]}|" \
            f"{struct.unpack('B', self.l2_proto)[0]}]\033[0m \033[32m{socket.inet_ntoa(self.src_host)} : " \
            f"{struct.unpack('!H', self.src_port)[0]}\033[\0m -> \033[36m{socket.inet_ntoa(self.dst_host)} : " \
            f"{struct.unpack('!H', self.dst_port)[0]}\033[0m"

    @classmethod
    def from_text(cls, text: str) -> Optional['PichiBinaryRecordRow']:
        fields = text.split('|')
        try:
            values = {
                'timestamp': datetime.datetime.utcfromtimestamp(int(fields[0].split('.')[0])),
                'ms': int(fields[0].split('.')[1]),
                'source_file': fields[1],
                'start': int(fields[2]),
                'stop': int(fields[3]),
                'eth_type': int(fields[4]),
                'l2_proto': int(fields[5]),
                'src_host': ipaddress.ip_address(fields[6]),
                'dst_host': ipaddress.ip_address(fields[7]),
                'src_port': int(fields[8]),
                'dst_port': int(fields[9])
            }
        except ValueError:
            return None
        return cls(**values)

    @classmethod
    def from_binary(cls, data: bytes, pcap: str, version: int) -> Optional['PichiBinaryRecordRow']:
        try:
            if version == 2:
                init_data = {
                    'source_file': pcap,
                    'version': version,
                    'timestamp': data[0:4],
                    'ms': data[4:8],
                    'start': struct.unpack('I', data[8:12])[0],
                    'stop': struct.unpack('I', data[12:16])[0],
                    'eth_type': data[16:18],
                    'l2_proto': data[18:19]
                }
                if init_data['eth_type'] == b'\x86\xdd':  # IPv6 EtherType
                    init_data['src_host'] = data[19:35]
                    init_data['dst_host'] = data[35:51]
                    init_data['src_port'] = data[51:55]
                    init_data['dst_port'] = data[55:57]
                else:
                    init_data['src_host'] = data[19:23]
                    init_data['dst_host'] = data[23:27]
                    init_data['src_port'] = data[27:29]
                    init_data['dst_port'] = data[29:31]
            elif version == 3:
                init_data = {
                    'source_file': pcap,
                    'version': version,
                    'timestamp': data[0:4],
                    'ms': data[4:8],
                    'start': struct.unpack('Q', data[8:16])[0],
                    'stop': struct.unpack('Q', data[16:24])[0],
                    'eth_type': data[24:26],
                    'l2_proto': data[26:27]
                }
                if init_data['eth_type'] == b'\x86\xdd':  # IPv6 EtherType
                    init_data['src_host'] = data[27:43]
                    init_data['dst_host'] = data[43:59]
                    init_data['src_port'] = data[59:63]
                    init_data['dst_port'] = data[63:65]
                else:
                    init_data['src_host'] = data[27:31]
                    init_data['dst_host'] = data[31:35]
                    init_data['src_port'] = data[35:37]
                    init_data['dst_port'] = data[37:39]
            else:
                raise PichiFileError(f'Unsupported format version, `{version}`!')
        except struct.error:
            return None
        return cls(**init_data)


class PichiExtractor(object):
    """
    An abstracter for extracting files from source pcaps with the help of a Pichi index, with optional support for
      specifying a filter for records to be checked against.
    """

    __slots__ = ['input_index', 'input_prefix', 'fix_input_compressed', 'output_pcap', 'output_compressed', 'open_out',
                 'index_filter', 'filter_set', 'load_to_memory', 'parser']

    def __init__(
            self,
            input_index: str,
            input_prefix: Optional[str] = None,
            fix_input_compressed: bool = False,
            output_pcap: Optional[str] = None,
            output_compressed: bool = False,
            index_filter: str = None,
            load_to_memory: bool = False,
            filter_set: Optional['PichiFilterSet'] = None
    ) -> None:
        self.input_index = input_index
        self.input_prefix = input_prefix
        self.fix_input_compressed = fix_input_compressed
        if not output_pcap:
            self.output_pcap = input_index + '.pcap'
        else:
            self.output_pcap = output_pcap
        self.output_compressed = output_compressed
        if self.output_compressed:
            self.open_out = gzip.open
            if self.output_pcap[-3:] != '.gz':
                self.output_pcap += '.gz'
        else:
            self.open_out = open
        self.index_filter = index_filter
        self.load_to_memory = load_to_memory
        self.filter_set = filter_set
        self.parser = None

    def extract(self) -> int:
        self.parser = PichiParser(index_file=self.input_index, store=False, load_to_memory=self.load_to_memory)
        if self.index_filter and not self.filter_set:
            if self.parser.format == 'bin':
                self.filter_set = PichiFilterSet(filter_string=self.index_filter, binary_filters=True)
            elif self.parser.format == 'text':
                self.filter_set = PichiFilterSet(filter_string=self.index_filter, binary_filters=False)
        logging.info(f'Extracting packets from index `{self.parser.index_name}`')
        logging.info(f'Writing to `{self.output_pcap}`')
        file_number = 1
        packet_number = 0
        output_file = None
        for input_file in self.parser:
            if self.input_prefix:
                input_source = f'{self.input_prefix}/{input_file.source_file}'
            else:
                input_source = input_file.source_file
            if self.fix_input_compressed and input_source[-3:] != '.gz':
                input_source = f'{input_source}.gz'
                input_file.compressed = True
            logging.info(f'Extracting from file {file_number}: `{input_source}`')
            logging.info('Working . . .')
            if input_file.compressed:
                current_pcap_file = gzip.open(input_source, 'rb')
            else:
                current_pcap_file = open(input_source, 'rb')
            for record in input_file:
                if self.filter_set:
                    if not self.filter_set.test_filters(record):
                        continue
                if packet_number == 0:
                    output_file = self.open_out(self.output_pcap, 'wb')
                    output_file.write(PCAP_HEADER)
                current_pcap_file.seek(record.start)
                output_file.write(current_pcap_file.read(record.bytes))
                packet_number += 1
            if current_pcap_file:
                current_pcap_file.close()
            file_number += 1
        if output_file:
            output_file.close()
        logging.info(f'Extracted {packet_number} packets')
        return packet_number


class PichiTextFilter(PichiFilterBase):
    """
    A filter object that a PichiTextRecordRow can be checked against using the row_passes_filter(row) function.
    """

    @classmethod
    def from_filter_statement(cls, filter_statement: str) -> 'PichiTextFilter':
        filter_parts = re.match(r"([a-z_]*)([<>=!]=)([a-z0-9./]*)", filter_statement)
        try:
            filter_obj = {
                'variable': filter_parts.groups()[0],
                'comparator': filter_parts.groups()[1],
                'value_raw': filter_parts.groups()[2]
            }
        except AttributeError:
            raise PichiFilterError(f'Malformed filter statement, `{filter_statement}`')
        if filter_obj['variable'] not in cls.VALID_VARIABLES:
            raise PichiFilterError(f'Unknown variable `{filter_obj["variable"]}`')
        if filter_obj['variable'] in ['host', 'src_host', 'dst_host']:
            if '/' in filter_obj['value_raw']:
                if ':' in filter_obj['value_raw']:
                    filter_obj['value'] = ipaddress.IPv6Network(filter_obj['value_raw'])
                elif '.' in filter_obj['value_raw']:
                    filter_obj['value'] = ipaddress.IPv4Network(filter_obj['value_raw'])
                else:
                    raise PichiFilterError
            elif re.search(r"[a-zA-Z]", filter_obj['value_raw']):
                filter_obj['value'] = ipaddress.IPv4Address(socket.gethostbyname(filter_obj['value_raw']))
            else:
                if ':' in filter_obj['value_raw']:
                    filter_obj['value'] = ipaddress.IPv6Address(filter_obj['value_raw'])
                elif '.' in filter_obj['value_raw']:
                    filter_obj['value'] = ipaddress.IPv4Address(filter_obj['value_raw'])
        elif filter_obj['variable'] == 'l2_proto':
            try:
                filter_obj['value'] = int(filter_obj['value_raw'])
            except ValueError:
                filter_obj['value'] = socket.getprotobyname(filter_obj['value_raw'])
        elif filter_obj['variable'] in ['port', 'src_port', 'dst_port']:
            try:
                filter_obj['value'] = int(filter_obj['value_raw'])
            except ValueError:
                filter_obj['value'] = socket.getservbyname(filter_obj['value_raw'])
        else:
            filter_obj['value'] = int(filter_obj['value_raw'])
        return cls(**filter_obj)

    def row_passes_filter(self, row: PichiTextRecordRow) -> bool:
        left1 = None
        left2 = None
        left = None
        middle = self.comparator
        right = self.value
        eval_type = 'single'
        if isinstance(self.value, ipaddress.IPv4Network):
            if self.comparator == '==':
                middle = 'in'
            elif self.comparator == '!=':
                middle = 'not in'
            else:
                raise PichiFilterError
        if self.variable == 'host':
            left1 = row.src_host
            left2 = row.dst_host
            eval_type = 'both'
        elif self.variable == 'src_host':
            left = row.src_host
        elif self.variable == 'dst_host':
            left = row.dst_host
        elif self.variable == 'port':
            left1 = row.src_port
            left2 = row.dst_port
            eval_type = 'both'
        elif self.variable == 'src_port':
            left = row.src_port
        elif self.variable == 'dst_port':
            left = row.dst_port
        elif self.variable == 'eth_type':
            left = row.eth_type
        elif self.variable == 'l2_proto':
            left = row.l2_proto
        else:
            raise PichiFilterError
        if eval_type == 'both':
            return eval('left1 ' + middle + ' right or left2 ' + middle + ' right')
        else:
            return eval('left ' + middle + ' right')


class PichiBinaryFilter(PichiFilterBase):
    """
    A filter object that a PichiTextRecordRow can be checked against using the row_passes_filter(row) function.
    """

    __slots__ = ['network', 'shift']

    def __init__(
            self,
            network: bool,
            shift: Optional[int] = None,
            **kwargs
    ) -> None:
        super().__init__(**kwargs)
        self.network = network
        self.shift = shift

    @staticmethod
    def shift_v6(v6_addr: Union[bytes, str], shift: int) -> int:
        if isinstance(v6_addr, bytes):
            ints = struct.unpack('!QQ', v6_addr)
        elif isinstance(v6_addr, str):
            ints = struct.unpack('!QQ', socket.inet_pton(socket.AF_INET6, v6_addr))
        else:
            raise ValueError
        v6_dec = ints[1] + (ints[0] << 64)
        return v6_dec >> shift

    @classmethod
    def from_filter_statement(cls, filter_statement: str) -> 'PichiBinaryFilter':
        filter_parts = re.match(r"([a-z2_]*)([<>=!]=)([a-z0-9.:/]*)", filter_statement)
        try:
            filter_obj = {
                'variable': filter_parts.groups()[0],
                'comparator': filter_parts.groups()[1],
                'value_raw': filter_parts.groups()[2],
                'network': False,
                'shift': None
            }
        except AttributeError:
            raise PichiFilterError(f'Malformed filter statement, `{filter_statement}`')
        if filter_obj['variable'] not in cls.VALID_VARIABLES:
            raise PichiFilterError(f'Unknown variable `{filter_obj["variable"]}`')
        if filter_obj['variable'] in ['host', 'src_host', 'dst_host']:
            if '/' in filter_obj['value_raw']:
                cidr = int(filter_obj['value_raw'].split('/')[1])
                addr = filter_obj['value_raw'].split('/')[0]
                filter_obj['network'] = True
                if ':' in filter_obj['value_raw']:
                    filter_obj['shift'] = 128 - cidr
                    filter_obj['value'] = cls.shift_v6(addr, filter_obj['shift'])
                elif '.' in filter_obj['value_raw']:
                    filter_obj['shift'] = 32 - cidr
                    filter_obj['value'] = \
                        struct.unpack('!I', socket.inet_aton(addr))[0] >> filter_obj['shift']
                else:
                    raise PichiFilterError
            elif '/' not in filter_obj['value_raw'] and \
                    ':' not in filter_obj['value_raw'] and re.search(r"[a-zA-Z]", filter_obj['value_raw']):
                filter_obj['value'] = socket.inet_aton(socket.gethostbyname(filter_obj['value_raw']))
            else:
                if ':' in filter_obj['value_raw']:
                    filter_obj['value'] = socket.inet_pton(socket.AF_INET6, filter_obj['value_raw'])
                elif '.' in filter_obj['value_raw']:
                    filter_obj['value'] = socket.inet_aton(filter_obj['value_raw'])
        elif filter_obj['variable'] == 'eth_type':
            filter_obj['value'] = struct.pack('!H', int(filter_obj['value_raw']))
        elif filter_obj['variable'] == 'l2_proto':
            try:
                filter_obj['value'] = struct.pack('B', int(filter_obj['value_raw']))
            except ValueError:
                filter_obj['value'] = struct.pack('B', socket.getprotobyname(filter_obj['value_raw']))
        elif filter_obj['variable'] in ['port', 'src_port', 'dst_port']:
            try:
                filter_obj['value'] = struct.pack('!H', int(filter_obj['value_raw']))
            except ValueError:
                filter_obj['value'] = struct.pack('!H', socket.getservbyname(filter_obj['value_raw']))
        else:
            raise PichiFileError
        return cls(**filter_obj)

    def row_passes_filter(self, row: PichiBinaryRecordRow) -> bool:
        if self.comparator == '==':
            if self.network:
                if self.variable == 'src_host':
                    if len(row.src_host) == 16:
                        return self.value == self.shift_v6(row.src_host, self.shift)
                    elif len(row.src_host) == 4:
                        return self.value == struct.unpack('!I', row.src_host)[0] >> self.shift
                elif self.variable == 'dst_host':
                    if len(row.src_host) == 16:
                        return self.value == self.shift_v6(row.dst_host, self.shift)
                    elif len(row.src_host) == 4:
                        return self.value == struct.unpack('!I', row.dst_host)[0] >> self.shift
                elif self.variable == 'host':
                    if len(row.src_host) == 16:
                        a = self.value == self.shift_v6(row.src_host, self.shift)
                        b = self.value == self.shift_v6(row.dst_host, self.shift)
                        if a or b:
                            return True
                        return False
                    elif len(row.src_host) == 4:
                        a = self.value == struct.unpack('!I', row.src_host)[0] >> self.shift
                        b = self.value == struct.unpack('!I', row.dst_host)[0] >> self.shift
                        if a or b:
                            return True
                        return False
            elif self.variable in ('src_host', 'dst_host', 'src_port', 'dst_port', 'eth_type', 'l2_proto'):
                return self.value == getattr(row, self.variable)
            elif self.variable == 'host':
                return self.value == row.src_host or self.value == row.dst_host
            elif self.variable == 'port':
                return self.value == row.src_port or self.value == row.dst_port
            else:
                raise PichiFilterError
        elif self.comparator == '!=':
            if self.network:
                if self.variable == 'src_host':
                    if len(row.src_host) == 16:
                        return self.value != self.shift_v6(row.src_host, self.shift)
                    elif len(row.src_host) == 4:
                        return self.value != struct.unpack('!I', row.src_host)[0] >> self.shift
                elif self.variable == 'dst_host':
                    if len(row.src_host) == 16:
                        return self.value != self.shift_v6(row.dst_host, self.shift)
                    elif len(row.src_host) == 4:
                        return self.value != struct.unpack('!I', row.dst_host)[0] >> self.shift
                elif self.variable == 'host':
                    if len(row.src_host) == 16:
                        a = self.value != self.shift_v6(row.src_host, self.shift)
                        b = self.value != self.shift_v6(row.dst_host, self.shift)
                        if a or b:
                            return True
                        return False
                    elif len(row.src_host) == 4:
                        a = self.value != struct.unpack('!I', row.src_host)[0] >> self.shift
                        b = self.value != struct.unpack('!I', row.dst_host)[0] >> self.shift
                        if a or b:
                            return True
                        return False
            elif self.variable in ('src_host', 'dst_host', 'src_port', 'dst_port', 'eth_type', 'l2_proto'):
                return self.value != getattr(row, self.variable)
            elif self.variable == 'host':
                return self.value != row.src_host or self.value != row.dst_host
            elif self.variable == 'port':
                return self.value != row.src_port or self.value != row.dst_port
            else:
                raise PichiFilterError
        elif self.comparator == '>=':
            if self.variable in ('src_host', 'dst_host', 'src_port', 'dst_port', 'eth_type', 'l2_proto'):
                return self.value >= getattr(row, self.variable)
            elif self.variable == 'host':
                return self.value >= row.src_host or self.value >= row.dst_host
            elif self.variable == 'port':
                return self.value >= row.src_port or self.value >= row.dst_port
            else:
                raise PichiFilterError
        elif self.comparator == '<=':
            if self.variable in ('src_host', 'dst_host', 'src_port', 'dst_port', 'eth_type', 'l2_proto'):
                return self.value <= getattr(row, self.variable)
            elif self.variable == 'host':
                return self.value <= row.src_host or self.value <= row.dst_host
            elif self.variable == 'port':
                return self.value <= row.src_port or self.value <= row.dst_port
            else:
                raise PichiFilterError
        else:
            raise PichiFilterError


class PichiFilterSet(object):
    """
    A logical grouping of one or more PichiFilters to make checking PichiTextRecordRow's against multiple filters at
      once simple, with the test_filters(row) function.
    """

    __slots__ = ['filter_string', 'binary_filters', 'filters']

    def __init__(
            self,
            filter_string: str,
            binary_filters: bool
    ) -> None:
        self.filter_string = filter_string
        self.binary_filters = binary_filters
        self.filters = self._parse_filters(self.filter_string, binary_filters)

    @staticmethod
    def _parse_filters(
            filter_string: str, binary_filters: bool = False
    ) -> Set[Union[PichiTextFilter, PichiBinaryFilter]]:
        filters = set()
        for filter_statement in filter_string.lower().split():
            if binary_filters:
                filters.add(PichiBinaryFilter.from_filter_statement(filter_statement))
            else:
                filters.add(PichiTextFilter.from_filter_statement(filter_statement))
        return filters

    def test_filters(self, row: Union[PichiTextRecordRow, PichiBinaryRecordRow]) -> bool:
        result = []
        for filter_obj in self.filters:
            result.append(filter_obj.row_passes_filter(row))
        return all(result)
