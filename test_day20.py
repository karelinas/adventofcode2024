import unittest

from day20 import Grid, count_good_2cheats, count_good_20cheats

EXAMPLE_GRID = """
###############
#...#...#.....#
#.#.#.#.#.###.#
#S#...#.#.#...#
#######.#.#.###
#######.#.#...#
#######.#.###.#
###..E#...#...#
###.#######.###
#...###...#...#
#.#####.#.###.#
#.#...#.#.#...#
#.#.#.#.#.#.###
#...#...#...###
###############
""".strip()


class Day20TestCase(unittest.TestCase):
    def test_2cheats(self):
        grid = Grid.from_string(EXAMPLE_GRID)
        self.assertEqual(count_good_2cheats(grid, minimum_score=2), 44)
        self.assertEqual(count_good_2cheats(grid, minimum_score=10), 10)
        self.assertEqual(count_good_2cheats(grid, minimum_score=20), 5)

    def test_20cheats(self):
        grid = Grid.from_string(EXAMPLE_GRID)
        self.assertEqual(count_good_20cheats(grid, minimum_score=70), 41)
        self.assertEqual(count_good_20cheats(grid, minimum_score=74), 7)
        self.assertEqual(count_good_20cheats(grid, minimum_score=76), 3)
