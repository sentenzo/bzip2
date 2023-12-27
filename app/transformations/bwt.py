from __future__ import annotations

from functools import cmp_to_key

from .transform import Transformation

ORIGIN_PTR_SIZE = 4


class BWT(Transformation):
    def encode(self, block: bytes) -> bytes:
        block_size = len(block)
        rotations = list(range(block_size))

        class ComparableRotation:
            def __init__(self, shift) -> None:
                self.shift = shift

            def __getitem__(self, index):
                return block[(index + self.shift) % block_size]

            def __lt__(self, other: ComparableRotation):
                for i in range(block_size):
                    if self[i] < other[i]:
                        return True
                    elif self[i] > other[i]:
                        return False
                    elif self[i] == other[i]:
                        continue
                return False

        def slice_key(rot):
            return ComparableRotation(rot)

        rotations.sort(key=slice_key)

        origin_ptr = rotations.index(0)
        origin_ptr_bytes = origin_ptr.to_bytes(
            ORIGIN_PTR_SIZE, byteorder="big"
        )
        encoded = bytearray(origin_ptr_bytes)
        for rot in rotations:
            encoded.append(block[rot - 1])
        return bytes(encoded)

    def decode(self, block: bytes) -> bytes:
        origin_ptr = int.from_bytes(block[:ORIGIN_PTR_SIZE], byteorder="big")
        block = block[ORIGIN_PTR_SIZE:]
        block_size = len(block)
        decoded = [None] * block_size

        transmissions = list(range(block_size))
        transmissions.sort(key=lambda i: block[i])
        cur = origin_ptr
        for i in range(block_size):
            cur = transmissions[cur]
            decoded[i] = block[cur]
        return bytes(decoded)
