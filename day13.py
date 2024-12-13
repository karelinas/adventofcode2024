import re
from dataclasses import dataclass
from itertools import product
from sys import stdin

from lib import Point

MAX_TOKENS: int = 100

RE_MACHINE = re.compile(
    r"^Button A: X\+(\d+), Y\+(\d+)\n"
    r"Button B: X\+(\d+), Y\+(\d+)\n"
    r"Prize: X=(\d+), Y=(\d+)$",
    re.MULTILINE,
)


@dataclass
class Machine:
    button_a: Point
    button_b: Point
    prize: Point


MACHINE = """
Button A: X+94, Y+34
Button B: X+22, Y+67
Prize: X=8400, Y=5400
""".strip()


def main() -> None:
    machines: list[Machine] = parse_machines(stdin.read())
    print("Part 1:", best_total_tokens(machines))


def parse_machine(data: str) -> Machine:
    matches = RE_MACHINE.match(data)
    assert matches, "Input must be valid"

    numbers: list[int] = list(map(int, matches.groups()))
    return Machine(
        button_a=Point(numbers[0], numbers[1]),
        button_b=Point(numbers[2], numbers[3]),
        prize=Point(numbers[4], numbers[5]),
    )


def parse_machines(data: str) -> list[Machine]:
    return [
        parse_machine(machine_str)
        for machine_str in data.strip().split("\n\n")
        if machine_str
    ]


def best_total_tokens(machines: list[Machine]) -> int:
    return sum(least_tokens_for_machine(machine) for machine in machines)


def least_tokens_for_machine(machine: Machine) -> int:
    return min(
        (
            3 * a + b
            for a, b in product(range(MAX_TOKENS), range(MAX_TOKENS))
            if machine.button_a * a + machine.button_b * b == machine.prize
        ),
        default=0,
    )


if __name__ == "__main__":
    main()
