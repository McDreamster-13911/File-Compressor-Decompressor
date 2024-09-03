import heapq
from bitarray import bitarray

class Tree:
    def __init__(self, character=None, frequency=None, left=None, right=None):
        self.character = character
        self.frequency = frequency
        self.left = left
        self.right = right

    def __lt__(self, other):
        return self.frequency < other.frequency

def build_huffman_tree(binary_data):
    letter_occurrences = {}
    # Convert binary data to bitarray and count frequencies
    bit_data = bitarray()
    bit_data.frombytes(binary_data)

    current_node = 0
    letter_list = []
    while current_node < len(bit_data):
        letter = ""
        # Traverse bit data to reconstruct letters
        while current_node < len(bit_data) and bit_data[current_node] == 1:
            letter += "1"
            current_node += 1
        if letter:
            letter_list.append(letter)
            letter_occurrences[letter] = letter_occurrences.get(letter, 0) + 1
        current_node += 1

    priority_queue = [Tree(letter, count) for letter, count in letter_occurrences.items()]
    heapq.heapify(priority_queue)

    while len(priority_queue) > 1:
        left = heapq.heappop(priority_queue)
        right = heapq.heappop(priority_queue)
        parent = Tree(None, left.frequency + right.frequency, left, right)
        heapq.heappush(priority_queue, parent)

    return heapq.heappop(priority_queue)

def decode(encoded, root):
    decoded = []
    node = root
    for bit in encoded:
        if bit == 0:
            node = node.left
        else:
            node = node.right

        if node is None:
            break

        if node.character:
            decoded.append(str(node.character))
            node = root
    return ''.join(decoded)

def decompress_binary_file(input_file, output_file, tree_root):
    with open(input_file, 'rb') as file:
        compressed_bits = bitarray()
        compressed_bits.fromfile(file)

    decompressed_text = decode(compressed_bits, tree_root)

    with open(output_file, 'w') as file:
        file.write(decompressed_text)
