from packager import Packager
from transformations import BWT, HFC, MTF, RLE

# BLOCK_SIZE_BYTES = 1024 * 512  # 0.5 Mib
BLOCK_SIZE_BYTES = 1024 * 64  # 0.5 Mib


if __name__ == "__main__":
    in_file = r"./test_file.txt"
    enc_file = r"./test_file.sbzip"
    dec_file = r"./test_file.decoded.txt"

    sbzip = RLE() >> BWT() >> MTF() >> RLE() >> HFC()
    packager = Packager(sbzip)

    packager.apply_encoding(in_file, enc_file)
    packager.apply_decoding(enc_file, dec_file)

    # import cProfile
    # cProfile.run("transform(in_file , enc_file, sbzip.encode)")
    # cProfile.run("transform(enc_file, dec_file, sbzip.decode)")
