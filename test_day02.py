import unittest

from day02 import parse_reports, safe_count, safe_count_with_tolerance

EXAMPLE_INPUT: str = """
7 6 4 2 1
1 2 7 8 9
9 7 6 2 1
1 3 2 4 5
8 6 4 4 1
1 3 6 7 9
"""


class Day02TestCase(unittest.TestCase):
    def test_calibration_value_example_part1(self):
        reports = parse_reports(EXAMPLE_INPUT)
        self.assertEqual(safe_count(reports), 2)

    def test_calibration_value_example_part2(self):
        reports = parse_reports(EXAMPLE_INPUT)
        self.assertEqual(safe_count_with_tolerance(reports), 4)
