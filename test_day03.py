import unittest

from day03 import Computer, MulComputer


class Day03TestCase(unittest.TestCase):
    def test_example_data_part1(self):
        computer = MulComputer(
            "xmul(2,4)%&mul[3,7]!@^do_not_mul(5,5)+mul(32,64]then(mul(11,8)mul(8,5))"
        )
        self.assertEqual(computer.run(), 161)

    def test_example_data_part2(self):
        computer = Computer(
            "xmul(2,4)&mul[3,7]!^don't()_mul(5,5)+mul(32,64](mul(11,8)undo()?mul(8,5))"
        )
        self.assertEqual(computer.run(), 48)
