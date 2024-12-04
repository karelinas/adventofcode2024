import unittest

from day04 import Grid

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
    def test_example_data_part1(self):
        grid = Grid.from_string(EXAMPLE_GRID)
        self.assertEqual(grid.count_occurrences("XMAS"), 18)
