from dataclasses import dataclass
from itertools import combinations
from sys import stdin
from typing import Optional

from lib import Point, manhattan_distance, orthogonal_neighborhood


def main() -> None:
    grid = Grid.from_string(stdin.read())
    print("Part 1:", count_good_2cheats(grid))
    print("Part 2:", count_good_20cheats(grid))


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


def make_costs(grid: Grid) -> dict[Point, int]:
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
    return cost


def count_good_ncheats(grid: Grid, *, n: int, minimum_score: int = 100) -> int:
    cost: dict[Point, int] = make_costs(grid)

    return sum(
        1
        for f, t in combinations(grid.grid, 2)
        if manhattan_distance(f, t) <= n
        and abs(cost[t] - cost[f]) - manhattan_distance(f, t) >= minimum_score
    )


def count_good_2cheats(grid: Grid, *, minimum_score: int = 100) -> int:
    return count_good_ncheats(grid, n=2, minimum_score=minimum_score)


def count_good_20cheats(grid: Grid, *, minimum_score: int = 100) -> int:
    return count_good_ncheats(grid, n=20, minimum_score=minimum_score)


if __name__ == "__main__":
    main()
