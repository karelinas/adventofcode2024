import unittest

from day12 import Grid, total_price

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


class Day10TestCase(unittest.TestCase):
    def test_example_data(self):
        grid = Grid.from_string(EXAMPLE_GRID)
        with self.subTest("Part 1"):
            self.assertEqual(total_price(grid), 1930)
