from dataclasses import dataclass
from itertools import count, cycle
from sys import stdin
from typing import Iterable

from lib import each_twice


@dataclass
class Bucket:
    file_counts: list[tuple[int, int]]
    empty_blocks: int


@dataclass
class DiskMap:
    bucket_list: list[Bucket]

    @staticmethod
    def from_string(data: str) -> "DiskMap":
        blockdata = [int(ch) for ch in data.strip()]

        bucket_list: list[Bucket] = []
        for block, current_id, is_empty in zip(
            blockdata, each_twice(count()), cycle([False, True])
        ):
            if is_empty:
                bucket_list.append(Bucket(file_counts=[], empty_blocks=block))
            else:
                bucket_list.append(
                    Bucket(file_counts=[(current_id, block)], empty_blocks=0)
                )

        return DiskMap(bucket_list=bucket_list)

    def defrag(self) -> None:
        left = 0
        right = len(self.bucket_list) - 1
        while left != right:
            left_bucket = self.bucket_list[left]
            right_bucket = self.bucket_list[right]

            if left_bucket.empty_blocks == 0:
                left += 1
                continue
            if not right_bucket.file_counts:
                right -= 1
                continue

            # move files from right to left
            last_file_id, last_file_count = right_bucket.file_counts.pop()
            overflow: int = max(0, last_file_count - left_bucket.empty_blocks)
            to_insert: int = last_file_count - overflow
            left_bucket.file_counts.append((last_file_id, to_insert))
            left_bucket.empty_blocks = left_bucket.empty_blocks - to_insert

            # reinsert bits that weren't moved, if any
            if overflow > 0:
                right_bucket.file_counts.append((last_file_id, overflow))


def main() -> None:
    diskmap = DiskMap.from_string(stdin.read())
    print("Part 1:", checksum(diskmap))


def bucket_rle_iter(bucket: Bucket) -> Iterable[int]:
    for file_id, file_count in bucket.file_counts:
        for _ in range(file_count):
            yield file_id


def checksum(diskmap: DiskMap) -> int:
    diskmap.defrag()
    return sum(
        block_number * file_id
        for block_number, file_id in enumerate(
            file_id
            for bucket in diskmap.bucket_list
            for file_id in bucket_rle_iter(bucket)
            if bucket.empty_blocks == 0
        )
    )


if __name__ == "__main__":
    main()
