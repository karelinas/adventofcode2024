import re
from dataclasses import dataclass
from sys import stdin

from lib import Point

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


def main() -> None:
    machines: list[Machine] = parse_machines(stdin.read())
    print("Part 1:", best_total_tokens(machines))
    print("Part 2:", best_total_tokens(fix_conversion_error(machines)))


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


def fix_conversion_error(machines: list[Machine]) -> list[Machine]:
    return [
        Machine(
            button_a=m.button_a,
            button_b=m.button_b,
            prize=m.prize + Point(10000000000000, 10000000000000),
        )
        for m in machines
    ]


def best_total_tokens(machines: list[Machine]) -> int:
    return sum(least_tokens_for_machine(machine) for machine in machines)


def least_tokens_for_machine(machine: Machine) -> int:
    """MATHS!"""
    # the principle here is that we have a two-equation system
    #
    #   n * Ax + m * Bx = X
    #   n * Ay + m * By = Y
    #
    # Where
    #        n = number of A button presses
    #        m = number of B button presses
    #   Ax, Ay = x, y for button A
    #   Bx, By = x, y for button B
    #     X, Y = x, y for prize
    #
    # solving for n and m gives:
    #
    #   n = (X - m * Bx) / Ax
    #   m = (Ax * Y - Ay * X) / (Ax * By - Bx * Ay)

    Ax, Ay = machine.button_a.as_tuple()
    Bx, By = machine.button_b.as_tuple()
    X, Y = machine.prize.as_tuple()

    # solve m
    if (Ax * Y - Ay * X) % (Ax * By - Bx * Ay) != 0:
        # no integer solution
        return 0
    m: int = (Ax * Y - Ay * X) // (Ax * By - Bx * Ay)

    # solve n
    if (X - m * Bx) % Ax != 0:
        # no integer solution
        return 0
    n: int = (X - m * Bx) // Ax

    return n * 3 + m


if __name__ == "__main__":
    main()
