from functools import cache
from sys import stdin


def main() -> None:
    patterns, towels = parse_towels(stdin.read())
    print("Part 1:", count_possible_designs(patterns, towels))


def parse_towels(data: str) -> tuple[list[str], frozenset[str]]:
    towelstr, patternstr = data.strip().split("\n\n")

    towels: frozenset[str] = frozenset(t.strip() for t in towelstr.strip().split(","))
    patterns: list[str] = [p.strip() for p in patternstr.strip().split("\n")]
    return patterns, towels


def count_possible_designs(patterns: list[str], towels: frozenset[str]) -> int:
    return sum(1 for p in patterns if is_possible(p, towels))


@cache
def is_possible(pattern: str, towels: frozenset[str]) -> bool:
    return any(
        not pattern
        or (pattern.startswith(t) and is_possible(pattern[len(t) :], towels))
        for t in towels
    )


if __name__ == "__main__":
    main()
