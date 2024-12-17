import unittest

from day17 import Cpu

EXAMPLE_PROGRAM = """
Register A: 729
Register B: 0
Register C: 0

Program: 0,1,5,4,3,0
""".strip()


class Day17TestCase(unittest.TestCase):
    def test_example_program(self):
        cpu = Cpu.from_string(EXAMPLE_PROGRAM)
        cpu.run()
        with self.subTest("Part 1"):
            self.assertEqual(cpu.stdout(), "4,6,3,5,6,3,5,2,1,0")
