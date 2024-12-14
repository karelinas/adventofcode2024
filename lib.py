from dataclasses import dataclass
from typing import Callable, Iterable, TypeVar

T = TypeVar("T")


@dataclass(eq=True, frozen=True)
class Point:
    x: int
    y: int

    def __add__(self, rhs: "Point") -> "Point":
        return Point(x=self.x + rhs.x, y=self.y + rhs.y)

    def __sub__(self, rhs: "Point") -> "Point":
        return Point(x=self.x - rhs.x, y=self.y - rhs.y)

    def __mul__(self, rhs: int) -> "Point":
        return Point(x=self.x * rhs, y=self.y * rhs)

    def __lt__(self, rhs: "Point") -> bool:
        return (self.x, self.y) < (rhs.x, rhs.y)

    def __mod__(self, rhs: "Point") -> "Point":
        return Point(self.x % rhs.x, self.y % rhs.y)

    def as_tuple(self) -> tuple[int, int]:
        return (self.x, self.y)

    def reverse(self) -> "Point":
        return Point(-self.x, -self.y)

    def rotate_right(self) -> "Point":
        return Point(-self.y, self.x)

    @staticmethod
    def north() -> "Point":
        return Point(0, -1)

    @staticmethod
    def south() -> "Point":
        return Point(0, 1)

    @staticmethod
    def west() -> "Point":
        return Point(-1, 0)

    @staticmethod
    def east() -> "Point":
        return Point(1, 0)

    @staticmethod
    def northwest() -> "Point":
        return Point(-1, -1)

    @staticmethod
    def northeast() -> "Point":
        return Point(1, -1)

    @staticmethod
    def southwest() -> "Point":
        return Point(-1, 1)

    @staticmethod
    def southeast() -> "Point":
        return Point(1, 1)


def adjacent_directions() -> list[Point]:
    return [
        Point.northwest(),
        Point.north(),
        Point.northeast(),
        Point.west(),
        Point.east(),
        Point.southwest(),
        Point.south(),
        Point.southeast(),
    ]


def neighborhood(p: Point) -> Iterable[Point]:
    return (p + d for d in adjacent_directions())


def orthogonal_directions() -> list[Point]:
    return [
        Point.north(),
        Point.west(),
        Point.east(),
        Point.south(),
    ]


def orthogonal_neighborhood(p: Point) -> Iterable[Point]:
    return (p + d for d in orthogonal_directions())


def manhattan_distance(p1: Point, p2: Point) -> int:
    return abs(p1.x - p2.x) + abs(p1.y - p2.y)


def transpose(lst: Iterable[Iterable[T]]) -> list[tuple[T, ...]]:
    return list(zip(*lst))


def each_twice(lst: Iterable[T]) -> Iterable[T]:
    for item in lst:
        yield item
        yield item


def repeat_call(fn: Callable[[T], T], arg: T, *, n) -> T:
    rv: T = arg
    for _ in range(n):
        rv = fn(rv)
    return rv
