import filecmp

from bzip2 import decode, encode

if __name__ == "__main__":
    in_file = r"./Tolstoy Leo - War and Peace.txt"
    enc_file = in_file + ".enc"
    dec_file = enc_file + ".dec"

    encode(in_file, enc_file)
    decode(enc_file, dec_file)

    # checking if the files are identical
    assert filecmp.cmp(in_file, dec_file, shallow=False)

    # import cProfile
    # cProfile.run("transform(in_file , enc_file, sbzip.encode)")
    # cProfile.run("transform(enc_file, dec_file, sbzip.decode)")
