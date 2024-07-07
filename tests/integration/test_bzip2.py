import filecmp

import pytest

from app.packager import Packager
from app.transformations import (
    BWT,
    HFC,
    MTF,
    Id,
    RlePackBits,
    RlePairs,
    RleStreams,
)

from ..helpers import apply_encoding_decoding


@pytest.mark.parametrize(
    "Algorithm",
    [BWT, HFC, MTF, RlePackBits, RlePairs, RleStreams, Id],
)
def test_singular_encoding(bin_file, block_size, Algorithm):
    algorithm = Algorithm()
    packager = Packager(algorithm, block_size)
    in_path = bin_file.name
    de_path = apply_encoding_decoding(packager, in_path)
    assert filecmp.cmp(in_path, de_path, shallow=False)


@pytest.mark.slow
@pytest.mark.parametrize(
    "Algorithm",
    [BWT, HFC, MTF, RlePackBits, RlePairs, RleStreams, Id],
)
def test_repetative_encoding(small_bin_file, block_size, Algorithm):
    repetative_algorithm = Algorithm() >> Algorithm() >> Algorithm()
    packager = Packager(repetative_algorithm, block_size)
    in_path = small_bin_file.name
    de_path = apply_encoding_decoding(packager, in_path)
    assert filecmp.cmp(in_path, de_path, shallow=False)


def test_bzip2(small_bin_file, block_size):
    bzip2 = RlePackBits() >> BWT() >> MTF() >> RlePackBits() >> HFC()
    packager = Packager(bzip2, block_size)
    in_path = small_bin_file.name
    de_path = apply_encoding_decoding(packager, in_path)
    assert filecmp.cmp(in_path, de_path, shallow=False)
