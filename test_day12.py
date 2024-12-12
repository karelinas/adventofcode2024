import unittest

from day12 import discounted_price, parse_regions, total_price

EXAMPLE_GRID = """
RRRRIICCFF
RRRRIICCCF
VVRRRCCFFF
VVRCCCJFFF
VVVVCJJCFE
VVIVCCJJEE
VVIIICJJEE
MIIIIIJJEE
MIIISIJEEE
MMMISSJEEE
"""


class Day12TestCase(unittest.TestCase):
    def test_example_data(self):
        regions = parse_regions(EXAMPLE_GRID)
        with self.subTest("Part 1"):
            self.assertEqual(total_price(regions), 1930)
        with self.subTest("Part 2"):
            self.assertEqual(discounted_price(regions), 1206)
