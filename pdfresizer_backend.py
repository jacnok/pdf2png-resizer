import fitz  # PyMuPDF
from PIL import Image
import os
import json
import pdfresizer_importer

# Load preferences
def load_preferences():
    try:
        with open('preferences.json', 'r') as f:
            return json.load(f)
    except:
        return {'pdf_directory':'', 'placeholder_path' : '', 'output_directory': ''}

# Save preferences
def save_preferences(preferences):
    with open('preferences.json', 'w') as f:
        json.dump(preferences, f, indent=4)
        

def convert_images_to_png(images, placeholder_path, output_folder):
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    for index, img in enumerate(images):
        width, height = img.size
        
        if width != 1920 or height != 1080:
            # taken from https://www.geeksforgeeks.org/print-colors-python-terminal/, 
            def prRed(skk): print("\033[91m {}\033[00m".format(skk)) 
            
            prRed(f"Image {index+1} is not 1920x1080, but {width}x{height}")

        # Resize the image to 1440x810 using LANCZOS filter
        img_resized = img.resize((1440, 810), Image.LANCZOS)

        # Open the placeholder image and resize to 480x810 using LANCZOS filter
        placeholder = Image.open(placeholder_path).resize((480, 810), Image.LANCZOS)

        # Create a new image with the combined width of 1920 and height of 810
        combined_img = Image.new("RGB", (1920, 810))

        # Paste the resized image and placeholder image into the combined image
        combined_img.paste(img_resized, (0, 0))
        combined_img.paste(placeholder, (1440, 0))

        # Save the combined image
        output_path = os.path.join(output_folder, f"slide_{index+1}.png")
        combined_img.save(output_path)

        print(f"Processed image {index+1}/{len(images)}")

    print("Processing complete. Images saved to:", output_folder)
