from itertools import groupby

from app.transformations.hfc.bits import BitArray

from ..transform import Transformation

ACTUAL_BYTE_SIZE = 8
FLAG_BLOCK_SIZE = 4


def _join_streams(flags: bytearray, symbols: bytearray) -> bytearray:
    out_bytes = bytearray()
    flags_length_bytes = len(flags).to_bytes(4, signed=False, byteorder="big")
    out_bytes.extend(flags_length_bytes)
    out_bytes.extend(flags)
    out_bytes.extend(symbols)
    return out_bytes


def _slpit_streams(
    in_bytes: bytes,
) -> tuple[bytes, bytes]:  # FlagStream, SymbolStream
    flags_length = int.from_bytes(in_bytes[:4], signed=False, byteorder="big")
    flag_stream = in_bytes[4 : 4 + flags_length]
    symbol_stream = in_bytes[4 + flags_length :]
    return (flag_stream, symbol_stream)


def _compress_flag_stream(uncompressed_flag_stream: list[int]) -> bytearray:
    bytes_length = len(uncompressed_flag_stream).to_bytes(
        4, signed=False, byteorder="big"
    )
    flag_stream: BitArray = BitArray(FLAG_BLOCK_SIZE)
    max_block_len = 2**FLAG_BLOCK_SIZE - 1
    for flag, group in groupby(uncompressed_flag_stream):
        count = len(list(group))
        if flag == 0:
            while count > 0:
                sub_count = min(count, max_block_len)
                for b in BitArray.gen_by_bits(
                    sub_count, byte_size=FLAG_BLOCK_SIZE
                ):
                    flag_stream.append_bit(b)
                count -= sub_count
        else:  # flag == 1
            flag_stream.extend_bit([0] * FLAG_BLOCK_SIZE * count)

    out_bytes = bytearray(bytes_length)
    out_bytes.extend(
        flag_stream.to_byte_size(ACTUAL_BYTE_SIZE).to_byte_array()
    )
    return out_bytes


def _uncompress_flag_stream(flag_stream: bytes) -> list[int]:
    length = int.from_bytes(flag_stream[:4], signed=False, byteorder="big")
    flag_stream = flag_stream[4:]
    flag_stream_arr: BitArray = BitArray(ACTUAL_BYTE_SIZE)
    for byte in flag_stream:
        flag_stream_arr.append_byte(byte)
    resized = flag_stream_arr.to_byte_size(FLAG_BLOCK_SIZE)
    flags = []
    for block in resized.to_byte_array():
        if block == 0:
            flags.append(1)
        else:
            flags.extend([0] * block)
    return flags[:length]


class RleStreams(Transformation):
    def encode(self, block: bytes) -> bytes:
        unc_flag_stream: list[int] = []
        symbol_stream: bytearray = bytearray()
        for byte, group in groupby(block):
            count = len(list(group))
            if count > 2:
                unc_flag_stream.append(0)
                symbol_stream.append(byte)

                counter_bytes = count.to_bytes(
                    32, signed=False, byteorder="big"
                )
                i = 0
                while counter_bytes[i] == 0:
                    i += 1  # drop leading zeros
                while i < len(counter_bytes):
                    unc_flag_stream.append(1)
                    symbol_stream.append(counter_bytes[i])
                    i += 1
            else:
                for _ in range(count):
                    unc_flag_stream.append(0)
                    symbol_stream.append(byte)
        flag_stream = _compress_flag_stream(unc_flag_stream)
        encoded = _join_streams(flag_stream, symbol_stream)
        return bytes(encoded)

    def decode(self, block: bytes) -> bytes:
        flag_stream, symbol_stream = _slpit_streams(block)
        unc_flag_stream = _uncompress_flag_stream(flag_stream)
        assert len(symbol_stream) == len(unc_flag_stream)
        decoded = bytearray()
        for flag, group in groupby(
            zip(unc_flag_stream, symbol_stream), key=lambda t: t[0]
        ):
            g_bytes = [b for _, b in group]
            if flag == 0:
                decoded.extend(g_bytes)
            else:
                counter = int.from_bytes(
                    g_bytes, signed=False, byteorder="big"
                )
                decoded.extend([decoded[-1]] * (counter - 1))
        return bytes(decoded)
