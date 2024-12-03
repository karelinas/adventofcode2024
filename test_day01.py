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
    def test_example_data(self):
        pairs = parse_pairs(EXAMPLE_INPUT)

        with self.subTest("Part 1"):
            self.assertEqual(total_distance(pairs), 11)
        with self.subTest("Part 2"):
            self.assertEqual(similarity_score(pairs), 31)
