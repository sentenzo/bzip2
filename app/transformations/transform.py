class Transformation:
    def encode(self, block: bytes) -> bytes:
        ...

    def decode(self, block: bytes) -> bytes:
        ...

    def __rshift__(self, obj):
        left_transformations = []
        right_transformations = []
        if isinstance(self, Composition):
            left_transformations = list(self.transformations)
        elif isinstance(self, Transformation):
            left_transformations = [self]
        if isinstance(obj, Composition):
            right_transformations = list(obj.transformations)
        elif isinstance(obj, Transformation):
            right_transformations = [obj]
        transformations = left_transformations + right_transformations
        return Composition(*transformations)


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
