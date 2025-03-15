import math
from graphviz import Digraph

def draw_huffman_tree(node, graph=None, parent=None, label=""):
    """ Recursively draw a Huffman tree using Graphviz """
    if graph is None:
        graph = Digraph(format="png")
        graph.attr(dpi="300")  # High resolution

    node_id = str(id(node))  # Unique identifier

    if node.char:  # Leaf node (character)
        graph.node(node_id, f"{node.char}\n({node.freq})", shape="box", style="filled", fillcolor="lightblue")
    else:  # Internal node (frequency sum)
        graph.node(node_id, f"Freq: {node.freq}", shape="circle")

    if parent:
        graph.edge(parent, node_id, label=label)

    if node.left:
        draw_huffman_tree(node.left, graph, node_id, "0")
    if node.right:
        draw_huffman_tree(node.right, graph, node_id, "1")

    return graph

# Improved Huffman Code Table (Better Layout)
def draw_huffman_codes_table(codes, max_rows_per_column=6):
    """ Generate a Graphviz table that organizes Huffman codes into multiple columns neatly. """
    graph = Digraph(format="png")
    graph.attr(dpi="300", rankdir="TB")  # Top to Bottom layout

    # Sort characters by code length for better structure
    sorted_codes = sorted(codes.items(), key=lambda x: len(x[1]))

    # Calculate number of columns needed
    num_cols = math.ceil(len(sorted_codes) / max_rows_per_column)

    # Create a table structure
    graph.node("title", "Huffman Code Table", shape="plaintext", fontsize="20")

    # Create subgraphs for proper column alignment
    columns = [[] for _ in range(num_cols)]

    for i, (char, code) in enumerate(sorted_codes):
        col = i % num_cols  # Distribute across columns
        label = f'"{char}" → {code}'
        node_name = f"code_{i}"
        columns[col].append(node_name)
        graph.node(node_name, label, shape="box", style="filled", fillcolor="lightyellow")

    # Maintain column alignment using invisible edges
    for col in columns:
        for i in range(len(col) - 1):
            graph.edge(col[i], col[i + 1], style="invis")  # Invisible edges for alignment

    return graph