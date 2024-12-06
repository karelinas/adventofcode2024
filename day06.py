from dataclasses import dataclass
from sys import stdin

from lib import Point, orthogonal_directions

DIRECTION_MAP: dict[str, Point] = {
    "^": Point.north(),
    ">": Point.east(),
    "v": Point.south(),
    "<": Point.west(),
}


@dataclass(frozen=True)
class Guard:
    position: Point = Point(0, 0)
    direction: Point = Point(0, 0)


Grid = dict[Point, str]


def main() -> None:
    grid, guard = parse_map(stdin.read())
    print("Part 1:", count_guard_positions(grid, guard))
    print("Part 2:", count_looping_configurations(grid, guard))


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
    distinct_route, _ = simulate_guard_route(grid, guard)
    return len(distinct_route)


def simulate_guard_route(grid: Grid, guard: Guard) -> tuple[set[Point], Guard]:
    assert any(
        grid.get(guard.position + d, None) != "#" for d in orthogonal_directions()
    ), "Illegal map: guard is stuck inside 4 walls"

    seen: set[Guard] = set()
    while guard.position in grid:
        if guard in seen:
            # we've been at this location, facing the same way,
            # so we're stuck in a loop
            break
        seen.add(guard)

        # Check for need to turn. Turn as many time as needed.
        forward_position: Point = guard.position + guard.direction
        while grid.get(forward_position, ".") != ".":
            guard = Guard(guard.position, guard.direction.rotate_right())
            forward_position = guard.position + guard.direction

        guard = Guard(forward_position, guard.direction)

    return set(g.position for g in seen), guard


def count_looping_configurations(grid: Grid, guard: Guard) -> int:
    total: int = 0

    # For adding new obstacles, we only need to consider the guard's initial
    # route on the unmodified grid. Any changes outside that route will not
    # change how the guard moves.
    route, _ = simulate_guard_route(grid, guard)

    distinct_route: set[Point] = route - {guard.position}
    for p in distinct_route:
        modified_grid = dict(grid)
        # Add a new obstacle to a modified grid
        modified_grid[p] = "#"
        # And simulate the route on the modified grid
        _, simulated_guard = simulate_guard_route(modified_grid, guard)
        # If the guard is still on the grid, they're stuck in a loop
        if simulated_guard.position in modified_grid:
            total += 1

    return total


if __name__ == "__main__":
    main()
