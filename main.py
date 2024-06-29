import tkinter as tk
from tkinter import filedialog, messagebox
from PIL import Image
import os
import pdfresizer_backend as myWorkflow  # Import the backend module
import pdfresizer_importer as myInput # Import the new importer module

# Load preferences on startup
preferences = myWorkflow.load_preferences()
chosen_files = []

def select_pdf():
    file_paths = filedialog.askopenfilenames(filetypes=[
        ("PDF, Image files", "*.pdf *.png *.jpg *.jpeg"),
        ("PDF files", "*.pdf"),
        ("Image files", "*.png *.jpg *.jpeg")], initialdir=preferences.get('pdf_directory', ''))
    if file_paths:
        global chosen_files
        chosen_files = list(file_paths)
        preferences['pdf_directory'] = os.path.dirname(file_paths[0])
        print(f"This is chosen_files: {chosen_files}")
        # preferences['pdf_file'] = file_path
    
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

        # Process each selected file or folder
        for file in chosen_files:
            print(f"Processing file: {file}")  # Debugging line
            if file.endswith(".pdf"):
                images = myInput.import_pdf(file)
            elif file.endswith((".png", ".jpg", ".jpeg")):
                images = [Image.open(file)]
            else:
                images = myInput.import_images(os.path.dirname(file))
            
            # Convert images to PNG
            myWorkflow.process_images(images, placeholder_path.get(), output_folder.get())
        
        messagebox.showinfo("Success", "Processing complete. Images saved to:\n" + output_folder.get())
    except Exception as e:
        messagebox.showerror("Error", str(e))

# GUI setup
root = tk.Tk()
root.title("PDF+ to PNG Converter")

bg_color = '#038C5A'
fg_color = '#F7F3EE'


root.configure(background=bg_color)


selected_files = tk.StringVar(value=preferences.get('pdf_file', ''))
# pdf_path = tk.StringVar(value=preferences.get('pdf_file', ''))
placeholder_path = tk.StringVar(value=preferences.get('placeholder_path', ''))
output_folder = tk.StringVar(value=preferences.get('output_directory', ''))

tk.Label(root, text="Select file:", bg=bg_color, fg=fg_color).grid(row=0, column=0, padx=10, pady=5)
tk.Entry(root, textvariable=selected_files, width=100, justify=tk.RIGHT).grid(row=0, column=1, padx=10, pady=5)
tk.Button(root, text="Browse", command=select_pdf).grid(row=0, column=2, padx=10, pady=5)

tk.Label(root, text="Select Placeholder Image:",bg=bg_color, fg=fg_color).grid(row=1, column=0, padx=10, pady=5)
tk.Entry(root, textvariable=placeholder_path, width=100, justify=tk.RIGHT).grid(row=1, column=1, padx=10, pady=5)
tk.Button(root, text="Browse", command=select_placeholder).grid(row=1, column=2, padx=10, pady=5)

tk.Label(root, text="Select Output Folder:", bg=bg_color, fg=fg_color).grid(row=2, column=0, padx=10, pady=5)
tk.Entry(root, textvariable=output_folder, width=100, justify=tk.RIGHT).grid(row=2, column=1, padx=10, pady=5)
tk.Button(root, text="Browse", command=select_output_folder).grid(row=2, column=2, padx=10, pady=5)

tk.Button(root, text="Convert", command=run_conversion).grid(row=3, column=0, columnspan=3, pady=20)

root.mainloop()
