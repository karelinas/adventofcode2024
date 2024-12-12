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
    for plots in make_regions(grid):
        min_x = min(p.x for p in plots)
        max_x = max(p.x for p in plots)
        min_y = min(p.y for p in plots)
        max_y = max(p.y for p in plots)

        sides_count: int = 0
        # count vertical sides
        for direction in [Point.east(), Point.west()]:
            vertical_sides: list[int] = []
            for x in range(min_x, max_x + 1):
                vertical_sides.append(0)
                for y in range(min_y, max_y + 1):
                    pos = Point(x, y)
                    neighbor = pos + direction
                    vertical_sides.append(
                        0 if pos not in plots or neighbor in plots else 1
                    )
            sides_count += sum(drop_consecutive(vertical_sides))
        # count horizontal sides
        for direction in [Point.north(), Point.south()]:
            horizontal_sides: list[int] = []
            for y in range(min_y, max_y + 1):
                horizontal_sides.append(0)
                for x in range(min_x, max_x + 1):
                    pos = Point(x, y)
                    if pos not in plots:
                        horizontal_sides.append(0)
                        continue
                    neighbor = pos + direction
                    horizontal_sides.append(
                        0 if pos not in plots or neighbor in plots else 1
                    )
            sides_count += sum(drop_consecutive(horizontal_sides))
        total += sides_count * len(plots)

    return total


def drop_consecutive(it: Iterable[int]) -> Iterable[int]:
    prev = None
    for val in it:
        if val != prev:
            yield val
            prev = val


if __name__ == "__main__":
    main()
