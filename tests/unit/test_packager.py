import filecmp

import pytest

from app.packager import Packager
from app.transformations import Id


def apply_encoding_decoding(packager: Packager, in_path):
    en_path = in_path + ".en"
    de_path = en_path + ".de"
    packager.apply_encoding(in_path, en_path)
    packager.apply_decoding(en_path, de_path)
    return de_path


def test_apply_encoding_decoding(bin_file, block_size):
    packager = Packager(Id(), block_size)
    in_path = bin_file.name
    de_path = apply_encoding_decoding(packager, in_path)
    assert filecmp.cmp(in_path, de_path, shallow=False)


def test_apply_encoding_decoding_empty(empty_bin_file, block_size):
    packager = Packager(Id(), block_size)
    in_path = empty_bin_file.name
    de_path = apply_encoding_decoding(packager, in_path)
    assert filecmp.cmp(in_path, de_path, shallow=False)
