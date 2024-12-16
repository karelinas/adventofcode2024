from collections import defaultdict
from dataclasses import dataclass
from heapq import heappop, heappush
from sys import stdin
from typing import Optional

from lib import Point, orthogonal_directions

DEFAULT_HEADING = Point.east()


def main() -> None:
    maze = Maze.from_string(stdin.read())
    print("Part 1:", best_score(maze))
    print("Part 2:", best_path_tiles(maze))


@dataclass
class Maze:
    maze: set[Point]
    start: Point
    end: Point

    @staticmethod
    def from_string(data: str) -> "Maze":
        filtered_lines: list[str] = [line for line in data.strip().split("\n") if line]
        maze: set[Point] = set()
        start: Optional[Point] = None
        end: Optional[Point] = None
        for y, line in enumerate(filtered_lines):
            for x, ch in enumerate(line.strip()):
                p = Point(x, y)
                if ch != "#":
                    maze.add(p)
                if ch == "S":
                    start = p
                elif ch == "E":
                    end = p

        assert start, "Input must include a start point"
        assert end, "Input must include an end point"
        return Maze(maze=maze, start=start, end=end)


def best_score(maze: Maze) -> int:
    costs = build_cost_matrix(maze)
    return costs[maze.end]


def best_path_tiles(maze: Maze) -> int:
    costs = build_cost_matrix(maze)
    path = find_alternative_paths(maze, costs)
    return len(path)


# cost, position, heading
QueueItem = tuple[int, Point, Point]


def build_cost_matrix(maze: Maze) -> dict[Point, int]:
    """
    Find the best path from start to end and return the resulting cost matrix.

    It's just a dijktsra with some custom cost stuff.
    """
    start: Point = maze.start
    end: Point = maze.end

    # set up djikstra priority queue
    queue: list[QueueItem] = []
    heappush(queue, (0, start, DEFAULT_HEADING))

    # set up cost matrix
    path_costs: dict[Point, int] = defaultdict(lambda: 2**32)
    path_costs[start] = 0

    # keep track of how we got to each node
    prev: dict[Point, set[Point]] = defaultdict(set)

    while queue:
        cost, pos, heading = heappop(queue)
        if pos == end:
            break

        for direction in orthogonal_directions():
            if direction == heading.reverse():
                # no backtracking
                continue

            next_pos: Point = pos + direction
            if next_pos not in maze.maze:
                # no wallhacks
                continue

            cost_to_move: int = 1 if direction == heading else 1001
            cost_to_destination: int = cost + cost_to_move
            if cost_to_destination >= path_costs[next_pos]:
                # we've already found a cheaper route to this tile
                continue

            prev[next_pos].add(pos)
            path_costs[next_pos] = cost_to_destination
            heappush(queue, (cost_to_destination, next_pos, direction))

    assert end in prev, "Maze must be solvable"
    return path_costs


def find_alternative_paths(maze: Maze, old_costs: dict[Point, int]) -> set[Point]:
    """
    Finds all equally good alternative paths for a solved maze.

    Also just a dijktsra with some custom cost stuff.
    """
    start: Point = maze.end
    end: Point = maze.start

    # set up djikstra priority queue
    queue: list[QueueItem] = []
    for direction in orthogonal_directions():
        heappush(queue, (0, start, direction))

    # set up cost matrix
    path_costs: dict[Point, int] = defaultdict(lambda: 2**32)
    path_costs[start] = 0

    # keep track of how we got to each node
    prev: dict[Point, set[Point]] = defaultdict(set)

    while queue:
        cost, pos, heading = heappop(queue)
        if pos == end:
            break

        for direction in orthogonal_directions():
            if direction == heading.reverse():
                # no backtracking
                continue

            next_pos: Point = pos + direction
            if next_pos not in maze.maze:
                # no wallhacks
                continue

            cost_to_move: int = 1 if direction == heading else 1001
            cost_to_destination: int = cost + cost_to_move
            if cost_to_destination + old_costs[next_pos] > old_costs[start]:
                # going to next_pos would be more expensive than the optimal route
                continue

            prev[next_pos].add(pos)
            path_costs[next_pos] = cost_to_destination
            heappush(queue, (cost_to_destination, next_pos, direction))

    assert end in prev, "Maze must be solvable"
    return make_paths(prev, end)


def make_paths(prev: dict[Point, set[Point]], tgt: Point) -> set[Point]:
    paths: set[Point] = set()
    to_check: list[Point] = [tgt]
    while to_check:
        current = to_check.pop()
        paths.add(current)
        to_check.extend(prev[current])
    return paths


if __name__ == "__main__":
    main()
