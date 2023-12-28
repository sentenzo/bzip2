from ..transform import Transformation

BYTE_CAPACITY = 256  # 2**8


class MTF(Transformation):
    def encode(self, block: bytes) -> bytes:
        dictionary = bytearray(range(BYTE_CAPACITY))
        encoded = bytearray()
        for byte in block:
            index = dictionary.index(byte)
            encoded.append(index)
            dictionary.pop(index)
            dictionary.insert(0, byte)
        return bytes(encoded)

    def decode(self, block: bytes) -> bytes:
        dictionary = bytearray(range(BYTE_CAPACITY))
        decoded = bytearray()
        for index in block:
            byte = dictionary.pop(index)
            decoded.append(byte)
            dictionary.insert(0, byte)
        return decoded
