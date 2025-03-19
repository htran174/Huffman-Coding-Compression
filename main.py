import tkinter as tk
from tkinter import filedialog, messagebox, ttk
import os
import threading
import time
from bitarray import bitarray
import backend
import graph

def select_file():
    """Allow the user to select a .txt file."""
    file = filedialog.askopenfilename(title="Select a Text File", filetypes=[("Text Files", "*.txt")])
    file_path.set(file)

def compress_file():
    """Start compression with progress bar."""
    if not file_path.get():
        messagebox.showwarning("Warning", "Please select a file first.")
        return
    
    progress_bar["value"] = 0
    progress_label.config(text="Compressing...")
    threading.Thread(target=run_compression, daemon=True).start()

def run_compression():
    global huffman_root, huffman_codes
    
    with open(file_path.get(), 'r', encoding='utf-8') as f:
        text = f.read()
    
    original_size = os.path.getsize(file_path.get())
    
    huffman_root = backend.build_huffman_tree(text)
    huffman_codes = backend.create_codes(huffman_root)
    encoded_text = backend.encode(text, huffman_codes)
    
    print(encoded_text)
    bit_arr = bitarray(encoded_text)
    
    with open("compress.bin", "wb") as f:
        bit_arr.tofile(f)
    
    compressed_size = os.path.getsize("compress.bin")
    
    for i in range(101):  # Simulate progress
        time.sleep(0.03)
        progress_bar["value"] = i
        progress_label.config(text=f"Progress: {i}%")
        root.update_idletasks()

    # Compute compression ratio
    compression_ratio = (100- (compressed_size / original_size) * 100)
    
    # Show results in a new window
    result_window = tk.Toplevel(root)
    result_window.title("Compression Statistics")
    result_window.geometry("300x150")
    
    tk.Label(result_window, text=f"Original File Size: {original_size} bytes").pack(pady=5)
    tk.Label(result_window, text=f"Compressed File Size: {compressed_size} bytes").pack(pady=5)
    tk.Label(result_window, text=f"Compression Ratio: {compression_ratio:.2f}%").pack(pady=5)
    
    messagebox.showinfo("Success", "File compressed successfully!")
    progress_label.config(text="Compression Complete")

def decompress_file():
    """Start decompression with progress bar."""
    progress_bar["value"] = 0
    progress_label.config(text="Decompressing...")
    threading.Thread(target=run_decompression, daemon=True).start()

def run_decompression():
    try:
        with open("compress.bin", "rb") as f:
            bit_arr = bitarray()
            bit_arr.fromfile(f)
        
        encoded_text = bit_arr.to01()
        
        with open(file_path.get(), 'r', encoding='utf-8') as f:
            text = f.read()
        huffman_root = backend.build_huffman_tree(text)
        huffman_codes = backend.create_codes(huffman_root)
        
        decoded_text = backend.decode(encoded_text, huffman_codes)
        
        decompressed_file_path = "decompress.txt"
        with open(decompressed_file_path, "w", encoding='utf-8') as f:
            f.write(decoded_text)
        
        for i in range(101):  # Simulate progress
            time.sleep(0.03)
            progress_bar["value"] = i
            progress_label.config(text=f"Progress: {i}%")   
            root.update_idletasks()
        
        with open(file_path.get(), "r", encoding="utf-8") as original_f:
            original_text = original_f.read()
        
        if original_text == decoded_text:
            messagebox.showinfo("Success", "Decompressed file matches the original input file!\nAnd is in decompress.txt")
        else:
            messagebox.showwarning("Mismatch", "Decompressed file does NOT match the original input file!")
        
        progress_label.config(text="Decompression Complete")
        
    except Exception as e:
        messagebox.showerror("Error", f"An error occurred: {str(e)}")

def show_huffman_tree():
    """Generate and display the Huffman tree."""
    if huffman_root:
        tree_graph = graph.draw_huffman_tree(huffman_root)
        tree_graph.render("huffman_tree", view=True)
    else:
        messagebox.showwarning("Warning", "No Huffman tree available. Compress a file first.")

def show_huffman_table():
    """Generate and display the Huffman code table."""
    if huffman_codes:
        code_graph = graph.draw_huffman_codes_table(huffman_codes)
        code_graph.render("huffman_codes", view=True)
    else:
        messagebox.showwarning("Warning", "No Huffman code table available. Compress a file first.")

if __name__ == "__main__":
    #color
    black = "#000000"    # Black text
    white = "#FFFFFF"  # White text
    dark_gray = "#2E2E2E"  # Dark gray

    # Create the main window
    root = tk.Tk()
    root.title("Huffman Compression GUI")
    root.geometry("450x400")

    root.configure(bg=dark_gray)

    file_path = tk.StringVar()
    huffman_root = None
    huffman_codes = None

    # File selection button
    select_button = tk.Button(root, text="Select File", command=select_file, bg=dark_gray)
    select_button.pack(pady=10)

    # Display selected file path
    file_label = tk.Label(root, textvariable=file_path, wraplength=400 , bg= dark_gray, fg= white)
    file_label.pack(pady=5)

    # Progress bar and label
    progress_label = tk.Label(root, text="", bg= dark_gray, fg= white)
    progress_label.pack(pady=5)

    style = ttk.Style()
    style.theme_use("default")
    style.configure("TProgressbar", background="#777777", troughcolor=dark_gray, bordercolor=black, lightcolor=black, darkcolor=black)

    progress_bar = ttk.Progressbar(root, style="TProgressbar", mode="determinate", length=300, maximum=100)
    progress_bar.pack(pady=10)

    # Compress button
    compress_button = tk.Button(root, text="Compress", command=compress_file)
    compress_button.pack(pady=10)

     # Show Huffman tree button
    tree_button = tk.Button(root, text="Show Huffman Tree", command=show_huffman_tree)
    tree_button.pack(pady=10)

    # Show Huffman table button
    table_button = tk.Button(root, text="Show Huffman Table", command=show_huffman_table)
    table_button.pack(pady=10)

    # Decompress button
    decompress_button = tk.Button(root, text="Decompress", command=decompress_file)
    decompress_button.pack(pady=10)

    # Run the GUI
    root.mainloop()