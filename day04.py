from sys import stdin

from lib import Point, adjacent_directions

# Used to discard unnecessary characters from the input
RELEVANT_CHARACTERS: set[str] = set("XMAS")


Pattern = list[tuple[Point, str]]


def main() -> None:
    grid = Grid.from_string(stdin.read())
    print("Part 1:", grid.count_occurrences("XMAS"))
    print("Part 2:", grid.count_patterns(make_patterns()))


class Grid:
    def __init__(self, grid: dict[Point, str]) -> None:
        self.grid: dict[Point, str] = grid

    @staticmethod
    def from_string(s: str) -> "Grid":
        lines: list[str] = [line.strip() for line in s.split("\n") if line]
        return Grid(
            {
                Point(x, y): ch
                for y, line in enumerate(lines)
                for x, ch in enumerate(line)
                if ch in RELEVANT_CHARACTERS
            }
        )

    def count_occurrences(self, s: str) -> int:
        return sum(
            self._check_direction(pos, direction, s)
            for pos in self.grid.keys()
            for direction in adjacent_directions()
        )

    def count_patterns(self, patterns: list[Pattern]) -> int:
        return sum(self._count_pattern(pattern) for pattern in patterns)

    def _count_pattern(self, pattern: Pattern) -> int:
        return sum(int(self._match_at_position(p, pattern)) for p in self.grid.keys())

    def _match_at_position(self, position: Point, pattern: Pattern) -> bool:
        return all(
            position + delta in self.grid and self.grid[position + delta] == ch
            for delta, ch in pattern
        )

    def _check_direction(self, position: Point, direction: Point, s: str) -> int:
        if not s:
            return 1

        if position not in self.grid:
            return 0

        if self.grid[position] != s[0]:
            return 0

        return self._check_direction(position + direction, direction, s[1:])


def make_patterns() -> list[Pattern]:
    """
    Make the following pattern and all its rotations:
    M M
     A
    S S
    """
    patterns: list[Pattern] = []

    ur_pattern: Pattern = [
        (Point(-1, -1), "M"),
        (Point(1, -1), "M"),
        (Point(0, 0), "A"),
        (Point(-1, 1), "S"),
        (Point(1, 1), "S"),
    ]
    patterns.append(ur_pattern)

    # Build rotated versions by rotating 90 degrees three times
    # One 90 degree rotation of (x, y) => (-y, x)
    previous_rotation: Pattern = ur_pattern
    for _ in range(3):
        rotated_pattern = []
        for p, ch in previous_rotation:
            rotated_pattern.append((Point(-p.y, p.x), ch))
        patterns.append(rotated_pattern)
        previous_rotation = rotated_pattern

    return patterns


if __name__ == "__main__":
    main()
