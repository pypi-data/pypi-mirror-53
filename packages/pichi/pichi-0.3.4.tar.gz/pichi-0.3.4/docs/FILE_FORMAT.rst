======================
The Pichi File Formats
======================

There are several Pichi file formats, but only one worth caring about. The first is the original text format, which
is easy to parse with common \*nix command line tools and highly portable. The second is whatever the current version
of the binary format is (currently version 3). Historical versions of the binary format are documented here to help
maintain backwards-compatibility, and as a curiosity.


-----------
Text Format
-----------

The text format is very simple and easy to send to tools like ``awk``, ``sed``, ``cut``, etc.

There is no header or footer, and every packet record is contained on its own line with fields pipe-delimited::

   {epoch}.{ms}|{in_filename}|{start}|{end}|{eth_proto}|{ip_proto}|{src_host}|{dst_host}|{src_port}|{dst_port}\n

- ``{in_filename}`` is the name of the input pcap
- ``{start}`` is the first byte of the packet
- ``{end}`` is the last byte of the packet


-------------
Binary Format
-------------


~~~~~~~~~~~~~~~~~~~~~~
Version 4 (*PLANNING*)
~~~~~~~~~~~~~~~~~~~~~~

Proposed deficits of v3
 1. One immediately noticable downside of the version 2 format is that the total file index count is limited to a single
    byte, when real world examples of needing to index more than 254 pcaps are available. This was an oversight when v2
    was created.
 2. Currently in a combined index, if you know from the start that you only care about data from the last file of a 254
    file index, the entire index prior to the last file index has to be read and examined.
 3. While getting a total packet count for the entire index is trivial, in a combined index there is so way to determine
    how much a specific file contributes to that total without parsing the entire index up to that file's end.
 4. Having fast access to total packet and file counts is useful, but if an index is compressed it still means
    seeking through and decompressing the entire file.
 5. The ``Header Length`` field in both the global header and file index header includes the entire header length,
    artificially limiting the available size of file names.

Proposed solutions for v4
 - Change the File Count field to 2 bytes and move it, along with the total packet count, to the global header.
 - Remove the footer entirely, and replace it with a post-global-header index of file names, packet counts, and start
   offsets.
 - The ``Header Length`` field can be changed instead to a ``Name Length`` field, as the rest of the header's
   size is fixed.

In version 4, the global header could look like this::

   .    byte 0     .    byte 1     .    byte 2     .    byte 3     .    byte 4     .    byte 5     .
   +---------------+---------------+---------------+---------------+---------------+---------------+
   |    Version    |  Name Length  |               Index Creation Time (Unix Epoch)                |
   +---------------+---------------+---------------+---------------+---------------+---------------+
   |          File Count           |                      Total Packet Count                       |
   +---------------+---------------+---------------+---------------+---------------+---------------+
   | Index Name . . .

Which would be followed by one or more input file mappings like this::

   .    byte 0     .    byte 1     .    byte 2     .    byte 3     .    byte 4     .
   +---------------+---------------+---------------+---------------+---------------+
   |  Name Length  |                         Packet Count                          |
   +---------------+---------------+---------------+---------------+---------------+
   |                         Start Offset                          | Input Filename . . .
   +---------------+---------------+---------------+---------------+


~~~~~~~~~~~~~~~~~~~~~
Version 3 (*CURRENT*)
~~~~~~~~~~~~~~~~~~~~~

Version 3 is identical to version 2, but the size of the start and stop offset is 8 bytes (to accommodate files larger
than 4.29 Gb -- new limit is over 16 Eb), and the version number in the header is 3 (``b'\x03'``).
Backwards-compatibility for reading and extracting from file format version 2 is retained, but all new indexes will be
written as version 3.

~~~~~~~~~
Version 2
~~~~~~~~~

The binary file format is also relatively simple. It was created to make writing as fast as possible, and parsing easy.

Remember that indexes may or may not be compressed with Gzip.

The magic number is four bytes at the beginning of every binary index: ``b'\xc8\xd3\xf7\x3d'``. After the magic number,
there is a short global header, followed by blocks of data for each input file. Every block has it's own header. At the
very end of the file is a footer.

The global header is formatted as (index 0)::

   .    byte 0     .    byte 1     .    byte 2     .    byte 3     .    byte 4     .    byte 5     .
   +---------------+---------------+---------------+---------------+---------------+---------------+
   |    Version    | Header Length |               Index Creation Time (Unix Epoch)                |
   +---------------+---------------+---------------+---------------+---------------+---------------+
   | Index Name . . .

Version is 2 (``b'\x02'``) for this format. The header length is the total size of the global header, meaning it is
always at least 6. The index name is optional, and set to the output file name if none is provided. The index name can
be up to 249 bytes long.

Directly after the global header is one or more file indexes. At the start of every file index is the separator value
``b'\x0c\x07\x00\x00'``. The reason for this value is explained below. After the file index separator value, the file
index header format is::

   .    byte 0     .    byte 1     .
   +---------------+---------------+
   | Header Length | Input Filename . . .

The header length is the total size of the index file header, meaning it is always at least 2. The input filename is
mandatory, and is the relative path given to Pichi on the command line for the pcap being indexed. The input file name
can be up to 245 bytes long.

Following the index file header is the actual index data, with one record per packet. Note that the size of the
record varies for IPv4 or IPv6, to conserve space::

   .    byte 0     .    byte 1     .    byte 2     .    byte 3     .
   +---------------+---------------+---------------+---------------+
   |                Received Timestamp (Unix Epoch)                |
   +---------------+---------------+---------------+---------------+
   |                 Milliseconds After Timestamp                  |
   +---------------+---------------+---------------+---------------+
   |                 Start Offset in Source PCAP                   |
   +---------------+---------------+---------------+---------------+
   |                  Stop Offset in Source PCAP                   |
   +---------------+---------------+---------------+---------------+
   |           EtherType           | Layer 2 Proto | ->
   +---------------+---------------+---------------+---------------+
   ->                     IPv4 Source Address                      |
   +---------------+---------------+---------------+---------------+
   |                   IPv4 Destination Address                    |
   +---------------+---------------+---------------+---------------+
   |          Source Port          |       Destination Port        |
   +---------------+---------------+---------------+---------------+

Note that the IPv4 Source Address comes directly after the Layer 2 Protocol byte, it is only shifted in the diagram to
make it easier to look at.

The only difference for IPv6 entries is that each address field is 16 bytes long instead of 4.

Packet records follow each-other one after another with no separator. An easy way to tell when you've run out of packets
is to check the received timestamp -- if it is ``b'\x0c\x07\x00\x00'`` (which yields an epoch time of Thursday,
January 1, 1970 12:30:04 AM -- one I suspect that no one was capturing packets on), you've hit the header for another
input file. Alternatively, if it is ``b'a\x07\x00\x00'``, then you've read the final packet record in this index
and hit the separator for the file footer. The footer has the following values::

   .    byte 0     .    byte 1     .    byte 2     .    byte 3     .    byte 4     .
   +---------------+---------------+---------------+---------------+---------------+
   |  File Count   |                         Packet Count                          |
   +---------------+---------------+---------------+---------------+---------------+

The File Count is the number of Index File blocks expected to be contained in the file, and the Packet Count is the
total number of packets. By the end of the file, if the values do not add up then the file was parsed wrong or likely
corrupted. This also means getting a file count and packet count is as simple as:

>>> import struct
>>> with open('pichi.pi', 'rb') as fp:
...     fp.seek(-5, 2)
...     file_count = struct.unpack('B', fp.read(1))[0]
...     packet_count = struct.unpack('I', fp.read(4))[0]


~~~~~~~~~~~~~~~~~~~~~~~~
Version 1 (*DEPRECATED*)
~~~~~~~~~~~~~~~~~~~~~~~~

Version one was only used in unreleased pilot builds. It wasted a lot of bytes on useless separators::

    b'\xc8\xd3\xf7\x3d' - Magic number (CRC32 of 'Zaedyus')
    b'\x01' - SOH
    1 byte - Length of header
    1 byte - PiB version (1 for this version)
    4 byte - index creation time
    n bytes - index filename
        b'\x02' - STX
        1 byte - Length of file header
        n bytes - source filename
        b'\x03' - ETX
            8 bytes - timestamp w/ ms
            b'\x1f' - US
            4 bytes - start position
            b'\x1f' - US
            4 bytes - end position
            b'\x1f' - US
            2 bytes - EtherType
            b'\x1f' - US
            1 byte - L2 Proto
            b'\x1f' - US
            4-16 bytes - source address
            b'\x1f' - US
            4-16 bytes - dest address
            b'\x1f' - US
            2 bytes - source port
            b'\x1f' - US
            2 bytes - dest port
            b'\x1e' - RS
    b'\x1d' - GS
    1 byte - input file count
    4 bytes - packet count
    b'\x04' - EOT
