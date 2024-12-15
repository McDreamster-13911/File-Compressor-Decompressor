import heapq
from bitarray import bitarray
import pickle

class Tree:
    def __init__(self, character=None, frequency=None, left=None, right=None):
        self.character = character
        self.frequency = frequency
        self.left = left
        self.right = right

    def __lt__(self, other):
        return self.frequency < other.frequency

def build_huffman_tree(content):
    letter_occurrences = {}
    for letter in content:
        letter_occurrences[letter] = letter_occurrences.get(letter, 0) + 1

    priority_queue = [Tree(letter, count) for letter, count in letter_occurrences.items()]
    heapq.heapify(priority_queue)

    while len(priority_queue) > 1:
        left = heapq.heappop(priority_queue)
        right = heapq.heappop(priority_queue)
        parent = Tree(None, left.frequency + right.frequency, left, right)
        heapq.heappush(priority_queue, parent)

    return heapq.heappop(priority_queue)

def build_encoding_map(root):
    def dfs(node, code, encoding_map):
        if node.character:
            encoding_map[node.character] = code
        else:
            dfs(node.left, code + '0', encoding_map)
            dfs(node.right, code + '1', encoding_map)

    encoding_map = {}
    dfs(root, '', encoding_map)
    return encoding_map

def compress(content):
    root = build_huffman_tree(content)
    encoding_map = build_encoding_map(root)

    encoded_text = bitarray()
    encoded_text.encode({char: bitarray(code) for char, code in encoding_map.items()}, content)

    return encoded_text, root

def compress_file(input_file, output_file):
    with open(input_file, 'r', encoding='utf-8') as file:
        content = file.read()

    compressed_data, huffman_tree = compress(content)

    with open(output_file, 'wb') as file:
        pickle.dump(huffman_tree, file)
        compressed_data.tofile(file)

    original_size = len(content.encode('utf-8'))
    compressed_size = len(compressed_data) / 8 + pickle.dumps(huffman_tree).__sizeof__()
    compression_ratio = (1 - compressed_size / original_size) * 100

    return compression_ratio

