from lib import repeat_call


def main() -> None:
    stones: list[int] = [965842, 9159, 3372473, 311, 0, 6, 86213, 48]
    print("Part 1:", len(blink(stones, n=25)))


def blink(stones: list[int], *, n: int = 1) -> list[int]:
    return repeat_call(blink_impl, stones, n=n)


def blink_impl(stones: list[int]) -> list[int]:
    next_stones: list[int] = []

    # As you observe them for a while, you find that the stones have a consistent
    # behavior. Every time you blink, the stones each simultaneously change according
    # to the first applicable rule in this list:
    for stone in stones:
        # If the stone is engraved with the number 0, it is replaced by a stone
        # engraved with the number 1.
        if stone == 0:
            next_stones.append(1)
        # If the stone is engraved with a number that has an even number of digits, it
        # is replaced by two stones. The left half of the digits are engraved on the
        # new left stone, and the right half of the digits are engraved on the new
        # right stone. (The new numbers don't keep extra leading zeroes: 1000 would
        # become stones 10 and 0.)
        elif len(stone_string := str(stone)) % 2 == 0:
            mid: int = len(stone_string) // 2
            next_stones.append(int(stone_string[:mid]))
            next_stones.append(int(stone_string[mid:]))
        # If none of the other rules apply, the stone is replaced by a new stone; the
        # old stone's number multiplied by 2024 is engraved on the new stone.
        else:
            next_stones.append(stone * 2024)

    return next_stones


if __name__ == "__main__":
    main()
