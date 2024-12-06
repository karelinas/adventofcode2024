from dataclasses import dataclass
from sys import stdin

from lib import Point, orthogonal_directions

DIRECTION_MAP: dict[str, Point] = {
    "^": Point.north(),
    ">": Point.east(),
    "v": Point.south(),
    "<": Point.west(),
}


@dataclass
class Guard:
    position: Point = Point(0, 0)
    direction: Point = Point(0, 0)


Grid = dict[Point, str]


def main() -> None:
    grid, guard = parse_map(stdin.read())
    print("Part 1:", count_guard_positions(grid, guard))


def parse_map(s: str) -> tuple[Grid, Guard]:
    guard: Guard = Guard()
    grid: Grid = {}

    for y, line in enumerate(s.strip().split("\n")):
        if not line:
            continue
        for x, ch in enumerate(line.strip()):
            if ch in DIRECTION_MAP:
                guard = Guard(Point(x, y), DIRECTION_MAP[ch])
                grid[Point(x, y)] = "."
            else:
                grid[Point(x, y)] = ch

    return grid, guard


def count_guard_positions(grid: Grid, guard: Guard) -> int:
    route: set[Point] = set(simulate_guard_route(grid, guard))
    return len(route)


def simulate_guard_route(grid: Grid, guard: Guard) -> list[Point]:
    assert all(
        grid.get(guard.position + d, None) != "#" for d in orthogonal_directions()
    ), "Illegal map: guard is stuck inside 4 walls"

    route: list[Point] = []
    while guard.position in grid:
        route.append(guard.position)

        # Check for need to turn
        forward_position: Point = guard.position + guard.direction
        while grid.get(forward_position, ".") != ".":
            guard.direction = guard.direction.rotate_right()
            forward_position = guard.position + guard.direction

        guard.position = forward_position

    return route


if __name__ == "__main__":
    main()
