import fitz  # PyMuPDF
from PIL import Image
import os

def convert_pdf_to_png(pdf_path, placeholder_path, output_folder):
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    # Open the PDF file
    pdf_document = fitz.open(pdf_path)
    page_count = pdf_document.page_count
    
    for page_num in range(page_count):
        # Load a page and check the size
        page = pdf_document.load_page(page_num)
        width, height = page.rect.width, page.rect.height
        
        if width != 1920 or height != 1080:
            # taken from https://www.geeksforgeeks.org/print-colors-python-terminal/, 
            def prRed(skk): print("\033[91m {}\033[00m".format(skk)) 
            
            prRed(f"Page {page_num+1} is not 1920x1080, but {width}x{height}")

        # Render the page to an image
        pix = page.get_pixmap()
        img = Image.frombytes("RGB", [pix.width, pix.height], pix.samples)

        # Resize the image to 1440x810
        img_resized = img.resize((1440, 810), Image.LANCZOS)

        # Open the placeholder image and resize to 480x810
        placeholder = Image.open(placeholder_path).resize((480, 810))

        # Create a new image with the combined width of 1920 and height of 810
        combined_img = Image.new("RGB", (1920, 810))

        # Paste the resized PDF page and placeholder image into the combined image
        combined_img.paste(img_resized, (0, 0))
        combined_img.paste(placeholder, (1440, 0))

        # Save the combined image
        output_path = os.path.join(output_folder, f"slide_{page_num+1}.png")
        combined_img.save(output_path)

        print(f"Processed page {page_num+1}/{page_count}")

    print("Processing complete. Images saved to:", output_folder)
