import pytest

from app.transformations.hfc.bits import BitArray


@pytest.mark.parametrize(
    "byte_str",
    ["00000000", "00000001", "11111111", "00010101"],
)
def test_gen_by_bits(byte_str):
    assert len(byte_str) == 8
    byte_str_drop_lz = bin(int(byte_str, 2))[2:]  # "00101" => "101"

    def reassemble(byte_str, drop_lz):
        byte = int(byte_str, 2)
        bit_list = list(BitArray.gen_by_bits(byte, drop_lz))
        return "".join(map(str, bit_list))

    assert reassemble(byte_str, False) == byte_str
    assert reassemble(byte_str, True) == byte_str_drop_lz
