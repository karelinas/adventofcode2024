from collections import defaultdict
from dataclasses import dataclass
from sys import stdin

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
        filtered_lines: list[str] = [line for line in data.strip().split("\n") if line]

        plants: dict[Point, str] = {
            Point(x, y): plant
            for y, line in enumerate(filtered_lines)
            for x, plant in enumerate(line.strip())
        }
        regions: dict[Point, int] = dict()
        current_region_id: int = 0
        for loc, plant in plants.items():
            if loc in regions:
                # this region has already been mapped
                continue
            for coord in map_region(plants, plant, loc):
                regions[coord] = current_region_id
            current_region_id += 1
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


def make_regions(grid: Grid) -> dict[int, set[Point]]:
    regions: dict[int, set[Point]] = defaultdict(set)
    for pos, plot in grid.grid.items():
        regions[plot.region_id].add(pos)
    return regions


def total_price(grid: Grid) -> int:
    regions: dict[int, set[Point]] = make_regions(grid)
    region_values: list[tuple[int, int]] = []
    for plots in regions.values():
        region_area: int = len(plots)
        region_perimeter: int = sum(
            (
                1
                if neighbor not in grid.grid
                or grid.grid[neighbor].plant != grid.grid[plot].plant
                else 0
            )
            for plot in plots
            for neighbor in orthogonal_neighborhood(plot)
        )
        region_values.append((region_area, region_perimeter))
    return sum(area * perimeter for area, perimeter in region_values)


def discounted_price(grid: Grid) -> int:
    regions: dict[int, set[Point]] = make_regions(grid)
    region_values: list[tuple[int, int]] = []

    for plots in regions.values():
        min_x = min(p.x for p in plots)
        max_x = max(p.x for p in plots)
        min_y = min(p.y for p in plots)
        max_y = max(p.y for p in plots)

        sides_count: int = 0
        # vertical sides
        for direction in [Point.east(), Point.west()]:
            vertical_sides: list[str] = []
            for x in range(min_x - 1, max_x + 2):
                for y in range(min_y - 1, max_y + 2):
                    pos = Point(x, y)
                    if pos not in plots:
                        vertical_sides.append(".")
                        continue
                    neighbor = pos + direction
                    vertical_sides.append("." if neighbor in plots else "#")
            sides_count += sum(1 for s in "".join(vertical_sides).split(".") if s)
        # horizontal sides
        for direction in [Point.north(), Point.south()]:
            horizontal_sides: list[str] = []
            for y in range(min_y - 1, max_y + 2):
                for x in range(min_x - 1, max_x + 2):
                    pos = Point(x, y)
                    if pos not in plots:
                        horizontal_sides.append(".")
                        continue
                    neighbor = pos + direction
                    horizontal_sides.append("." if neighbor in plots else "#")
            sides_count += sum(1 for s in "".join(horizontal_sides).split(".") if s)

        region_values.append((len(plots), sides_count))

    return sum(area * sides for area, sides in region_values)


if __name__ == "__main__":
    main()
