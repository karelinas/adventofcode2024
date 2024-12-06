import unittest

from day06 import count_guard_positions, count_looping_configurations, parse_map

EXAMPLE_MAP = """
....#.....
.........#
..........
..#.......
.......#..
..........
.#..^.....
........#.
#.........
......#...
"""


class Day06TestCase(unittest.TestCase):
    def test_example_data(self):
        grid, guard = parse_map(EXAMPLE_MAP)
        with self.subTest("Part 1"):
            self.assertEqual(count_guard_positions(grid, guard), 41)
        with self.subTest("Part 2"):
            self.assertEqual(count_looping_configurations(grid, guard), 6)
