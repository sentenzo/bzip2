from collections import deque

REAL_BYTE_SIZE = 8
DEFAULT_BYTE_SIZE = REAL_BYTE_SIZE


class BitArray:
    @staticmethod
    def gen_by_bits(
        byte,
        drop_lz: bool = False,
        byte_size: int = DEFAULT_BYTE_SIZE,
    ):
        for pos in range(byte_size - 1, -1, -1):
            bit = int(byte & (1 << pos) != 0)
            if bit:
                drop_lz = False
            if not drop_lz:
                yield bit
        if drop_lz:
            yield 0

    @staticmethod
    def gen_bit_stream(
        chunk_of_bytes: list[int],
        *,
        drop_last=0,
        byte_size: int = DEFAULT_BYTE_SIZE,
    ):
        total_bit_count = len(chunk_of_bytes) * byte_size
        processed_bit_count = 0
        for byte in chunk_of_bytes:
            for bit in BitArray.gen_by_bits(byte, byte_size=byte_size):
                yield bit
                processed_bit_count += 1
                if processed_bit_count == total_bit_count - drop_last:
                    break
            if processed_bit_count == total_bit_count - drop_last:
                break

    def __init__(self, byte_size: int = DEFAULT_BYTE_SIZE) -> None:
        self.byte_size = byte_size
        self.bytes: list[int] = []
        self.acc_bits: deque[int] = deque()

    def flush_bits(self):
        while len(self.acc_bits) >= self.byte_size:
            byte = 0
            for _ in range(self.byte_size):
                byte <<= 1
                byte += self.acc_bits.popleft()
            # byte = byte.to_bytes(1, byteorder="big")[0]
            self.bytes.append(byte)

    def append_bit(self, bit: int):
        self.acc_bits.append(bit)
        self.flush_bits()

    def extend_bit(self, bits: list[int | bool]):
        for bit in bits:
            self.acc_bits.append(int(bit))
        self.flush_bits()

    def append_byte(self, byte: int):
        for bit in BitArray.gen_by_bits(
            byte,
            byte_size=self.byte_size,
        ):
            self.acc_bits.append(bit)
        self.flush_bits()

    def append_code(self, code: int):
        for bit in BitArray.gen_by_bits(
            code, drop_lz=True, byte_size=self.byte_size
        ):
            self.acc_bits.append(bit)
        self.flush_bits()

    def to_byte_array(self):
        byte_array = self.bytes[:]
        if self.acc_bits:
            last_byte = 0
            for i in range(
                self.byte_size
            ):  # [01011] => [01011000] (filing with zeros)
                last_byte <<= 1
                if i < len(self.acc_bits):
                    last_byte += self.acc_bits[i]
            byte_array.append(last_byte)
        return byte_array

    def __len__(self):
        return len(self.bytes) * DEFAULT_BYTE_SIZE + len(self.acc_bits)

    def __iter__(self):
        yield from self.gen_bit_stream(self.bytes, byte_size=self.byte_size)
        yield from self.acc_bits
