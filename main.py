import tkinter as tk
from tkinter import filedialog, messagebox
import pdfresizer_backend as myWorkflow  # Import the backend module
import os

# Load preferences on startup
preferences = myWorkflow.load_preferences()


def select_pdf():
    file_path = filedialog.askopenfilename(filetypes=[("PDF files", "*.pdf")], initialdir=preferences.get('pdf_directory', ''))
    if file_path:
        pdf_path.set(file_path)
        preferences['pdf_directory'] = os.path.dirname(file_path)
        preferences['pdf_file'] = file_path
    
def select_placeholder():
    file_path = filedialog.askopenfilename(filetypes=[("Image files", "*.png")], initialdir=preferences.get('placeholder_path', ''))
    if file_path:
        placeholder_path.set(file_path)
        preferences['placeholder_path'] = file_path
    
def select_output_folder():
    folder_path = filedialog.askdirectory(initialdir=preferences.get('output_directory', ''))
    if folder_path:
        output_folder.set(folder_path)
        preferences['output_directory'] = folder_path
    
def run_conversion():
    try:
        # Save the selected paths to preferences
        myWorkflow.save_preferences(preferences)

        myWorkflow.convert_pdf_to_png(pdf_path.get(), placeholder_path.get(), output_folder.get())
        messagebox.showinfo("Success", "Processing complete. Images saved to:\n" + output_folder.get())
    except Exception as e:
        messagebox.showerror("Error", str(e))

# GUI setup
root = tk.Tk()
root.title("PDF to PNG Converter")

pdf_path = tk.StringVar(value=preferences.get('pdf_file', ''))
placeholder_path = tk.StringVar(value=preferences.get('placeholder_path', ''))
output_folder = tk.StringVar(value=preferences.get('output_directory', ''))

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
