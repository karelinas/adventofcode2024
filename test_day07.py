import unittest

from day07 import parse_equations, sum_of_true_equations

EXAMPLE_EQUATIONS = """
190: 10 19
3267: 81 40 27
83: 17 5
156: 15 6
7290: 6 8 6 15
161011: 16 10 13
192: 17 8 14
21037: 9 7 18 13
292: 11 6 16 20
"""


class Day07TestCase(unittest.TestCase):
    def test_example_data(self):
        equations = parse_equations(EXAMPLE_EQUATIONS)
        with self.subTest("Part 1"):
            self.assertEqual(sum_of_true_equations(equations), 3749)
        with self.subTest("Part 2"):
            self.assertEqual(
                sum_of_true_equations(equations, enable_concat=True), 11387
            )
