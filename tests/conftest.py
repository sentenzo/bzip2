import random
import tempfile

import pytest

from tests.helpers import KiB, MiB

DEFAULT_CHUNK_SIZE = 2**15

random.seed(0xDEADBEEF)


@pytest.fixture
def always_true():
    return True


@pytest.fixture(scope="session")
def temp_dir():
    with tempfile.TemporaryDirectory() as temp_dir:
        yield temp_dir


@pytest.fixture(scope="session")
def empty_bin_file(temp_dir):
    with tempfile.NamedTemporaryFile(dir=temp_dir, delete=False) as temp_file:
        pass
    return temp_file


@pytest.fixture
def temp_file(temp_dir):
    with tempfile.NamedTemporaryFile(dir=temp_dir) as temp_file:
        yield temp_file


@pytest.fixture(params=[123, 53 * KiB, MiB * 7 // 11])
def bin_file(temp_dir, request):
    file_size = request.param
    with tempfile.NamedTemporaryFile(dir=temp_dir, delete=False) as temp_file:
        while file_size > 0:
            chunk_size = min(file_size, DEFAULT_CHUNK_SIZE)
            temp_file.write(random.randbytes(chunk_size))
            file_size -= chunk_size
    return temp_file
