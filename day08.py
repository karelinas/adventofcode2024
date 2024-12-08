from dataclasses import dataclass
from itertools import combinations
from sys import stdin

from lib import Point


@dataclass
class Grid:
    grid: dict[Point, str]
    width: int
    height: int

    def in_bounds(self, p: Point) -> bool:
        return p.x >= 0 and p.x < self.width and p.y >= 0 and p.y < self.height


def main() -> None:
    grid = parse_grid(stdin.read())
    print("Part 1:", count_antinodes(grid))


def parse_grid(data: str) -> Grid:
    non_empty_lines: list[str] = [line for line in data.strip().split("\n") if line]
    unfiltered_grid: dict[Point, str] = {
        Point(x, y): ch
        for y, line in enumerate(non_empty_lines)
        for x, ch in enumerate(line.strip())
    }
    width: int = max(p.x for p in unfiltered_grid.keys()) + 1
    height: int = max(p.y for p in unfiltered_grid.keys()) + 1

    # leave only antennas in the grid, as empty squares are not necessary
    # for the calculations
    filtered_grid: dict[Point, str] = {
        p: ch for p, ch in unfiltered_grid.items() if ch != "."
    }
    return Grid(grid=filtered_grid, width=width, height=height)


def count_antinodes(grid: Grid) -> int:
    def antinodes_for_pair(a: tuple[Point, str], b: tuple[Point, str]) -> set[Point]:
        if a[1] != b[1]:
            return set()
        delta: Point = a[0] - b[0]
        return set(p for p in [a[0] + delta, b[0] - delta] if grid.in_bounds(p))

    return len(
        set(
            antinode
            for a, b in combinations(grid.grid.items(), 2)
            for antinode in antinodes_for_pair(a, b)
        )
    )


if __name__ == "__main__":
    main()
