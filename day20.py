from dataclasses import dataclass
from sys import stdin
from typing import Optional

from lib import Point, orthogonal_directions, orthogonal_neighborhood


def main() -> None:
    grid = Grid.from_string(stdin.read())
    print("Part 1:", count_good_cheats(grid))


@dataclass
class Grid:
    grid: set[Point]
    start: Point
    end: Point

    @staticmethod
    def from_string(data: str) -> "Grid":
        filtered_lines: list[str] = [line for line in data.strip().split("\n") if line]

        grid: set[Point] = set()
        start: Optional[Point] = None
        end: Optional[Point] = None

        for y, line in enumerate(filtered_lines):
            for x, ch in enumerate(line.strip()):
                p = Point(x, y)
                if ch == "S":
                    start = p
                    grid.add(p)
                elif ch == "E":
                    end = p
                    grid.add(p)
                elif ch == ".":
                    grid.add(p)

        assert start, "Path must have a start point"
        assert end, "Path must have an end point"

        return Grid(grid=grid, start=start, end=end)


def count_good_cheats(grid: Grid, *, minimum_score: int = 100) -> int:
    # Build the path and costs to get to each point on the path
    cost: dict[Point, int] = {}
    distance: int = 0
    current: Optional[Point] = grid.start
    while current:
        cost[current] = distance
        distance += 1
        current = next(
            (
                p
                for p in orthogonal_neighborhood(current)
                if p in grid.grid and p not in cost
            ),
            None,
        )

    # Count shortcuts
    shortcut_count: int = 0
    for pos in grid.grid:
        for d in orthogonal_directions():
            if d in grid.grid:
                # not a wall
                continue

            next_pos: Point = pos + (d * 2)
            if next_pos not in grid.grid or cost[next_pos] < cost[pos]:
                # not a shortcut
                continue

            saves: int = cost[next_pos] - cost[pos] - 2
            if saves >= minimum_score:
                shortcut_count += 1

    return shortcut_count


if __name__ == "__main__":
    main()
