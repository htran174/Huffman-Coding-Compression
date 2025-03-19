"""
======================================================================================================

                                            backend.py
                                        Created by Hien Tran
                                Holds huffman function to build tree and nodes

======================================================================================================
"""

import heapq
from collections import Counter

#Node class
class Node:
    def __init__(self, freq, char=None, left=None, right=None):
        self.freq = freq
        self.char = char
        self.left = left
        self.right = right

    def __lt__(self, other):  # Needed for heapq
        return self.freq < other.freq

#Build Huffman Tree
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

#Generate Huffman Codes
def create_codes(node, current_code="", codes={}):
    if node.char:  # Leaf node
        codes[node.char] = current_code
        return

    create_codes(node.left, current_code + "0", codes)
    create_codes(node.right, current_code + "1", codes)

    return codes

# Encode & Decode Functions
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


