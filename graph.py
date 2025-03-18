from graphviz import Digraph

#Drawing Trees
def draw_huffman_tree(node, graph=None, parent=None, label=""):
   
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

# Huffman Code Table
def draw_huffman_codes_table(codes):
    graph = Digraph(format="png")
    graph.attr(dpi="300", rankdir="TB")  # Top to Bottom layout

    # Create an HTML-like table for better formatting
    table_content = """<<TABLE BORDER="1" CELLBORDER="1" CELLSPACING="0">"""
    table_content += """<TR><TD><B>Character</B></TD><TD><B>Huffman Code</B></TD></TR>"""

    for char, code in sorted(codes.items(), key=lambda x: len(x[1])):  # Sort by code length
        char_display = repr(char) if char != " " else "SPACE"
        table_content += f"<TR><TD>{char_display}</TD><TD>{code}</TD></TR>"

    table_content += "</TABLE>>"

    graph.node("table", table_content, shape="plaintext")

    return graph