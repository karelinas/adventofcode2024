import unittest

from day04 import Grid, make_patterns

EXAMPLE_GRID = """
MMMSXXMASM
MSAMXMSMSA
AMXSXMAAMM
MSAMASMSMX
XMASAMXAMM
XXAMMXXAMA
SMSMSASXSS
SAXAMASAAA
MAMMMXMMMM
MXMXAXMASX
"""


class Day04TestCase(unittest.TestCase):
    def test_example_data(self):
        grid = Grid.from_string(EXAMPLE_GRID)
        with self.subTest("Part 1"):
            self.assertEqual(grid.count_occurrences("XMAS"), 18)
        with self.subTest("Part 2"):
            self.assertEqual(grid.count_patterns(make_patterns()), 9)
