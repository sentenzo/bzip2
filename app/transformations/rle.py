from collections import namedtuple
from itertools import groupby

from .transform import Transformation

"""
## The PackBits algorithm

You split your initial data into packages:
```python
-128;127
"inqktqigfffffhmkvosynozpgggggggggpcrelizif"
["inqktqig", ("f", 5), "hmkvvosynozp", ("g", 9), "pcrelizzif"]
[8, "inqktqig", -5, "f", 12, "hmkvvosynozp", -9, "g", 10, "pcrelizzif"]
```
The stream of bytes always starts with a **counter byte** `n`. Its value 
can be between `-128` and `127`. It describes the package of the size, 
determined by the `n` value.

- if  `0 <= n <= 127` — the next `n` symbols are not modified
- if `-128 <= n <= -1` — the following byte should be repeated `-n` times
"""


class RLE(Transformation):
    """Run-length encoding"""

    def encode(self, block: bytes) -> bytes:
        Repeat = namedtuple("Repeat", ["times", "byte"])
        chunks = []
        # splitting into chunks
        for byte, goup in groupby(block):
            count = len(list(goup))
            if count > 2:
                chunks.append(Repeat(count, byte))
            else:
                if not chunks or isinstance(chunks[-1], Repeat):
                    chunks.append([])
                chunks[-1].extend([byte] * count)

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
