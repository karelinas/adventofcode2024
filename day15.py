from dataclasses import dataclass
from sys import stdin
from typing import Optional

from lib import Point

DIRECTION_MAP: dict[str, Point] = {
    "^": Point.north(),
    ">": Point.east(),
    "v": Point.south(),
    "<": Point.west(),
}


def main() -> None:
    sim = Simulation.from_string(stdin.read())
    print("Part 1:", sum_of_gps_coordinates(sim.simulate()))


@dataclass
class Simulation:
    walls: set[Point]
    boxes: set[Point]
    robot: Point
    moves: list[Point]

    @staticmethod
    def from_string(data: str) -> "Simulation":
        str_grid, str_moves, *_ = data.strip().split("\n\n")

        # parse grid
        filtered_grid: list[str] = [
            line for line in str_grid.strip().split("\n") if line
        ]
        walls: set[Point] = set()
        boxes: set[Point] = set()
        robot: Optional[Point] = None
        for y, line in enumerate(filtered_grid):
            for x, ch in enumerate(line.strip()):
                if ch == "@":
                    robot = Point(x, y)
                elif ch == "O":
                    boxes.add(Point(x, y))
                elif ch == "#":
                    walls.add(Point(x, y))
                # other characters are unnecessary

        assert robot, "Input must contain a robot"

        # parse moves
        moves: list[Point] = [
            DIRECTION_MAP[ch] for line in str_moves.strip() for ch in line.strip()
        ]

        return Simulation(walls=walls, boxes=boxes, robot=robot, moves=moves)

    def simulate(self) -> "Simulation":
        for move in self.moves:
            next_pos: Point = self.robot + move
            if self.has_wall(next_pos):
                continue
            if self.has_box(next_pos) and not self.move_boxes(next_pos, move):
                continue
            self.robot = next_pos
        return self

    def has_wall(self, pos: Point) -> bool:
        return pos in self.walls

    def has_box(self, pos: Point) -> bool:
        return pos in self.boxes

    def move_boxes(self, p: Point, v: Point) -> bool:
        next_pos = p + v

        if self.has_wall(next_pos):
            return False

        if self.has_box(next_pos) and not self.move_boxes(next_pos, v):
            return False

        # move box
        self.boxes.remove(p)
        self.boxes.add(next_pos)
        return True


def sum_of_gps_coordinates(sim: Simulation) -> int:
    return sum(p.x + 100 * p.y for p in sim.boxes)


if __name__ == "__main__":
    main()
