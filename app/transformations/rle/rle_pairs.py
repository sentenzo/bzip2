from itertools import groupby

from ..transform import Transformation


class RlePairs(Transformation):
    """Run-length encoding"""

    def encode(self, block: bytes) -> bytes:
        encoded: bytearray = bytearray()
        for byte, group in groupby(block):
            count = len(list(group))
            if count > 1:
                while count > 1:
                    encoded.append(byte)
                    encoded.append(byte)
                    cur_count = min(count, 255)
                    counter_byte = cur_count.to_bytes(
                        1, signed=False, byteorder="big"
                    )[0]
                    encoded.append(counter_byte)
                    count -= cur_count
                if count == 1:
                    encoded.append(byte)
            else:
                encoded.append(byte)
        return bytes(encoded)

    def decode(self, block: bytes) -> bytes:
        decoded = bytearray()
        prev_byte: int | None = None
        next_will_be_counter = False
        for byte in block:
            if byte == prev_byte:
                prev_byte = None
                next_will_be_counter = True
            elif next_will_be_counter:
                next_will_be_counter = False
                counter = int.from_bytes([byte], signed=False, byteorder="big")
                decoded.extend([decoded[-1]] * (counter - 1))
            else:
                prev_byte = byte
                decoded.append(byte)
        return bytes(decoded)
