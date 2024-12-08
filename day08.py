from dataclasses import dataclass
from itertools import permutations
from sys import stdin
from typing import Callable

from lib import Point

AntinodeFunction = Callable[["Grid", tuple[Point, str], tuple[Point, str]], set[Point]]


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
    print("Part 2:", count_antinodes_harmonic(grid))


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


def pairwise_antinodes(
    grid: Grid, a: tuple[Point, str], b: tuple[Point, str]
) -> set[Point]:
    """Generate antinodes for antenna a with respect to antenna b"""
    if a[1] != b[1]:
        # antenna pair is not on the same frequency, so it does not create antinodes
        return set()
    delta: Point = a[0] - b[0]
    candidate_antinode: Point = a[0] + delta
    return set([candidate_antinode]) if grid.in_bounds(candidate_antinode) else set()


def pairwise_antinodes_harmonic(
    grid: Grid, a: tuple[Point, str], b: tuple[Point, str]
) -> set[Point]:
    """Generate harmonic antinodes for antenna a with respect to antenna b"""
    if a[1] != b[1]:
        # antenna pair is not on the same frequency, so it does not create antinodes
        return set()

    delta: Point = a[0] - b[0]

    # Harmonic antinodes for antenna a
    harmonic_antinodes: set[Point] = set()
    candidate_antinode: Point = a[0]
    while grid.in_bounds(candidate_antinode):
        harmonic_antinodes.add(candidate_antinode)
        candidate_antinode = candidate_antinode + delta

    return harmonic_antinodes


def count_antinodes_impl(grid: Grid, *, antinode_fn: AntinodeFunction) -> int:
    return len(
        set(
            antinode
            for a, b in permutations(grid.grid.items(), 2)
            for antinode in antinode_fn(grid, a, b)
        )
    )


def count_antinodes(grid: Grid) -> int:
    return count_antinodes_impl(grid, antinode_fn=pairwise_antinodes)


def count_antinodes_harmonic(grid: Grid) -> int:
    return count_antinodes_impl(grid, antinode_fn=pairwise_antinodes_harmonic)


if __name__ == "__main__":
    main()
