from collections import Counter
from operator import itemgetter
from sys import stdin

LocationList = list[tuple[int, int]]


def main():
    unsorted_pairs: LocationList = [
        tuple(map(int, line.strip().split())) for line in stdin if line
    ]
    sorted_pairs: LocationList = [
        (left, right)
        for left, right in zip(
            sorted(map(itemgetter(0), unsorted_pairs)),
            sorted(map(itemgetter(1), unsorted_pairs)),
        )
    ]

    # Part 1
    total_distance: int = sum(abs(left - right) for left, right in sorted_pairs)
    print("Part 1:", total_distance)

    # Part 2
    counts = Counter(map(itemgetter(1), unsorted_pairs))
    similarity_score: int = sum(left * counts[left] for left, _ in unsorted_pairs)
    print("Part 2:", similarity_score)


if __name__ == "__main__":
    main()
