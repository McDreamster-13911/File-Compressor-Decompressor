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

def build_huffman_tree(content):
    letter_list = list(content)

    letter_occurrences = {}

    for letter in letter_list:
        letter_occurrences[letter] = letter_occurrences.get(letter, 0) + 1

    priority_queue = [Tree(letter, count) for letter, count in letter_occurrences.items()]

    heapq.heapify(priority_queue)

    while len(priority_queue) > 1:
        left = heapq.heappop(priority_queue)
        right = heapq.heappop(priority_queue)
        parent = Tree(None, left.frequency + right.frequency, left, right)
        heapq.heappush(priority_queue, parent)

    return heapq.heappop(priority_queue)

def decode(encoded, root):
    if root.character:
        return root.character * len(encoded)
    decoded = []
    node = root
    for bit in encoded:
        if bit == 0:  # Modified to compare with integer 0
            node = node.left
        else:
            node = node.right

        # Check if node is None before accessing the character attribute
        if node is None:
            break

        if node.character:
            # Convert the character to a string before appending to the list
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

