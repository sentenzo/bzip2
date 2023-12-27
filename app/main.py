from transformations.bwt import BWT
from transformations.hfc import HFC
from transformations.mtf import MTF
from transformations.rle import RLE
from transformations.transform import Composition

path = r"./test_file.txt"

BLOCK_SIZE_BYTES = 1024 * 512  # 0.5 Mib


def transform(in_path, out_path, method):
    with open(in_path, "rb") as in_file:
        with open(out_path, "wb") as out_file:
            while block := in_file.read(BLOCK_SIZE_BYTES):
                transformed_block = method(block)
                out_file.write(transformed_block)


if __name__ == "__main__":
    sbzip = Composition(RLE(), BWT(), MTF(), RLE(), HFC())
    in_file = r"./test_file.txt"
    enc_file = r"./test_file.sbzip"
    dec_file = r"./test_file.decoded.txt"

    # import cProfile
    # cProfile.run("transform(in_file , enc_file, sbzip.encode)")
    # cProfile.run("transform(enc_file, dec_file, sbzip.decode)")
    transform(in_file, enc_file, sbzip.encode)
    transform(enc_file, dec_file, sbzip.decode)
