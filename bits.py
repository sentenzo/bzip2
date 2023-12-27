from collections import deque

BYTE_SIZE = 8


class BitArray:
    @staticmethod
    def gen_by_bits(byte, drop_lz=False):
        for pos in range(BYTE_SIZE - 1, -1, -1):
            bit = int(byte & (1 << pos) != 0)
            if bit:
                drop_lz = False
            if not drop_lz:
                yield bit

    @staticmethod
    def gen_bit_stream(chunk_of_bytes, *, drop_last=0):
        total_bit_count = len(chunk_of_bytes) * BYTE_SIZE
        processed_bit_count = 0
        for byte in chunk_of_bytes:
            for bit in BitArray.gen_by_bits(byte):
                yield bit
                processed_bit_count += 1
                if processed_bit_count == total_bit_count - drop_last:
                    break
            if processed_bit_count == total_bit_count - drop_last:
                break

    # @staticmethod
    # def from_bit_iterable(iter):
    #     bit_array = BitArray()
    #     for b in iter:
    #         bit_array.append_bit(int(b))
    #     return bit_array

    def flush_bits(self):
        while len(self.acc_bits) >= 8:
            byte = 0
            for _ in range(8):
                byte <<= 1
                byte += self.acc_bits.popleft()
            byte = byte.to_bytes(1)[0]
            self.bytes.append(byte)

    def __init__(self) -> None:
        self.bytes = []
        self.acc_bits = deque()

    def append_bit(self, bit):
        self.acc_bits.append(bit)
        self.flush_bits()

    def extend_bit(self, bits):
        for bit in bits:
            self.acc_bits.append(int(bit))
        self.flush_bits()

    def append_byte(self, byte):
        for bit in BitArray.gen_by_bits(byte):
            self.acc_bits.append(bit)
        self.flush_bits()

    def append_code(self, code):
        for bit in BitArray.gen_by_bits(code, drop_lz=True):
            self.acc_bits.append(bit)
        self.flush_bits()

    def to_byte_array(self):
        byte_array = self.bytes[:]
        if self.acc_bits:
            last_byte = 0
            for i in range(8):
                last_byte <<= 1
                if i < len(self.acc_bits):
                    last_byte += self.acc_bits[i]
            byte_array.append(last_byte)
        return byte_array

    def __len__(self):
        return len(self.bytes) * BYTE_SIZE + len(self.acc_bits)

    def __iter__(self):
        ...
