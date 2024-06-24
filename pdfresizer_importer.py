import os
from PIL import Image
import fitz  # PyMuPDF

def import_pdf(pdf_path):
    pdf_document = fitz.open(pdf_path)
    images = []
    
    for page_num in range(pdf_document.page_count):
        page = pdf_document.load_page(page_num)
        pix = page.get_pixmap()
        img = Image.frombytes("RGB", [pix.width, pix.height], pix.samples)
        images.append(img)
        
    return images

def import_images(image_folder, extensions=[".png", ".jpg", ".jpeg"]):
    images = []
    
    for filename in os.listdir(image_folder):
        if any(filename.lower().endswith(ext) for ext in extensions):
            img_path = os.path.join(image_folder, filename)
            img = Image.open(img_path)
            images.append(img)
            
    return images
