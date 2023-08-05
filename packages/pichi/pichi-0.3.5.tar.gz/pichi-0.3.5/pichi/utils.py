#!/usr/bin/env python
# -*- coding: utf-8 -*-
import argparse
import logging

from pichi.version import __version__


def get_options() -> dict:
    parser = argparse.ArgumentParser(
        prog='pichi',
        description="Create and use simple pcap indexes",
        fromfile_prefix_chars='@'
    )
    parser.add_argument(
        "-V",
        "--version",
        action="version",
        version="%(prog)s {}".format(__version__)
    )
    parser.add_argument(
        "-d",
        "--debug",
        action="store_true",
        dest="debug_logging",
        help="Show debug messages"
    )
    subparsers = parser.add_subparsers(help='sub-command help')
    index_subparser = subparsers.add_parser('index', help='Create a Pichi index from pcap(s)')
    index_subparser.set_defaults(func='index')
    index_subparser.add_argument(
        "-i",
        "--input",
        action="append",
        required=True,
        metavar="PCAP",
        dest="input_pcaps",
        help="Input file (pcap or pcap.gz)"
    )
    index_subparser.add_argument(
        "-m",
        "--mode",
        action="store",
        choices=['individual', 'combined'],
        default='individual',
        metavar="MODE",
        dest="mode",
        help="The mode for writing indexes. Combined for one shared index, individual for an index per input file."
    )
    index_subparser.add_argument(
        "-o",
        "--output",
        action="store",
        metavar="FILE/DIR",
        dest="output_path",
        help="Output file in combined mode, or output directory in individual"
    )
    index_subparser.add_argument(
        "-f",
        "--format",
        action="store",
        choices=['text', 'bin'],
        default='text',
        metavar="FORMAT",
        dest="file_format",
        help="Output format, text for plaintext (slower to index, faster to extract), or bin for binary (the reverse)."
    )
    index_subparser.add_argument(
        "-z",
        "--compress",
        action="store_true",
        dest="output_compressed",
        help="Compress output"
    )
    index_subparser.add_argument(
        "-B",
        "--create-bloom-filter",
        action="store_true",
        dest="write_bloom_filter",
        help="Specify this flag to also create a bloom filter for testing IP's against with the `bloom` subcommand. \
             Only works with binary indexes"
    )

    extract_subparser = subparsers.add_parser('extract', help='Extract traffic using a pichi index')
    extract_subparser.set_defaults(func='extract')
    extract_subparser.add_argument(
        "-i",
        "--input",
        action="store",
        required=True,
        metavar="INDEX",
        dest="input_index",
        help="Input index"
    )
    extract_subparser.add_argument(
        "-I",
        "--input-prefix",
        action="store",
        metavar="DIR",
        dest="input_prefix",
        help="Prefix directory for pcap file names stored in index, defaults to nothing"
    )
    extract_subparser.add_argument(
        "-o",
        "--output",
        action="store",
        metavar="FILE",
        dest="output_pcap",
        help="Output pcap file for indexed packets"
    )
    extract_subparser.add_argument(
        "-F",
        "--filter",
        action="store",
        metavar="FILTER",
        dest="index_filter",
        help="Filter statement for determining which packets to keep and ignore (see README.rst for more info)"
    )
    extract_subparser.add_argument(
        "-g",
        "--compress-fix",
        action="store_true",
        dest="fix_input_compressed",
        help="If the files stored in the indexes do not have a .gz prefix, add it prior to extraction"
    )
    extract_subparser.add_argument(
        "-z",
        "--compress",
        action="store_true",
        dest="output_compressed",
        help="Compress output pcap"
    )
    extract_subparser.add_argument(
        "-M",
        "--memory",
        action="store_true",
        dest="load_to_memory",
        help="Load the index into memory first. CAUTION: faster, but will use at least 1.3 x uncompressed index size \
              in memory!"
    )

    bloom_subparser = subparsers.add_parser('bloom', help='Check to see if a given IP is in a given Bloom Filter')
    bloom_subparser.set_defaults(func='bloom')
    bloom_subparser.add_argument(
        "-b",
        "--bloom-filter",
        action="store",
        metavar="FILE",
        dest="filename",
        help="The bloom filter to check against"
    )
    bloom_subparser.add_argument(
        "-i",
        "--ip-address",
        action="store",
        metavar="ADDR",
        dest="ip_addresses",
        help="The IP address to check. Multiple can be specified by separating with a space"
    )

    options = vars(parser.parse_args())
    if options['debug_logging']:
        logging.basicConfig(level=logging.DEBUG, format='%(asctime)s [%(levelname)-7s] %(message)s')
    else:
        logging.basicConfig(level=logging.INFO, format='%(message)s')

    del options['debug_logging']

    if options['func'] == 'extract':
        del options['func']
        from pichi import PichiExtractor
        options['func'] = PichiExtractor(**options).extract
    elif options['func'] == 'index':
        del options['func']
        if options['file_format'] == 'text':
            from pichi import PichiTextIndexer
            del options['file_format']
            options['func'] = PichiTextIndexer(**options).index
        elif options['file_format'] == 'bin':
            from pichi import PichiBinaryIndexer
            del options['file_format']
            options['func'] = PichiBinaryIndexer(**options).index
        else:
            raise ValueError(f'Unsupported file format choice, `{options["file_format"]}`!')
    elif options['func'] == 'bloom':
        del options['func']
        from pichi.bloom import BloomChecker
        options['func'] = BloomChecker(**options).check
    else:
        raise ValueError(f'Unsupported function, `{options["func"]}`!')

    return options


def bytes_to_hr(num: int) -> str:
    """
    Convert bytes into a human-readable string.

    Adapted from https://stackoverflow.com/questions/1094841/reusable-library-to-get-human-readable-version-of-file-size
    """
    for unit in [' B', ' KiB', ' MiB', ' GiB', ' TiB', ' PiB', ' EiB', ' ZiB']:
        if abs(num) < 1024.0:
            return f"{num:3.2f}{unit}"
        num /= 1024.0
    return f"{num:.2f} YiB"
