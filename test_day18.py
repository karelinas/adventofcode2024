import unittest

from day18 import Grid, shortest_path_length
from lib import Point

EXAMPLE_BYTES = """
5,4
4,2
4,5
3,0
2,1
6,3
2,4
1,5
0,6
3,3
2,6
5,1
1,2
5,5
2,5
6,5
1,4
0,4
6,4
1,1
6,1
1,0
0,5
1,6
2,0
""".strip()


class Day18TestCase(unittest.TestCase):
    def test_example(self):
        grid = Grid.from_string(EXAMPLE_BYTES)
        grid.goal = Point(6, 6)
        self.assertEqual(shortest_path_length(grid.simulate(n=12)), 22)
