#!/usr/bin/env python
# -*- coding: utf-8 -*-
from random import Random
import socket
import logging
import math
import struct
from typing import Union, Dict, Generator, Any


class BloomFilter:
    # Adapted from: http://code.activestate.com/recipes/577684-bloom-filter/
    def __init__(self, num_bytes, num_probes) -> None:
        self.array = bytearray(num_bytes)
        self.num_probes = num_probes
        self.num_bins = num_bytes * 8

    def get_probes(self, key) -> Generator[int, Any, None]:
        random = Random(key).random
        return (int(random() * self.num_bins) for _ in range(self.num_probes))

    def update(self, keys) -> None:
        for key in keys:
            for i in self.get_probes(key):
                self.array[i//8] |= 2 ** (i % 8)

    def load(self, byte_array) -> None:
        self.array = byte_array

    def write(self, filename) -> None:
        with open(filename, 'wb') as bloom_fp:
            bloom_fp.write(struct.pack('<QB', self.num_bins // 8, self.num_probes))
            bloom_fp.write(bytes(self.array))

    def bulk_check(self, items) -> Dict[Union[str, bytes], bool]:
        results = {}
        for item in items:
            results[item] = item in self
        return results

    @classmethod
    def from_num_entries(cls, num_entries, probability=0.0001) -> 'BloomFilter':
        num_bits = math.ceil((num_entries * math.log(probability)) / math.log(1 / pow(2, math.log(2))))
        num_probes = round((num_bits / num_entries) * math.log(2))
        return cls(num_bits // 8, num_probes)

    @classmethod
    def from_file(cls, filename) -> 'BloomFilter':
        with open(filename, 'rb') as bloom_fp:
            num_bytes, num_probes = struct.unpack('<QB', bloom_fp.read(9))
            bloom_bytes = bloom_fp.read()
        bloom_filter = cls(num_bytes=num_bytes, num_probes=num_probes)
        bloom_filter.load(bytearray(bloom_bytes))
        return bloom_filter

    def check_efficiency(self, items_in_filter, random_trials=100000) -> Dict[str, Union[int, float]]:
        from random import getrandbits
        data_matches = sum(item in self for item in items_in_filter)
        random_matches = 0
        trials = 0
        while trials < random_trials:
            random_value = getrandbits(32).to_bytes(4, byteorder='big')
            if random_value in items_in_filter:
                continue
            if random_value in self:
                random_matches += 1
            trials += 1
        density = ''.join(format(x, '08b') for x in self.array)
        bit_density = density.count('1') / float(len(density))
        return {
            'true_positives': data_matches,
            'false_negatives': len(items_in_filter) - data_matches,
            'true_negatives': random_trials - random_matches,
            'false_positives': random_matches,
            'bit_density': bit_density
        }

    def __contains__(self, key) -> bool:
        if isinstance(key, str):
            if ':' in key:
                key = socket.inet_pton(socket.AF_INET6, key)
            elif '.' in key:
                key = socket.inet_aton(key)
            else:
                raise ValueError
        return all(self.array[i//8] & (2 ** (i % 8)) for i in self.get_probes(key))


class BloomChecker(object):
    def __init__(
            self,
            filename: str,
            ip_addresses: Union[list, str],
            **kwargs
    ) -> None:
        self.filename = filename
        if isinstance(ip_addresses, str):
            ip_addresses = ip_addresses.split()
        self.ip_addresses = ip_addresses

    def check(self) -> Dict[str, bool]:
        bloom_filter = BloomFilter.from_file(self.filename)
        results = bloom_filter.bulk_check(self.ip_addresses)
        for address in results:
            logging.info(f'{address}: {results[address]}')
        return results
