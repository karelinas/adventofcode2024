import unittest

from day11 import blink


class Day11TestCase(unittest.TestCase):
    def test_simple_example(self):
        stones = [0, 1, 10, 99, 999]
        expected_blink = [1, 2024, 1, 0, 9, 9, 2021976]
        self.assertEqual(blink(stones), expected_blink)

    def test_example_sequence(self):
        stones = [125, 17]
        expected_generations = [
            [253000, 1, 7],
            [253, 0, 2024, 14168],
            [512072, 1, 20, 24, 28676032],
            [512, 72, 2024, 2, 0, 2, 4, 2867, 6032],
            [1036288, 7, 2, 20, 24, 4048, 1, 4048, 8096, 28, 67, 60, 32],
            [
                2097446912,
                14168,
                4048,
                2,
                0,
                2,
                4,
                40,
                48,
                2024,
                40,
                48,
                80,
                96,
                2,
                8,
                6,
                7,
                6,
                0,
                3,
                2,
            ],
        ]
        for n, generation in enumerate(expected_generations, start=1):
            with self.subTest(f"Generation {n}", n=n, generation=generation):
                stones = blink(stones)
                self.assertEqual(stones, generation)

    def test_example_value(self):
        stones = [125, 17]
        self.assertEqual(len(blink(stones, n=25)), 55312)
