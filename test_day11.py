import unittest

from day11 import blink


class Day11TestCase(unittest.TestCase):
    def test_simple_example(self):
        stones = [0, 1, 10, 99, 999]
        self.assertEqual(blink(stones, n=1), 7)

    def test_example_sequence(self):
        stones = [125, 17]
        expected_generations = [3, 4, 5, 9, 13, 22]

        for n, generation in enumerate(expected_generations, start=1):
            with self.subTest(f"Generation {n}", n=n, generation=generation):
                stone_count = blink(stones, n=n)
                self.assertEqual(stone_count, generation)

    def test_example_value(self):
        stones = [125, 17]
        self.assertEqual(blink(stones, n=25), 55312)
