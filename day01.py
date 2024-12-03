from collections import Counter
from operator import itemgetter
from sys import stdin

LocationList = list[tuple[int, int]]


def main() -> None:
    unsorted_pairs: LocationList = parse_pairs(stdin.read())

    # Part 1
    print("Part 1:", total_distance(unsorted_pairs))

    # Part 2
    print("Part 2:", similarity_score(unsorted_pairs))


def parse_pairs(s: str) -> LocationList:
    def parse_line(line: str) -> tuple[int, int]:
        a, b, *_ = tuple(map(int, line.strip().split()))
        return a, b

    return [parse_line(line) for line in s.split("\n") if line]


def total_distance(pairs: LocationList) -> int:
    sorted_pairs: LocationList = [
        (left, right)
        for left, right in zip(
            sorted(map(itemgetter(0), pairs)),
            sorted(map(itemgetter(1), pairs)),
        )
    ]
    return sum(abs(left - right) for left, right in sorted_pairs)


def similarity_score(pairs: LocationList) -> int:
    counts = Counter(map(itemgetter(1), pairs))
    return sum(left * counts[left] for left, _ in pairs)


if __name__ == "__main__":
    main()
