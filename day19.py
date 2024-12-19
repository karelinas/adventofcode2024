from functools import cache
from sys import stdin


def main() -> None:
    patterns, towels = parse_towels(stdin.read())
    print("Part 1:", count_possible_designs(patterns, towels))
    print("Part 2:", count_possible_arrangements(patterns, towels))


def parse_towels(data: str) -> tuple[list[str], frozenset[str]]:
    towelstr, patternstr = data.strip().split("\n\n")

    towels: frozenset[str] = frozenset(t.strip() for t in towelstr.strip().split(","))
    patterns: list[str] = [p.strip() for p in patternstr.strip().split("\n")]
    return patterns, towels


def count_possible_designs(patterns: list[str], towels: frozenset[str]) -> int:
    return sum(1 for p in patterns if count_possible(p, towels) >= 1)


def count_possible_arrangements(patterns: list[str], towels: frozenset[str]) -> int:
    return sum(count_possible(p, towels) for p in patterns)


@cache
def count_possible(pattern: str, towels: frozenset[str]) -> int:
    if not pattern:
        return 1

    return sum(
        count_possible(pattern[len(t) :], towels)
        for t in towels
        if pattern.startswith(t)
    )


if __name__ == "__main__":
    main()
