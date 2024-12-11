from functools import cache


def main() -> None:
    stones: list[int] = [965842, 9159, 3372473, 311, 0, 6, 86213, 48]
    print("Part 1:", blink(stones, n=25))
    print("Part 2:", blink(stones, n=75))


def blink(stones: list[int], *, n: int = 1) -> int:
    return sum(blink_impl(stone, n=n) for stone in stones)


@cache
def blink_impl(stone: int, *, n: int) -> int:
    if n == 0:
        return 1

    # If the stone is engraved with the number 0, it is replaced by a stone
    # engraved with the number 1.
    if stone == 0:
        return blink_impl(1, n=n - 1)
    # If the stone is engraved with a number that has an even number of digits, it
    # is replaced by two stones. The left half of the digits are engraved on the
    # new left stone, and the right half of the digits are engraved on the new
    # right stone. (The new numbers don't keep extra leading zeroes: 1000 would
    # become stones 10 and 0.)
    elif len(stone_string := str(stone)) % 2 == 0:
        mid: int = len(stone_string) // 2
        left_stone: int = int(stone_string[:mid])
        right_stone: int = int(stone_string[mid:])
        return blink_impl(left_stone, n=n - 1) + blink_impl(right_stone, n=n - 1)
    # If none of the other rules apply, the stone is replaced by a new stone; the
    # old stone's number multiplied by 2024 is engraved on the new stone.
    else:
        return blink_impl(stone * 2024, n=n - 1)


if __name__ == "__main__":
    main()
