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
        ("PDF, PPTX, Image files", "*.pdf *.pptx *.png *.jpg *.jpeg"),
        ("PowerPoint (PPTX) files", "*.pptx"),
        ("PDF files", "*.pdf"),
        ("Image files", "*.png *.jpg *.jpeg")], initialdir=preferences.get('pdf_directory', ''))
    if file_paths:
        global chosen_files
        chosen_files = list(file_paths)
        preferences['pdf_directory'] = os.path.dirname(file_paths[0])
        # if (len(chosen_files) > 1):   # this code works for a single-line display, showing off the chosen_files.
        #     files_display.set('; '.join(chosen_files))
        # else:
        #     files_display.set(chosen_files[0])
        files_display.config(height=len(chosen_files))
        files_display.delete('1.0', tk.END)
        files_display.insert(tk.END, "\n".join(chosen_files))
    
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
        images = []
        
        # Save the selected paths to preferences
        myWorkflow.save_preferences(preferences)

        # Process each selected file or folder
        for file in chosen_files:
            print(f"Processing file: {file}")  # Debugging line
            
            if file.endswith(".pdf"):
                images = myInput.import_pdf(file)
                
            elif file.endswith(".pptx"):
                
                images, media_files = myInput.import_pptx(file, output_folder.get())
                
                # do additional processing for video and audio media
                myWorkflow.process_media_files(media_files, output_folder.get())
                
            elif file.endswith((".png", ".jpg", ".jpeg")) and (len(chosen_files) > 1):
                images.append(Image.open(file)) # might actually allow for selective files 
                
            else:
                images = myInput.import_images(os.path.dirname(file))
            
        # Convert images to PNG, and will run even on a .pptx file
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

files_display = tk.Text(root, height=1, width=100)  # Text widget to display selected files
selected_files = tk.StringVar(value=preferences.get('input_file', ''))
placeholder_path = tk.StringVar(value=preferences.get('placeholder_path', ''))
output_folder = tk.StringVar(value=preferences.get('output_directory', ''))

tk.Label(root, text="Select file:", bg=bg_color, fg=fg_color).grid(row=0, column=0, padx=10, pady=5)
files_display.grid(row=0, column=1, padx=10, pady=5)
tk.Button(root, text="Browse", command=select_pdf).grid(row=0, column=2, padx=10, pady=5)

tk.Label(root, text="Select Placeholder Image:",bg=bg_color, fg=fg_color).grid(row=1, column=0, padx=10, pady=5)
tk.Entry(root, textvariable=placeholder_path, width=100, justify=tk.RIGHT).grid(row=1, column=1, padx=10, pady=5)
tk.Button(root, text="Browse", command=select_placeholder).grid(row=1, column=2, padx=10, pady=5)

tk.Label(root, text="Select Output Folder:", bg=bg_color, fg=fg_color).grid(row=2, column=0, padx=10, pady=5)
tk.Entry(root, textvariable=output_folder, width=100, justify=tk.RIGHT).grid(row=2, column=1, padx=10, pady=5)
tk.Button(root, text="Browse", command=select_output_folder).grid(row=2, column=2, padx=10, pady=5)

tk.Button(root, text="Convert", command=run_conversion).grid(row=3, column=0, columnspan=3, pady=20)

root.mainloop()
