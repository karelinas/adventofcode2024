import re
from sys import stdin

RE_MUL = re.compile(r"mul\((\d+),(\d+)\)")


def prod_line(line: str) -> int:
    return sum(int(m[0]) * int(m[1]) for m in RE_MUL.findall(line))


def main() -> None:
    total: int = sum(prod_line(line) for line in stdin)
    print("Part 1:", total)


if __name__ == "__main__":
    main()
