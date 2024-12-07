import operator
from sys import stdin
from typing import Callable

Equation = tuple[int, list[int]]
Operator = Callable[[int, int], int]


def main():
    equations = parse_equations(stdin.read())
    print("Part 1:", sum_of_true_equations(equations))
    print("Part 1:", sum_of_true_equations(equations, enable_concat=True))


def parse_equations(data: str) -> list[Equation]:
    def split_line(s: str) -> tuple[int, str]:
        a, b, *_ = s.strip().split(":")
        return int(a), b

    def split_numbers(s: str) -> list[int]:
        return [int(n.strip()) for n in s.split(" ") if n]

    lines: list[tuple[int, str]] = [
        split_line(line) for line in data.strip().split("\n") if line
    ]
    return [(lhs, split_numbers(rhs)) for lhs, rhs in lines]


def sum_of_true_equations(
    equations: list[Equation], *, enable_concat: bool = False
) -> int:
    operators: list[Operator] = [operator.add, operator.mul]
    if enable_concat:
        operators.append(concat_int)

    return sum(
        target_value
        for target_value, numbers in equations
        if check_equation(target_value, numbers[0], numbers[1:], operators)
    )


def check_equation(
    target_value: int,
    intermediate_result: int,
    numbers: list[int],
    operators: list[Operator],
) -> bool:
    if not numbers:
        return target_value == intermediate_result

    return any(
        check_equation(
            target_value, op(intermediate_result, numbers[0]), numbers[1:], operators
        )
        for op in operators
    )


def concat_int(a: int, b: int) -> int:
    return int(str(a) + str(b))


if __name__ == "__main__":
    main()
