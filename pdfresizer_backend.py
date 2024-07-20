from PIL import Image
import os
import json

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
        

def resize_and_center_image(image, target_size):
    # Calculate the scaling factor
    target_width, target_height = target_size
    original_width, original_height = image.size
    scaling_factor = min(target_width / original_width, target_height / original_height)

    # Resize the image
    new_width = int(original_width * scaling_factor)
    new_height = int(original_height * scaling_factor)
    resized_image = image.resize((new_width, new_height), Image.LANCZOS)

     # Create a new image with the target size and paste the resized image
    new_image = Image.new("RGBA", target_size, (255, 255, 255, 0))  # Transparent background

    # Calculate the left position based on aspect ratio
    left_position = 0
    if original_width / original_height <= 0.75:  # For aspect ratios narrower than 3:4
        left_position = 275
    elif original_width / original_height <= 1:  # For aspect ratios narrower than 1:1
        left_position = 400
    elif original_width / original_height < 1.33:  # For aspect ratios narrower than 4:3
        left_position = 40
    paste_position = (left_position, (target_height - new_height) // 2)
    new_image.paste(resized_image, paste_position, resized_image)

    return new_image


def process_images(images, placeholder_path, output_folder):
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    # Load the placeholder image
    placeholder = Image.open(placeholder_path).convert("RGBA")

    for index, img in enumerate(images):
        # Ensure the image is in RGBA mode
        img = img.convert("RGBA")

        # Resize and center the image
        processed_img = resize_and_center_image(img, placeholder.size)
        
        # Layer the processed image on top of the placeholder
        combined_img = Image.alpha_composite(placeholder, processed_img)

        # Convert to RGB mode before saving
        combined_img = combined_img.convert("RGB")

        # Save the combined image
        output_path = os.path.join(output_folder, f"slide_{index+1}.png")
        combined_img.save(output_path)

        print(f"Processed slide {index+1}/{len(images)}")

    print("\nProcessing complete. Images saved to:", output_folder)
