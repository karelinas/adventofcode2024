from collections import defaultdict
from dataclasses import dataclass
from heapq import heappop, heappush
from sys import stdin

from lib import Point, orthogonal_neighborhood


def main() -> None:
    grid = Grid.from_string(stdin.read())
    print("Part 1:", shortest_path_length(grid.simulate(n=1024)))
    block = first_blocking_coordinate(grid)
    print(f"Part 2: {block.x},{block.y}")


@dataclass
class Grid:
    incoming: list[Point]
    walls: set[Point]
    previously_added: Point
    goal: Point = Point(70, 70)

    @staticmethod
    def from_string(data: str) -> "Grid":
        incoming: list[Point] = []
        for line in reversed(data.strip().split("\n")):
            x, y, *_ = line.split(",")
            incoming.append(Point(int(x), int(y)))
        return Grid(incoming=incoming, walls=set(), previously_added=Point(0, 0))

    def simulate(self, n: int = 1) -> "Grid":
        for _ in range(n):
            self.previously_added = self.incoming.pop()
            self.walls.add(self.previously_added)
        return self

    def in_bounds(self, p: Point) -> bool:
        return p.x >= 0 and p.x <= self.goal.x and p.y >= 0 and p.y <= self.goal.y


def shortest_path_length(grid: Grid) -> int:
    return len(shortest_path(grid))


def first_blocking_coordinate(grid: Grid) -> Point:
    path: set[Point] = set()
    while grid.incoming:
        grid.simulate()
        if not path or grid.previously_added in path:
            # only need to recalculate when previously found path was blocked by new
            # wall
            path = shortest_path(grid)
            if grid.goal not in path:
                return grid.previously_added

    raise Exception("No solution")


# cost, position
QueueItem = tuple[int, Point]


def shortest_path(grid: Grid) -> set[Point]:
    """
    Find the best path from start to end.

    It's just a dijktsra with some custom cost stuff.
    """
    start: Point = Point(0, 0)
    end: Point = grid.goal

    # set up djikstra priority queue
    queue: list[QueueItem] = []
    heappush(queue, (0, start))

    # set up cost matrix
    path_costs: dict[Point, int] = defaultdict(lambda: 2**32)
    path_costs[start] = 0

    # keep track of how we got to each node
    prev: dict[Point, Point] = {}

    while queue:
        cost, pos = heappop(queue)
        if pos == end:
            break

        for next_pos in orthogonal_neighborhood(pos):
            if next_pos in grid.walls or not grid.in_bounds(next_pos):
                # this way is blocked
                continue

            cost_to_destination: int = cost + 1
            if cost_to_destination >= path_costs[next_pos]:
                # we've already found a cheaper route to this tile
                continue

            prev[next_pos] = pos
            path_costs[next_pos] = cost_to_destination
            heappush(queue, (cost_to_destination, next_pos))

    current: Point = end
    path: set[Point] = set()
    while current in prev:
        path.add(current)
        current = prev[current]
    return path


if __name__ == "__main__":
    main()
