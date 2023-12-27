from transformations.bwt import BWT
from transformations.hfc import HFC
from transformations.mtf import MTF
from transformations.rle import RLE
from transformations.transform import Composition
from packager import Packager

# BLOCK_SIZE_BYTES = 1024 * 512  # 0.5 Mib
BLOCK_SIZE_BYTES = 1024 * 64  # 0.5 Mib


if __name__ == "__main__":
    in_file = r"./test_file.txt"
    enc_file = r"./test_file.sbzip"
    dec_file = r"./test_file.decoded.txt"

    sbzip = Composition(RLE(), BWT(), MTF(), RLE(), HFC())
    # sbzip = Composition(BWT())
    packager = Packager(sbzip)

    packager.apply_encoding(in_file, enc_file)
    packager.apply_decoding(enc_file, dec_file)

    # import cProfile
    # cProfile.run("transform(in_file , enc_file, sbzip.encode)")
    # cProfile.run("transform(enc_file, dec_file, sbzip.decode)")
