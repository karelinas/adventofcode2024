from sys import stdin
from typing import Iterable

from lib import Point, orthogonal_neighborhood

Region = set[Point]


def main() -> None:
    regions: list[Region] = parse_regions(stdin.read())
    print("Part 1:", total_price(regions))
    print("Part 2:", discounted_price(regions))


def parse_regions(data: str) -> list[Region]:
    """Parse a grid and find all the regions in it"""
    # remove empty lines from input
    filtered_lines: list[str] = [line for line in data.strip().split("\n") if line]

    # make a simple plant grid
    plants: dict[Point, str] = {
        Point(x, y): plant
        for y, line in enumerate(filtered_lines)
        for x, plant in enumerate(line.strip())
    }

    # find regions in the grid
    regions: list[Region] = []
    used: set[Point] = set()
    for loc in plants.keys():
        if loc in used:
            # this position has already been included in a region
            continue
        region: Region = map_region(plants, loc)
        regions.append(region)
        used.update(region)

    # finally return the new regions
    return regions


def map_region(plants: dict[Point, str], start_plot: Point) -> set[Point]:
    """List the points belonging to the given region"""
    want_plant: str = plants[start_plot]

    to_check: list[Point] = [start_plot]
    region: set[Point] = set(to_check)
    while to_check:
        pos = to_check.pop()
        region.add(pos)
        to_check.extend(
            neighbor
            for neighbor in orthogonal_neighborhood(pos)
            if neighbor not in region and plants.get(neighbor, None) == want_plant
        )

    return region


def total_price(regions: list[Region]) -> int:
    return sum(len(region) * perimeter_length(region) for region in regions)


def discounted_price(regions: list[Region]) -> int:
    return sum(count_sides(region) * len(region) for region in regions)


def perimeter_length(region: Region) -> int:
    return sum(
        1
        for pos in region
        for neighbor in orthogonal_neighborhood(pos)
        if neighbor not in region
    )


def count_sides(region: Region) -> int:
    """Count sides for the given region"""
    # The total number of sides for the region is the combination of horizontal
    # sides and vertical sides
    return count_vertical_sides(region) + count_horizontal_sides(region)


def count_vertical_sides(region: Region) -> int:
    """Count vertical sides for the given region"""
    min_x = min(p.x for p in region)
    max_x = max(p.x for p in region)
    min_y = min(p.y for p in region)
    max_y = max(p.y for p in region)

    side_count: int = 0
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
                neighbor: Point = pos + direction
                has_edge: bool = pos in region and neighbor not in region
                vertical_sides.append(1 if has_edge else 0)
        side_count += sum(drop_consecutive(vertical_sides))

    return side_count


def count_horizontal_sides(region: Region) -> int:
    """Count horizontal sides for the given region"""
    # Count horizontal sides by transposing the region and counting vertical sides
    # This is equivalent to just counting horizontal sides
    transposed_region: Region = set(transpose_points(region))
    return count_vertical_sides(transposed_region)


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
