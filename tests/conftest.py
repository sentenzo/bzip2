import random
import tempfile

import pytest

from tests.helpers import KiB, MiB

DEFAULT_CHUNK_SIZE = 2**15  # 32 KiB

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


def create_random_file(temp_dir, file_size):
    with tempfile.NamedTemporaryFile(dir=temp_dir, delete=False) as temp_file:
        while file_size > 0:
            chunk_size = min(file_size, DEFAULT_CHUNK_SIZE)
            temp_file.write(random.randbytes(chunk_size))
            file_size -= chunk_size
    return temp_file


@pytest.fixture(params=[123, 53 * KiB, MiB * 7 // 11])
def bin_file(temp_dir, request):
    file_size = request.param
    return create_random_file(temp_dir, file_size)


@pytest.fixture(params=[123, 565, 1380, 7 * KiB, 53 * KiB])
def small_bin_file(temp_dir, request):
    file_size = request.param
    return create_random_file(temp_dir, file_size)


@pytest.fixture(params=[409, 15 * KiB, 77 * KiB, 512 * KiB])
def block_size(request):
    return request.param
