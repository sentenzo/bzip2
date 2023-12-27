import filecmp

import pytest

from app.packager import Packager
from app.transformations import Id
from tests.helpers import KiB, MiB


@pytest.mark.parametrize("block_size", [77 * KiB, 512 * KiB])
def test_apply_encoding_decoding(bin_file, block_size):
    packager = Packager(Id(), block_size)
    in_path = bin_file.name
    en_path = in_path + ".en"
    de_path = en_path + ".de"
    packager.apply_encoding(in_path, en_path)
    packager.apply_decoding(en_path, de_path)
    assert filecmp.cmp(in_path, de_path, shallow=False)
