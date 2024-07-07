from collections import namedtuple
from itertools import groupby

from ..transform import Transformation


class RlePackBits(Transformation):
    def encode(self, block: bytes) -> bytes:
        Repeat = namedtuple("Repeat", ["times", "byte"])
        chunks: list[Repeat | list[int]] = []
        # splitting into chunks
        for byte, group in groupby(block):
            count = len(list(group))
            if count > 2:
                chunks.append(Repeat(count, byte))
            else:
                if not chunks or isinstance(chunks[-1], Repeat):
                    chunks.append([])
                chunks[-1].extend([byte] * count)  # type: ignore[union-attr]

        encoded = bytearray()
        # splitting chunks into packages, counting package bytes
        for chunk in chunks:
            if isinstance(chunk, Repeat):
                times, byte = chunk
                while times > 0:
                    counter = min(128, times)
                    times -= counter
                    counter_byte = (-counter).to_bytes(
                        1, signed=True, byteorder="big"
                    )[0]
                    encoded.append(counter_byte)
                    encoded.append(byte)
            elif isinstance(chunk, list):
                total_length = len(chunk)
                for i, byte in enumerate(chunk):
                    if i % 127 == 0:
                        length = min(127, total_length - i)
                        length_byte = length.to_bytes(
                            1, signed=True, byteorder="big"
                        )[0]
                        encoded.append(length_byte)
                    encoded.append(byte)
        return bytes(encoded)

    def decode(self, block: bytes) -> bytes:
        decoded = bytearray()
        next_counter_byte = 0
        repeat = 0
        for byte in block:
            if next_counter_byte == 0:
                counter_int = int.from_bytes(
                    [byte], signed=True, byteorder="big"
                )
                if counter_int > 0:
                    next_counter_byte = counter_int
                else:
                    next_counter_byte = 1
                    repeat = -counter_int
            else:
                next_counter_byte -= 1
                if repeat:
                    decoded.extend([byte] * repeat)
                    repeat = 0
                else:
                    decoded.append(byte)
        return decoded
