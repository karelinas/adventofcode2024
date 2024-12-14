import unittest

from day14 import Simulation, safety_factor

EXAMPLE_ROBOTS = """
p=0,4 v=3,-3
p=6,3 v=-1,-3
p=10,3 v=-1,2
p=2,0 v=2,-1
p=0,0 v=1,3
p=3,0 v=-2,-2
p=7,6 v=-1,-3
p=3,0 v=-1,-2
p=9,3 v=2,3
p=7,3 v=-1,2
p=2,4 v=2,-3
p=9,5 v=-3,-3
""".strip()


class Day14TestCase(unittest.TestCase):
    def test_example_data(self):
        sim = Simulation.from_string(EXAMPLE_ROBOTS)
        sim.width = 11
        sim.height = 7

        with self.subTest("Part 1"):
            self.assertEqual(safety_factor(sim.simulate(100)), 12)
