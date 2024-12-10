from dataclasses import dataclass
from sys import stdin

from lib import Point, orthogonal_neighborhood


def main() -> None:
    grid = Grid.from_string(stdin.read())
    print("Part 1:", count_trailheads(grid))


@dataclass
class Grid:
    grid: dict[Point, int]
    height: int
    width: int

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
        width: int = max(p.x for p in grid.keys()) + 1
        height: int = max(p.y for p in grid.keys()) + 1
        return Grid(grid=grid, height=height, width=width)


def count_trailheads(grid: Grid) -> int:
    return sum(
        len(trail_heads(grid, pos)) for pos, height in grid.grid.items() if height == 0
    )


def trail_heads(grid: Grid, pos: Point) -> set[Point]:
    if grid.grid[pos] == 9:
        return set([pos])
    heads: set[Point] = set()
    for new_pos in orthogonal_neighborhood(pos):
        if grid.in_bounds(new_pos) and grid.grid[new_pos] == grid.grid[pos] + 1:
            heads.update(trail_heads(grid, new_pos))
    return heads


if __name__ == "__main__":
    main()
