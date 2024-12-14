import os
import re
from collections import Counter
from dataclasses import dataclass
from itertools import count
from math import prod
from sys import stdin
from typing import Optional

from lib import Point, neighborhood

RE_ROBOT = re.compile(r"^p=(\d+),(\d+) v=(-?\d+),(-?\d+)$")
IMG_OUT_DIR: str = "out"


def main() -> None:
    sim = Simulation.from_string(stdin.read())

    print("Part 1:", safety_factor(sim.copy().simulate(100)))

    print(f"Saving images to {IMG_OUT_DIR}. Press CTRL-C to stop.")
    if not os.path.isdir(IMG_OUT_DIR):
        os.mkdir(IMG_OUT_DIR)
    try:
        sim.find_christmas_tree()
    except KeyboardInterrupt:
        print("Stopped.")
        print("Browse the generated images manually to find a christmas tree.")
        print("The image filename is the puzzle answer for part 2.")


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

    def simulate(self, rounds: int = 1) -> "Simulation":
        for bot in self.bots:
            bot.p = (bot.p + bot.v * rounds) % Point(self.width, self.height)
        return self

    def copy(self) -> "Simulation":
        return Simulation(
            bots=[Robot(p=bot.p, v=bot.v) for bot in self.bots],
            width=self.width,
            height=self.height,
        )

    def save_simulation(self, filename: str) -> None:
        """Save an image of the simulation to the given file"""
        # Hack: import PIL here to avoid bringing it as a dependency for unit tests
        from PIL import Image

        img = Image.new(mode="RGB", size=(self.width + 1, self.height + 1))
        pixels = img.load()

        locations = Counter(bot.p for bot in self.bots)
        for y in range(self.height + 1):
            for x in range(self.width + 1):
                p = Point(x, y)
                if p in locations:
                    pixels[x, y] = (255, 255, 255)
                else:
                    pixels[x, y] = (0, 0, 0)
        img.save(filename)

    def find_christmas_tree(self) -> None:
        """
        Find christmas trees by:
        1. Saving images of states where most of the bots (>70%) are close to each
           other. This significantly reduces the number of uninteresting states.
        2. Browse manually through the images to find the one that shows a
           christmas tree.

        The manual step was included because to be honest, I had no idea what the
        christmas tree would look like, so I didn't know where to even begin with
        building a heuristic for that. The "vicinity filter" (step 1) filters out
        most of the "uninteresting" states, so manual browsing was pretty fast.

        So let the program run for a while, and then browse through the out/ folder
        for christmas trees. The image file name for the image that shows a
        christmas tree is the puzzle answer.
        """

        def vicinity_percent() -> float:
            """
            Returns the percent of bots that sees another bot in their immediate
            vicinity, including diagonals.
            """
            locations = Counter(bot.p for bot in self.bots)
            bots_close_to_another: int = sum(
                1
                for bot in self.bots
                if any(locations[neighbor] > 0 for neighbor in neighborhood(bot.p))
            )
            return bots_close_to_another / len(self.bots)

        # Keep going until user hits CTRL-C
        for round in count(start=1):
            self.simulate()
            # Save images where a lot of the bots are close to each other
            # This filters out most of the uninteresting states, reducing manual
            # work.
            if vicinity_percent() > 0.7:
                filename: str = f"{IMG_OUT_DIR}/{round:0>6}.png"
                print(f"Saving {filename}")
                self.save_simulation(filename)


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
