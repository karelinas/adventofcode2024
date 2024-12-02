from sys import stdin

Report = list[int]


def main():
    reports: list[Report] = [
        [int(c) for c in line.strip().split()] for line in stdin if line
    ]
    safe_count: int = sum(int(is_safe(report)) for report in reports)
    print("Part 1:", safe_count)

    safe_count_with_tolerance: int = sum(
        int(is_safe_with_tolerance(report)) for report in reports
    )
    print("Part 2:", safe_count_with_tolerance)


def descends(a: int, b: int) -> bool:
    return a > b


def ascends(a: int, b: int) -> bool:
    return a < b


def gradual(a: int, b: int) -> bool:
    return abs(a - b) <= 3


def is_safe(report: Report) -> bool:
    return all(gradual(a, b) for a, b in zip(report, report[1:])) and (
        all(descends(a, b) for a, b in zip(report, report[1:]))
        or all(ascends(a, b) for a, b in zip(report, report[1:]))
    )


def is_safe_with_tolerance(report: Report) -> bool:
    return any(is_safe(report[0:n] + report[n + 1 :]) for n in range(len(report)))


if __name__ == "__main__":
    main()
