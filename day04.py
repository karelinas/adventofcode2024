from sys import stdin

from lib import Point, adjacent_directions

RELEVANT_CHARACTERS: set[str] = set("XMAS")


def main() -> None:
    grid = Grid.from_string(stdin.read())
    print("Part 1:", grid.count_occurrences("XMAS"))


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

    def _check_direction(self, position: Point, direction: Point, s: str) -> int:
        if not s:
            return 1

        if position not in self.grid:
            return 0

        if self.grid[position] != s[0]:
            return 0

        return self._check_direction(position + direction, direction, s[1:])


if __name__ == "__main__":
    main()
