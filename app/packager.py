DEFAULT_BLOCK_SIZE = 1024 * 512  # 0.5 Mib
CHUNK_SIZE = DEFAULT_BLOCK_SIZE // 8

ENCODED_BLOCK_HEADER_SIZE = 4


class Packager:
    def __init__(self, transformation, block_size=DEFAULT_BLOCK_SIZE) -> None:
        self.transformation = transformation
        self.block_size = block_size

    def gen_split_blocks(self, file_to_encode):
        while block := file_to_encode.read(self.block_size):
            yield block

    def gen_split_encoded_blocks(self, file_to_decode):
        while block_length := file_to_decode.read(ENCODED_BLOCK_HEADER_SIZE):
            block_length = int.from_bytes(block_length, byteorder="big")
            block = file_to_decode.read(block_length)
            yield block

    def apply_encoding(self, in_path, out_path):
        with open(in_path, "rb") as in_file, open(out_path, "wb") as out_file:
            for block in self.gen_split_blocks(in_file):
                transformed_block = self.transformation.encode(block)
                block_length = len(transformed_block)
                block_length = block_length.to_bytes(
                    ENCODED_BLOCK_HEADER_SIZE, byteorder="big"
                )
                out_file.write(block_length)
                out_file.write(transformed_block)

    def apply_decoding(self, in_path, out_path):
        with open(in_path, "rb") as in_file, open(out_path, "wb") as out_file:
            for block in self.gen_split_encoded_blocks(in_file):
                transformed_block = self.transformation.decode(block)
                out_file.write(transformed_block)
