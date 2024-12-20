import unittest

from day20 import Grid, count_good_cheats

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
    def test_example(self):
        grid = Grid.from_string(EXAMPLE_GRID)
        self.assertEqual(count_good_cheats(grid, minimum_score=2), 44)
        self.assertEqual(count_good_cheats(grid, minimum_score=10), 10)
        self.assertEqual(count_good_cheats(grid, minimum_score=20), 5)
