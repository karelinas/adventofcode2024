from collections import defaultdict
from sys import stdin

ManualUpdate = list["CustomOrderedItem"]


def main() -> None:
    updates: list[ManualUpdate] = manual_updates_from_string(stdin.read())
    print("Part 1:", sum_of_correct_updates(updates))
    print("Part 2:", sum_of_incorrect_updates(updates))


class CustomOrderedItem:
    def __init__(self, lt_list: set[int], value: int) -> None:
        self.lt_list: set[int] = lt_list
        self.value: int = value

    def __lt__(self, other: "CustomOrderedItem") -> bool:
        return other.value in self.lt_list

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, CustomOrderedItem):
            return NotImplemented
        return self.value == other.value


def manual_updates_from_string(s: str) -> list[ManualUpdate]:
    orderstring, updatestring = s.split("\n\n")

    # build orderlist
    orderlist: dict[int, set[int]] = defaultdict(set)
    for line in orderstring.split("\n"):
        if not line:
            continue
        a, b, *_ = line.strip().split("|")
        orderlist[int(a)].add(int(b))

    # build updatelist
    return [
        list(
            map(
                lambda x: CustomOrderedItem(orderlist[int(x)], int(x)),
                line.strip().split(","),
            )
        )
        for line in updatestring.split("\n")
        if line
    ]


def sum_of_correct_updates(updates: list[ManualUpdate]) -> int:
    total: int = 0
    for u in updates:
        sorted_u = sorted(u)
        if u == sorted_u:
            total += u[len(u) // 2].value

    return total


def sum_of_incorrect_updates(updates: list[ManualUpdate]) -> int:
    total: int = 0
    for u in updates:
        sorted_u = sorted(u)
        if u != sorted_u:
            total += sorted_u[len(sorted_u) // 2].value

    return total


if __name__ == "__main__":
    main()
