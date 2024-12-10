import unittest

from day10 import Grid, count_distinct_trailheads, sum_trail_ratings

EXAMPLE_GRID = """
89010123
78121874
87430965
96549874
45678903
32019012
01329801
10456732
"""


class Day08TestCase(unittest.TestCase):
    def test_example_data(self):
        grid = Grid.from_string(EXAMPLE_GRID)
        with self.subTest("Part 1"):
            self.assertEqual(count_distinct_trailheads(grid), 36)
        with self.subTest("Part 2"):
            self.assertEqual(sum_trail_ratings(grid), 81)
