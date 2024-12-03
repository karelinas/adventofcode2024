import unittest

from day01 import parse_pairs, similarity_score, total_distance

EXAMPLE_INPUT: str = """
3   4
4   3
2   5
1   3
3   9
3   3
"""


class Day01TestCase(unittest.TestCase):
    def test_calibration_value_example_part1(self):
        pairs = parse_pairs(EXAMPLE_INPUT)
        self.assertEqual(total_distance(pairs), 11)

    def test_calibration_value_example_part2(self):
        pairs = parse_pairs(EXAMPLE_INPUT)
        self.assertEqual(similarity_score(pairs), 31)
