from dataclasses import dataclass
from sys import stdin

from lib import Point, orthogonal_neighborhood


def main() -> None:
    grid = Grid.from_string(stdin.read())
    print("Part 1:", count_distinct_trailheads(grid))
    print("Part 2:", sum_trail_ratings(grid))


@dataclass
class Grid:
    grid: dict[Point, int]

    def in_bounds(self, p: Point) -> bool:
        return p in self.grid

    @staticmethod
    def from_string(data: str) -> "Grid":
        filtered_lines = [line for line in data.strip().split("\n") if line]
        grid = {
            Point(x, y): int(ch)
            for y, line in enumerate(filtered_lines)
            for x, ch in enumerate(line.strip())
        }
        return Grid(grid=grid)


def count_distinct_trailheads(grid: Grid) -> int:
    return sum(
        len(set(trail_heads(grid, pos)))
        for pos, height in grid.grid.items()
        if height == 0
    )


def sum_trail_ratings(grid: Grid) -> int:
    return sum(
        len(trail_heads(grid, pos)) for pos, height in grid.grid.items() if height == 0
    )


def trail_heads(grid: Grid, pos: Point) -> list[Point]:
    if grid.grid[pos] == 9:
        return [pos]
    heads: list[Point] = []
    for new_pos in orthogonal_neighborhood(pos):
        if grid.in_bounds(new_pos) and grid.grid[new_pos] == grid.grid[pos] + 1:
            heads.extend(trail_heads(grid, new_pos))
    return heads


if __name__ == "__main__":
    main()
