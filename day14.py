import re
from collections import Counter
from dataclasses import dataclass
from math import prod
from sys import stdin
from typing import Optional

from lib import Point

RE_ROBOT = re.compile(r"^p=(\d+),(\d+) v=(-?\d+),(-?\d+)$")


def main() -> None:
    sim = Simulation.from_string(stdin.read())
    print("Part 1:", safety_factor(sim.simulate(100)))


@dataclass
class Robot:
    p: Point
    v: Point

    @staticmethod
    def from_string(data: str) -> "Robot":
        matches = RE_ROBOT.match(data.strip())
        assert matches, "Input must be valid"
        v: list[int] = list(map(int, matches.groups()))
        return Robot(p=Point(v[0], v[1]), v=Point(v[2], v[3]))


@dataclass
class Simulation:
    bots: list[Robot]
    width: int = 101
    height: int = 103

    @staticmethod
    def from_string(data: str) -> "Simulation":
        return Simulation(
            bots=[Robot.from_string(line) for line in data.strip().split("\n") if line]
        )

    def simulate(self, rounds: int) -> "Simulation":
        for bot in self.bots:
            bot.p = (bot.p + bot.v * rounds) % Point(self.width, self.height)
        return self


def safety_factor(sim: Simulation) -> int:
    def quadrant(bot: Robot) -> Optional[int]:
        # Quadrants:
        # 00 | 01
        # ---+---
        # 10 | 11

        # The middle area is no-man's land, part of no quadrant
        mid_x = sim.width // 2
        mid_y = sim.height // 2
        if bot.p.x == mid_x or bot.p.y == mid_y:
            return None

        # Set the bits for quadrants
        return int(bot.p.x > mid_x) | (int(bot.p.y > mid_y) << 1)

    counts = Counter(quadrant(bot) for bot in sim.bots)
    return prod(n for q, n in counts.items() if q is not None)


if __name__ == "__main__":
    main()
