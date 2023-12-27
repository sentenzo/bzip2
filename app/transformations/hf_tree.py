from collections import defaultdict, namedtuple
from heapq import heapify, heappop, heappush

BYTE_SIZE = 8
BYTE_CAPACITY = 2**BYTE_SIZE


class HuffmanCanonicalTree:
    def __init__(self, lengths):
        self.lengths = lengths
        self.trie = None
        self.encoding_table = None

    @staticmethod
    def lengths_from_block(block: bytes) -> list:
        frequencies = [0] * BYTE_CAPACITY
        for byte in block:
            frequencies[byte] += 1
        Node = namedtuple("Node", ["weight", "values"])
        lengths = [0] * BYTE_CAPACITY
        weight_heap = [Node(w, [b]) for b, w in enumerate(frequencies)]
        heapify(weight_heap)
        while len(weight_heap) > 1:
            w1, vs1 = heappop(weight_heap)
            w2, vs2 = heappop(weight_heap)
            values = vs1
            vs1.extend(vs2)
            weight = w1 + w2
            heappush(weight_heap, Node(weight, values))
            for byte in values:
                lengths[byte] += 1
                assert 0 <= lengths[byte] < 256
        return lengths

    @staticmethod
    def lengths_from_bytes(lengths_bytes: bytes) -> list:
        assert len(lengths_bytes) == BYTE_CAPACITY
        lengths = []
        for byte in lengths_bytes:
            lengths.append(int.from_bytes([byte], byteorder="big"))
        return lengths

    def lengths_to_bytes(self) -> bytes:
        return bytes(self.lengths)

    def get_trie(self):
        if not self.trie:
            Trie = lambda: defaultdict(Trie)
            trie = Trie()
            encoding_table = self.get_encoding_table()
            encoding_table = [(c, b, trie) for b, c in enumerate(encoding_table) if c]
            # encoding_table.sort()
            depth = 0
            while encoding_table:
                next_encoding_table = []  # maybe deque ?
                for code, byte, trie_ptr in encoding_table:
                    code_bit = code[depth]
                    if depth == len(code) - 1:
                        trie_ptr[code_bit] = byte
                        continue
                    trie_ptr = trie_ptr[code_bit]
                    next_encoding_table.append((code, byte, trie_ptr))
                encoding_table = next_encoding_table
                depth += 1
            self.trie = trie
        return self.trie

    def get_encoding_table(self):
        if not self.encoding_table:
            lengths = [(l, b) for b, l in enumerate(self.lengths)]
            lengths.sort()
            encoding_table = [None] * BYTE_CAPACITY
            current_code = -1
            current_length = 0
            for length, byte in lengths:
                if length == 0:
                    continue
                current_code += 1
                while current_length < length:
                    current_code <<= 1
                    current_length += 1
                code_bits = bin(current_code)[2:]
                code_bits = code_bits.zfill(current_length)
                encoding_table[byte] = tuple(int(b) for b in code_bits)
            self.encoding_table = encoding_table
        return self.encoding_table
