import random

import pytest

from app.transformations.hfc.bits import BitArray
from app.transformations.rle.rle_streams import (
    RleStreams,
    _compress_flag_stream,
    _join_streams,
    _slpit_streams,
    _uncompress_flag_stream,
)


@pytest.mark.parametrize(
    "flags_len, symbols_len",
    [
        (13, 49),
        (1997, 48000),
    ],
)
def test_join_slpit_streams(flags_len, symbols_len):
    flags = random.randbytes(flags_len)
    symbols = random.randbytes(symbols_len)

    expected = bytearray(len(flags).to_bytes(4, signed=False, byteorder="big"))
    expected.extend(flags)
    expected.extend(symbols)

    joined = _join_streams(flags, symbols)
    assert joined == expected

    split = _slpit_streams(joined)
    assert split == (flags, symbols)


@pytest.mark.parametrize(
    "flags_len",
    [1, 2, 3, 13, 49, 1997],
)
def test_compress_stream(flags_len):
    flag_stream = random.randbytes(flags_len)
    barr = BitArray()
    [barr.append_byte(byte) for byte in flag_stream]
    flags = list(barr)
    flags = flags[: -random.randint(0, 7)]
    compressed = _compress_flag_stream(flags)
    decompressed = _uncompress_flag_stream(compressed)

    assert flags == decompressed


@pytest.mark.parametrize(
    "bytes_",
    [
        b"aaaaaa",
        b"aaabbcccccccadd",
        random.randbytes(41),
        random.randbytes(314),
        (
            b"cskjhfkjslakjhdfl"
            + b"d" * 27
            + b"lkjhkjhadlkcfj"
            + b"y" * 513
            + b"dksj"
        ),
    ],
)
def test_rle_streams(bytes_):
    rle = RleStreams()
    encoded = rle.encode(bytes_)
    decodeed = rle.decode(encoded)
    assert bytes_ == decodeed
