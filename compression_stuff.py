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

    def build_huffman_tree(self, content):
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

    def build_encoding_map(self, root):
        def dfs(root, code, encoding_map):
            if root.character:
                encoding_map[root.character] = bitarray(code)
            else:
                code.append(False)  # '0' represented as False in bitarray
                dfs(root.left, code, encoding_map)
                code.pop()
                code.append(True)  # '1' represented as True in bitarray
                dfs(root.right, code, encoding_map)
                code.pop()

        encoding_map = {}
        dfs(root, [], encoding_map)
        return encoding_map

    def encode(self, content):
        root = self.build_huffman_tree(content)
        encoding_map = self.build_encoding_map(root)

        encoded_text = bitarray()
        encoded_text.extend([bit for character in content for bit in encoding_map[character]])

        return encoded_text
