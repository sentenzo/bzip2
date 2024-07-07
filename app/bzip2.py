from app.packager import Packager
from app.transformations import BWT, HFC, MTF, RLE

bzip2 = RLE() >> BWT() >> MTF() >> RLE() >> HFC()


def encode(in_file, out_file):
    packager = Packager(bzip2)
    packager.apply_encoding(in_file, out_file)


def decode(in_file, out_file):
    packager = Packager(bzip2)
    packager.apply_decoding(in_file, out_file)
