import operator
from sys import stdin
from typing import Callable, Optional

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
        operators.append(concatenation)

    return sum(
        target_value
        for target_value, numbers in equations
        if check_equation(numbers, target_value, operators)
    )


def check_equation(
    numbers: list[int],
    target_value: int,
    operators: list[Operator],
    intermediate_result: Optional[int] = None,
) -> bool:
    if not numbers:
        return target_value == intermediate_result

    if intermediate_result is None:
        intermediate_result = numbers[0]
        numbers = numbers[1:]

    return any(
        check_equation(
            numbers[1:], target_value, operators, op(intermediate_result, numbers[0])
        )
        for op in operators
    )


def concatenation(a: int, b: int) -> int:
    return int(str(a) + str(b))


if __name__ == "__main__":
    main()
