import unittest

from day19 import count_possible_arrangements, count_possible_designs, parse_towels

EXAMPLE_TOWELS = """
r, wr, b, g, bwu, rb, gb, br

brwrr
bggr
gbbr
rrbgbr
ubwu
bwurrg
brgr
bbrgwb
""".strip()


class Day19TestCase(unittest.TestCase):
    def test_example(self):
        patterns, towels = parse_towels(EXAMPLE_TOWELS)
        with self.subTest("Part 1"):
            self.assertEqual(count_possible_designs(patterns, towels), 6)
        with self.subTest("Part 2"):
            self.assertEqual(count_possible_arrangements(patterns, towels), 16)
