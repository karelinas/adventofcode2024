import unittest

from day19 import count_possible_designs, parse_towels

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


class Day18TestCase(unittest.TestCase):
    def test_example(self):
        patterns, towels = parse_towels(EXAMPLE_TOWELS)
        self.assertEqual(count_possible_designs(patterns, towels), 6)
