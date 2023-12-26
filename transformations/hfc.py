from .transform import Transformation, Composition
from transformations.rle import RLE
from transformations.bwt import BWT 
from transformations.mtf import MTF
from bits import BitArray
from .hf_tree import HuffmanCanonicalTree

BYTE_SIZE = 8
BYTE_CAPACITY = 2**BYTE_SIZE

TREE_ENCODER = Composition(RLE()) # Composition(RLE(), BWT(), MTF(), RLE())
TREE_HEADER_SIZE = 4


class HFC(Transformation):
    def encode(self, block: bytes) -> bytes:
        h_lengths = HuffmanCanonicalTree.lengths_from_block(block)
        h_tree = HuffmanCanonicalTree(h_lengths)
        encoded_bits = BitArray()

        encoding_table = h_tree.get_encoding_table()
        for byte in block:
            encoded_bits.extend_bit(encoding_table[byte])
        
        last_byte_length = len(encoded_bits) % BYTE_SIZE
        tail_length = 0
        if last_byte_length != 0:
            tail_length = BYTE_SIZE - last_byte_length

        tree_lengths = h_tree.lengths_to_bytes()
        tree_lengths = TREE_ENCODER.encode(tree_lengths)
        tree_lengths_size = len(tree_lengths)
        tree_lengths_size_bytes = tree_lengths_size.to_bytes(TREE_HEADER_SIZE)

        encoded = bytearray()
        encoded.extend(tree_lengths_size_bytes)
        encoded.extend(tree_lengths)
        encoded.extend(encoded_bits.to_byte_array())
        encoded.append(tail_length)
        return bytes(encoded)

    def decode(self, block: bytes) -> bytes:
        tree_lengths_size_bytes = block[:TREE_HEADER_SIZE]
        tree_lengths_size = int.from_bytes(tree_lengths_size_bytes)
        block = block[TREE_HEADER_SIZE:]
        tree_lengths = block[:tree_lengths_size]
        tree_lengths = TREE_ENCODER.decode(tree_lengths)

        tail_length = int.from_bytes([block[-1]])

        block = block[tree_lengths_size:-1]

        h_lengths = HuffmanCanonicalTree.lengths_from_bytes(tree_lengths)
        h_tree = HuffmanCanonicalTree(h_lengths)
        h_trie_root = h_tree.get_trie()
        h_trie_ptr= h_trie_root
        decoded = bytearray()
        for bit in BitArray.gen_bit_stream(block, drop_last=tail_length):
            h_trie_ptr = h_trie_ptr[bit]
            if isinstance(h_trie_ptr, int):
                decoded.append(h_trie_ptr)
                h_trie_ptr = h_trie_root
        return bytes(decoded)

