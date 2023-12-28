from app.packager import Packager

KiB = 1 << 10
MiB = 1 << 20

SMALL_SIZE = 123
MEDIUM_SIZE = 53 * KiB
LARGE_SIZE = MiB * 7 // 11


def apply_encoding_decoding(packager: Packager, in_path: str) -> str:
    en_path = in_path + ".en"
    de_path = en_path + ".de"
    packager.apply_encoding(in_path, en_path)
    packager.apply_decoding(en_path, de_path)
    return de_path
