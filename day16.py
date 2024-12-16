from collections import defaultdict
from dataclasses import dataclass
from heapq import heappop, heappush
from sys import stdin
from typing import Optional

from lib import Point, orthogonal_directions

DEFAULT_HEADING = Point.east()


def main() -> None:
    maze = Maze.from_string(stdin.read())
    print("Part 1:", best_score(maze))


@dataclass
class Maze:
    maze: set[Point]
    start: Point
    end: Point

    @staticmethod
    def from_string(data: str) -> "Maze":
        filtered_lines: list[str] = [line for line in data.strip().split("\n") if line]
        maze: set[Point] = set()
        start: Optional[Point] = None
        end: Optional[Point] = None
        for y, line in enumerate(filtered_lines):
            for x, ch in enumerate(line.strip()):
                p = Point(x, y)
                if ch != "#":
                    maze.add(p)
                if ch == "S":
                    start = p
                elif ch == "E":
                    end = p

        assert start, "Input must include a start point"
        assert end, "Input must include an end point"
        return Maze(maze=maze, start=start, end=end)


# cost, position, heading
QueueItem = tuple[int, Point, Point]
# position, heading
CostKey = tuple[Point, Point]


def best_score(maze: Maze) -> int:
    queue: list[QueueItem] = []
    heappush(queue, (0, maze.start, DEFAULT_HEADING))

    path_costs: dict[CostKey, int] = defaultdict(lambda: 2**32)
    seen: set[CostKey] = set()

    while queue:
        cost, pos, heading = heappop(queue)

        if pos == maze.end:
            return int(cost)

        if (pos, heading) in seen:
            continue
        seen.add((pos, heading))

        for direction in orthogonal_directions():
            next_pos: Point = pos + direction
            if next_pos not in maze.maze:
                continue

            cost_to_move: int = 1
            if direction != heading:
                cost_to_move += 1000

            cost_to_destination: int = cost + cost_to_move
            if cost_to_destination >= path_costs[(next_pos, direction)]:
                continue

            path_costs[(next_pos, direction)] = cost_to_destination
            heappush(queue, (cost_to_destination, next_pos, direction))

    assert None, "Path not found"


if __name__ == "__main__":
    main()
