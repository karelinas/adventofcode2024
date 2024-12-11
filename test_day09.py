import unittest

from day09 import DiskMap, checksum, checksum2

EXAMPLE_BLOCKS = "2333133121414131402"


class Day09TestCase(unittest.TestCase):
    def test_example_data(self):
        diskmap = DiskMap.from_string(EXAMPLE_BLOCKS)
        with self.subTest("Part 1"):
            self.assertEqual(checksum(diskmap), 1928)
        with self.subTest("Part 2"):
            self.assertEqual(checksum2(diskmap), 2858)
