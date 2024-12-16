import unittest

from day16 import Maze, best_path_tiles, best_score

EXAMPLE_MAZE_SMALLER = """
###############
#.......#....E#
#.#.###.#.###.#
#.....#.#...#.#
#.###.#####.#.#
#.#.#.......#.#
#.#.#####.###.#
#...........#.#
###.#.#####.#.#
#...#.....#.#.#
#.#.#.###.#.#.#
#.....#...#.#.#
#.###.#.#.#.#.#
#S..#.....#...#
###############
""".strip()

EXAMPLE_MAZE_LARGER = """
#################
#...#...#...#..E#
#.#.#.#.#.#.#.#.#
#.#.#.#...#...#.#
#.#.#.#.###.#.#.#
#...#.#.#.....#.#
#.#.#.#.#.#####.#
#.#...#.#.#.....#
#.#.#####.#.###.#
#.#.#.......#...#
#.#.###.#####.###
#.#.#...#.....#.#
#.#.#.#####.###.#
#.#.#.........#.#
#.#.#.#########.#
#S#.............#
#################
""".strip()


class Day16TestCase(unittest.TestCase):
    def test_example_maze_small(self):
        maze = Maze.from_string(EXAMPLE_MAZE_SMALLER)
        with self.subTest("Part 1"):
            self.assertEqual(best_score(maze), 7036)
        with self.subTest("Part 2"):
            self.assertEqual(best_path_tiles(maze), 45)

    def test_example_maze_large(self):
        maze = Maze.from_string(EXAMPLE_MAZE_LARGER)
        with self.subTest("Part 1"):
            self.assertEqual(best_score(maze), 11048)
        with self.subTest("Part 2"):
            self.assertEqual(best_path_tiles(maze), 64)
