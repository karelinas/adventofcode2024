from collections import defaultdict
from dataclasses import dataclass
from sys import stdin

from lib import Point, orthogonal_neighborhood


def main() -> None:
    grid = Grid.from_string(stdin.read())
    print("Part 1:", total_price(grid))


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


def total_price(grid: Grid) -> int:
    regions: dict[int, list[Point]] = defaultdict(list)
    for pos, plot in grid.grid.items():
        regions[plot.region_id].append(pos)
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


if __name__ == "__main__":
    main()
