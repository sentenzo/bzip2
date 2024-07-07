import pytest

from app.transformations.hfc.bits import BitArray


@pytest.mark.parametrize(
    "byte_size, byte_str_arr",
    [
        (8, ["00000000", "00000001", "11111111", "00010101"]),
        (4, ["0000", "0001", "1111", "0110", "1010", "0011"]),
        (7, ["0000000", "0000001", "1111111", "1101000", "1001011"]),
        (13, ["0100101110110", "1100110100111", "1000110110000"]),
    ],
)
def test_gen_by_bits(byte_size: int, byte_str_arr: list[str]):
    for byte_str in byte_str_arr:
        assert len(byte_str) == byte_size
        byte_str_drop_lz = bin(int(byte_str, 2))[2:]  # "00101" => "101"

        def reassemble(
            byte_str,
            drop_lz,
            byte_size,
        ):
            byte = int(byte_str, 2)
            bit_list = list(BitArray.gen_by_bits(byte, drop_lz, byte_size))
            return "".join(map(str, bit_list))

        assert reassemble(byte_str, False, byte_size) == byte_str
        assert reassemble(byte_str, True, byte_size) == byte_str_drop_lz


@pytest.mark.parametrize(
    "byte_size, byte_str_arr",
    [
        (8, ["00000000", "00000001", "11111111", "00010101"]),
        (4, ["0000", "0001", "1111", "0110", "1010", "0011"]),
        (7, ["0000000", "0000001", "1111111", "1101000", "1001011"]),
        (13, ["0100101110110", "1100110100111", "1000110110000"]),
    ],
)
def test_gen_bit_stream(byte_size: int, byte_str_arr: list[str]):
    byte_arr = []
    for byte_str in byte_str_arr:
        assert len(byte_str) == byte_size
        byte_arr.append(int(byte_str, 2))

    def get_received(drop_last) -> str:
        bit_list = list(
            BitArray.gen_bit_stream(
                byte_arr, drop_last=drop_last, byte_size=byte_size
            )
        )
        return "".join(map(str, bit_list))

    expected = "".join(byte_str_arr)
    for drop_last in range(4):
        received = get_received(drop_last=drop_last)
        assert expected[: len(expected) - drop_last] == received


@pytest.mark.parametrize(
    "byte_size",
    [3, 4, 7, 8, 13],
)
@pytest.mark.parametrize(
    "bits_str",
    ["000", "1111111111", "01001011101101111111000101011"],
)
def test_append_bit(byte_size, bits_str):
    bits = list(map(int, bits_str))

    barr = BitArray(byte_size)
    for bit in bits:
        barr.append_bit(bit)
    received = "".join(str(bit) for bit in barr)
    assert bits_str == received

    barr = BitArray(byte_size)
    barr.extend_bit(bits)
    received = "".join(str(bit) for bit in barr)
    assert bits_str == received


@pytest.mark.parametrize(
    "byte_size, byte_strs",
    [
        (3, ["110", "000", "001", "011"]),
        (4, ["0110", "0000", "1001", "0111"]),
        (8, ["01100000", "10010111"]),
        (13, ["1100110100111", "0100101110110", "1000110110000"]),
    ],
)
def test_append_byte(byte_size, byte_strs):
    bytes_ = []
    for byte_str in byte_strs:
        assert len(byte_str) == byte_size
        bytes_.append(int(byte_str, 2))

    barr = BitArray(byte_size)
    for byte in bytes_:
        barr.append_byte(byte)

    assert "".join(byte_strs) == "".join(map(str, barr))
    assert bytes_ == barr.to_byte_array()
