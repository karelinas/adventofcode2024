from collections import defaultdict
from dataclasses import dataclass
from sys import stdin
from typing import Iterable

from lib import Point, orthogonal_neighborhood


def main() -> None:
    grid = Grid.from_string(stdin.read())
    print("Part 1:", total_price(grid))
    print("Part 2:", discounted_price(grid))


@dataclass
class Plot:
    plant: str
    region_id: int


@dataclass
class Grid:
    grid: dict[Point, Plot]

    @staticmethod
    def from_string(data: str) -> "Grid":
        # remove empty lines from input
        filtered_lines: list[str] = [line for line in data.strip().split("\n") if line]

        # make a simple plant grid
        plants: dict[Point, str] = {
            Point(x, y): plant
            for y, line in enumerate(filtered_lines)
            for x, plant in enumerate(line.strip())
        }

        # find regions and give each a unique ID
        regions: dict[Point, int] = dict()
        current_region_id: int = 0
        for loc, plant in plants.items():
            if loc in regions:
                # this region has already been mapped
                continue
            for coord in map_region(plants, plant, loc):
                regions[coord] = current_region_id
            current_region_id += 1

        # finally return the new grid with plants and regions
        return Grid(
            grid={
                loc: Plot(plant=plant, region_id=regions[loc])
                for loc, plant in plants.items()
            }
        )


def map_region(
    plants: dict[Point, str], want_plant: str, start_plot: Point
) -> list[Point]:
    to_check: list[Point] = [start_plot]
    seen: set[Point] = set(to_check)

    while to_check:
        pos = to_check.pop()
        seen.add(pos)
        for neighbor in orthogonal_neighborhood(pos):
            if (
                neighbor in seen
                or neighbor not in plants
                or plants[neighbor] != want_plant
            ):
                continue
            to_check.append(neighbor)
    return list(seen)


def make_regions(grid: Grid) -> list[set[Point]]:
    """Group points by region"""
    regions: dict[int, set[Point]] = defaultdict(set)
    for pos, plot in grid.grid.items():
        regions[plot.region_id].add(pos)
    return list(plots for plots in regions.values())


def total_price(grid: Grid) -> int:
    total: int = 0
    for plots in make_regions(grid):
        region_area: int = len(plots)
        region_perimeter: int = sum(
            1
            for plot in plots
            for neighbor in orthogonal_neighborhood(plot)
            if neighbor not in grid.grid
            or grid.grid[neighbor].plant != grid.grid[plot].plant
        )
        total += region_area * region_perimeter
    return total


def discounted_price(grid: Grid) -> int:
    total: int = 0

    # count scores for each region
    for original_plots in make_regions(grid):
        sides_count: int = 0

        # The total number of sides for the region is the combination of horizontal
        # sides and vertical sides:
        # - count vertical sides for the unmodified region
        # - count horizontal sides by transposing the region and counting vertical sides
        for plots in [original_plots, set(transpose_points(original_plots))]:
            min_x = min(p.x for p in plots)
            max_x = max(p.x for p in plots)
            min_y = min(p.y for p in plots)
            max_y = max(p.y for p in plots)

            # count only vertical sides
            for direction in [Point.east(), Point.west()]:
                # keep track of sides in a list
                # 0 => no side in this direction
                # 1 => has a side in this direction at this position
                vertical_sides: list[int] = []
                for x in range(min_x, max_x + 1):
                    # insert 0 to avoid accidentally continuing a side to the next row
                    vertical_sides.append(0)
                    for y in range(min_y, max_y + 1):
                        pos = Point(x, y)
                        neighbor = pos + direction
                        vertical_sides.append(
                            0 if pos not in plots or neighbor in plots else 1
                        )

                sides_count += sum(drop_consecutive(vertical_sides))

        total += sides_count * len(plots)

    return total


def drop_consecutive(it: Iterable[int]) -> Iterable[int]:
    """
    Iterate over it, preserving only non-consecutive values.

    For example [0, 1, 1, 1, 0, 1] would become [0, 1, 0, 1], because two consecutive
    1s are dropped.
    """
    prev = None
    for val in it:
        if val != prev:
            yield val
            prev = val


def transpose_points(it: Iterable[Point]) -> Iterable[Point]:
    return (Point(p.y, p.x) for p in it)


if __name__ == "__main__":
    main()
