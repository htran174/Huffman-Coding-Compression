import heapq
from collections import Counter
import graph

# ✅ Node class for Huffman Tree
class Node:
    def __init__(self, freq, char=None, left=None, right=None):
        self.freq = freq
        self.char = char
        self.left = left
        self.right = right

    def __lt__(self, other):  # Needed for heapq
        return self.freq < other.freq

# ✅ Build Huffman Tree
def build_huffman_tree(text):
    frequency = Counter(text)
    heap = [Node(freq, char) for char, freq in frequency.items()]
    heapq.heapify(heap)

    while len(heap) > 1:
        left = heapq.heappop(heap)
        right = heapq.heappop(heap)
        merged = Node(left.freq + right.freq, left=left, right=right)
        heapq.heappush(heap, merged)

    return heap[0]

# ✅ Generate Huffman Codes
def create_codes(node, current_code="", codes={}):
    if node.char:  # Leaf node
        codes[node.char] = current_code
        return

    create_codes(node.left, current_code + "0", codes)
    create_codes(node.right, current_code + "1", codes)

    return codes

# ✅ Encode & Decode Functions
def encode(text, codes):
    return ''.join(codes[char] for char in text)

def decode(encoded_text, codes):
    reverse_codes = {code: char for char, code in codes.items()}
    current_code = ""
    decoded_text = ""

    for bit in encoded_text:
        current_code += bit
        if current_code in reverse_codes:
            decoded_text += reverse_codes[current_code]
            current_code = ""

    return decoded_text


# ✅ Longer text example
text = "Huffman coding is a lossless data compression algorithm. It is used in various applications including file compression formats like ZIP. The algorithm follows a greedy approach by assigning variable-length codes to characters, ensuring optimal encoding efficiency."
print(f"\nOriginal text: {text[:50]}... (truncated for display)")

# ✅ Build Huffman Tree
huffman_root = build_huffman_tree(text)

# ✅ Generate Huffman Codes
huffman_codes = create_codes(huffman_root)
print("\nHuffman Codes Generated:")
for char, code in sorted(huffman_codes.items(), key=lambda x: len(x[1])):  # Sorted by code length
    print(f"{repr(char)}: {code}")  # Use repr() to display special characters properly

# ✅ Encode input text
encoded_str = encode(text, huffman_codes)
print(f"\nEncoded (first 100 bits): {encoded_str[:100]}... (truncated for display)")

# ✅ Decode back
decoded_text = decode(encoded_str, huffman_codes)
print(f"\nDecoded text matches: {text == decoded_text}")

if text == decoded_text:
    print("\nDecoding successful!")
else:
    print("\nDecoding failed! Mismatch detected.")

# ✅ Draw Huffman Tree and Huffman Code Table
tree_graph = graph.draw_huffman_tree(huffman_root)
code_graph = graph.draw_huffman_codes_table(huffman_codes)

tree_graph.render("huffman_tree", view=True)  # Save & open Huffman tree
code_graph.render("huffman_codes", view=True)  # Save & open Huffman codes
