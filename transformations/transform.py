class Transformation:
    def encode(self, block: bytes) -> bytes:
        ...

    def decode(self, block: bytes) -> bytes:
        ...


class Composition(Transformation):
    def __init__(self, *transformations) -> None:
        self.transformations = transformations

    def encode(self, block: bytes) -> bytes:
        for t in self.transformations:
            block = t.encode(block)
        return block

    def decode(self, block: bytes) -> bytes:
        for t in self.transformations[::-1]:
            block = t.decode(block)
        return block
