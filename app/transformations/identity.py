from .transform import Transformation


class Id(Transformation):
    def encode(self, block: bytes) -> bytes:
        return block

    def decode(self, block: bytes) -> bytes:
        return block
