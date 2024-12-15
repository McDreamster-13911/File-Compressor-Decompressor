from bitarray import bitarray
import pickle

def decode(encoded_data, root):
    decoded = []
    node = root
    for bit in encoded_data:
        if bit:
            node = node.right
        else:
            node = node.left

        if node.character:
            decoded.append(node.character)
            node = root

    return ''.join(decoded)

def decompress_file(input_file, output_file):
    with open(input_file, 'rb') as file:
        huffman_tree = pickle.load(file)
        compressed_data = bitarray()
        compressed_data.fromfile(file)

    decompressed_text = decode(compressed_data, huffman_tree)

    with open(output_file, 'w', encoding='utf-8') as file:
        file.write(decompressed_text)

    return len(decompressed_text)

