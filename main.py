import tkinter as tk
from tkinter import filedialog, messagebox
import pdfresizer_backend as myWorkflow  # Import the backend module

# TODO: make this GUI look actually nice.

def select_pdf():
    pdf_path.set(filedialog.askopenfilename(filetypes=[("PDF files", "*.pdf")]))
    
def select_placeholder():
    placeholder_path.set(filedialog.askopenfilename(filetypes=[("Image files", "*.png")]))
    
def select_output_folder():
    output_folder.set(filedialog.askdirectory())
    
def run_conversion():
    try:
        myWorkflow.convert_pdf_to_png(pdf_path.get(), placeholder_path.get(), output_folder.get())
        messagebox.showinfo("Success", "Processing complete. Images saved to:\n" + output_folder.get())
    except Exception as e:
        messagebox.showerror("Error", str(e))

# GUI setup
root = tk.Tk()
root.title("PDF to PNG Converter")

pdf_path = tk.StringVar()
placeholder_path = tk.StringVar()
output_folder = tk.StringVar()

tk.Label(root, text="Select PDF file:").grid(row=0, column=0, padx=10, pady=5)
tk.Entry(root, textvariable=pdf_path, width=50).grid(row=0, column=1, padx=10, pady=5)
tk.Button(root, text="Browse", command=select_pdf).grid(row=0, column=2, padx=10, pady=5)

tk.Label(root, text="Select Placeholder Image:").grid(row=1, column=0, padx=10, pady=5)
tk.Entry(root, textvariable=placeholder_path, width=50).grid(row=1, column=1, padx=10, pady=5)
tk.Button(root, text="Browse", command=select_placeholder).grid(row=1, column=2, padx=10, pady=5)

tk.Label(root, text="Select Output Folder:").grid(row=2, column=0, padx=10, pady=5)
tk.Entry(root, textvariable=output_folder, width=50).grid(row=2, column=1, padx=10, pady=5)
tk.Button(root, text="Browse", command=select_output_folder).grid(row=2, column=2, padx=10, pady=5)

tk.Button(root, text="Convert", command=run_conversion).grid(row=3, column=0, columnspan=3, pady=20)

root.mainloop()
