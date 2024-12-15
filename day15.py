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

            # Check if there's a wall in the way
            if self.has_wall(next_pos):
                continue

            # If there's a box in our way, try to push it
            box: Optional[Point] = self.get_box_at(next_pos)
            if box and not self.move_boxes(box, move):
                # Pushing the box failed, can't move
                continue

            # We can move!
            self.robot = next_pos

        return self

    def has_wall(self, pos: Point) -> bool:
        return pos in self.walls

    def has_box(self, pos: Point) -> bool:
        return pos in self.boxes

    def get_box_at(self, pos: Point) -> Optional[Point]:
        """Return the box at given position"""
        return pos if pos in self.boxes else None

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
        """
        Make a double-width version of the grid.

        Boxes and walls are now two squares wide.
        All x-coordinates are multiplied by 2.
        """
        sim = Simulation.from_string(data)

        walls: set[Point] = set()
        for w in sim.walls:
            new_p = Point(w.x * 2, w.y)
            walls.add(new_p)
            walls.add(new_p + Point.east())

        return WideSimulation(
            walls=walls,
            boxes=set(Point(p.x * 2, p.y) for p in sim.boxes),
            robot=Point(sim.robot.x * 2, sim.robot.y),
            moves=sim.moves,
        )

    def get_box_at(self, pos: Point) -> Optional[Point]:
        """Return the box at given position, considering double-wide boxes"""
        for p in (pos, pos + Point.west()):
            if p in self.boxes:
                return p
        return None

    @staticmethod
    def future_box(box: Point, v: Point) -> Point:
        """Return where the box will be after moving"""
        return box + v

    @staticmethod
    def wide_box(box: Point) -> tuple[Point, Point]:
        """Return both points belonging to a double-wide box"""
        return (box, box + Point.east())

    def get_collisions(self, box: Point, v: Point) -> set[Point]:
        """List all the collisions caused by box moving by v amount"""
        collisions: set[Point] = set()
        # direct collisions for this box
        for p in WideSimulation.wide_box(WideSimulation.future_box(box, v)):
            if collision := self.get_box_at(p):
                if collision != box:
                    collisions.add(collision)

        # indirect collisions caused by the boxes moved by current box
        indirect_collisions: set[Point] = set(
            coll
            for collided_box in collisions
            for coll in self.get_collisions(collided_box, v)
        )

        return collisions.union(indirect_collisions)

    def can_move(self, box: Point, v: Point) -> bool:
        """
        Return True if box can move by v, otherwise False

        Considers chain movement caused by boxes colliding into each other.
        """
        return all(
            not self.has_wall(p + v)
            for b in self.get_collisions(box, v).union(set([box]))
            for p in WideSimulation.wide_box(b)
        )

    def move_boxes(self, box: Point, v: Point) -> bool:
        """
        Try to move box by v and return True if movement succeeded, otherwise False
        """
        if not self.can_move(box, v):
            return False

        to_add: set[Point] = set()
        for moved_box in self.get_collisions(box, v).union([box]):
            self.boxes.remove(moved_box)
            to_add.add(self.future_box(moved_box, v))
        self.boxes.update(to_add)

        return True


def sum_of_gps_coordinates(sim: Simulation) -> int:
    return sum(p.x + 100 * p.y for p in sim.boxes)


if __name__ == "__main__":
    main()
