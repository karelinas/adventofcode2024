from collections import defaultdict
from sys import stdin


def main() -> None:
    updates = manual_updates_from_string(stdin.read())
    print("Part 1:", sum_of_correct_updates(updates))


class CustomOrderedItem:
    def __init__(self, lt_list: set[int], value: int) -> None:
        self.lt_list: set[int] = lt_list
        self.value: int = value

    def __lt__(self, other: "CustomOrderedItem") -> bool:
        return other.value in self.lt_list


ManualUpdate = list[CustomOrderedItem]


def manual_updates_from_string(s: str) -> list[ManualUpdate]:
    orderstring, updatestring = s.split("\n\n")

    # build orderlist
    orderlist: dict[int, set[int]] = defaultdict(set)
    for line in orderstring.split("\n"):
        if not line:
            continue
        a, b, *_ = line.strip().split("|")
        orderlist[int(a)].add(int(b))

    updatelist: list[ManualUpdate] = [
        list(
            map(
                lambda x: CustomOrderedItem(orderlist[int(x)], int(x)),
                line.strip().split(","),
            )
        )
        for line in updatestring.split("\n")
        if line
    ]
    return updatelist


def sum_of_correct_updates(updates: list[ManualUpdate]) -> int:
    def lists_equal(lhs: list[CustomOrderedItem], rhs: list[CustomOrderedItem]) -> bool:
        return len(lhs) == len(rhs) and all(
            a.value == b.value for a, b in zip(lhs, rhs)
        )

    total: int = 0
    for u in updates:
        sorted_u = sorted(u)
        if lists_equal(u, sorted_u):
            total += u[len(u) // 2].value

    return total


if __name__ == "__main__":
    main()
