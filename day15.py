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
    raw_input: str = stdin.read()
    sim = Simulation.from_string(raw_input)
    print("Part 1:", sum_of_gps_coordinates(sim.simulate()))
    wide_sim = WideSimulation.from_string(raw_input)
    print("Part 2:", sum_of_gps_coordinates(wide_sim.simulate()))


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


@dataclass
class WideSimulation(Simulation):
    @staticmethod
    def from_string(data: str) -> "WideSimulation":
        sim = Simulation.from_string(data)

        walls: set[Point] = set()
        for w in sim.walls:
            new_p = Point(w.x * 2, w.y)
            walls.add(new_p)
            walls.add(new_p + Point.east())

        return WideSimulation(
            walls=walls,
            boxes={Point(p.x * 2, p.y) for p in sim.boxes},
            robot=Point(sim.robot.x * 2, sim.robot.y),
            moves=sim.moves,
        )

    def simulate(self) -> "WideSimulation":
        for move in self.moves:
            next_pos: Point = self.robot + move
            if self.has_wall(next_pos):
                continue
            if self.has_box(next_pos) and not self.move_boxes(next_pos, move):
                continue
            self.robot = next_pos
        return self

    def has_box(self, pos: Point) -> bool:
        return pos in self.boxes or pos + Point.west() in self.boxes

    def can_move_boxes(self, p: Point, v: Point) -> bool:
        if v.x != 0:
            return self.can_move_boxes_horizontal(p, v)
        return self.can_move_boxes_vertical(p, v)

    def can_move_boxes_horizontal(self, p: Point, v: Point) -> bool:
        if self.has_wall(p + v):
            return False
        if v.x == 1 and self.has_wall(p + v * 2):
            return False

        new_p: Point = p + v * 2
        if new_p in self.boxes:
            return self.can_move_boxes_horizontal(new_p, v)

        return True

    def can_move_boxes_vertical(self, p: Point, v: Point) -> bool:
        if self.has_wall(p + v) or self.has_wall(p + v + Point.east()):
            return False
        new_p = p + v

        # aligned with another box?
        if new_p in self.boxes:
            return self.can_move_boxes_vertical(new_p, v)

        # hitting the edge of another box?
        can_move: bool = True
        east_diagonal: Point = new_p + Point.east()
        west_diagonal: Point = new_p + Point.west()
        if east_diagonal in self.boxes:
            can_move = self.can_move_boxes_vertical(east_diagonal, v)
        if west_diagonal in self.boxes:
            can_move = can_move and self.can_move_boxes_vertical(west_diagonal, v)

        return can_move

    def move_boxes(self, p: Point, v: Point) -> bool:
        if p not in self.boxes:
            p = p + Point.west()
        if p not in self.boxes:
            return True

        next_pos = p + v

        if self.has_wall(next_pos):
            return False

        if not self.can_move_boxes(p, v):
            return False

        if v.x != 0:
            # horizontal movement
            if v.x == 1:
                self.move_boxes(next_pos + v, v)
            else:
                self.move_boxes(next_pos, v)
        else:
            # vertical movement is trickier
            if next_pos in self.boxes:
                self.move_boxes(next_pos, v)
            else:
                east_diagonal: Point = next_pos + Point.east()
                west_diagonal: Point = next_pos + Point.west()
                if east_diagonal in self.boxes:
                    self.move_boxes(east_diagonal, v)
                if west_diagonal in self.boxes:
                    self.move_boxes(west_diagonal, v)

        # move box
        self.boxes.remove(p)
        self.boxes.add(next_pos)
        return True


def sum_of_gps_coordinates(sim: Simulation) -> int:
    return sum(p.x + 100 * p.y for p in sim.boxes)


if __name__ == "__main__":
    main()
