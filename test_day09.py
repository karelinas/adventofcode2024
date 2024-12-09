import unittest

from day09 import DiskMap, checksum

EXAMPLE_BLOCKS = "2333133121414131402"


class Day08TestCase(unittest.TestCase):
    def test_example_data(self):
        diskmap = DiskMap.from_string(EXAMPLE_BLOCKS)
        with self.subTest("Part 1"):
            self.assertEqual(checksum(diskmap), 1928)
