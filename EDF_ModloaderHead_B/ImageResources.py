import os, sys, random, ctypes, json
import tkinter as tk
from PIL import Image, ImageTk

# Define the script directory
if getattr(sys, 'frozen', False):
    SCRIPT_DIR = sys._MEIPASS
    icon_path = os.path.join(SCRIPT_DIR, 'Icon_256.ICO')
else:
    SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
    icon_path = os.path.join(SCRIPT_DIR, 'Icon_256.ICO')

# Paths to the images and custom images folders
images_dir = os.path.join(SCRIPT_DIR, 'images')
custom_images_dir = os.path.join(SCRIPT_DIR, 'mml_custom_images')

# JSON file path
json_file_path = os.path.join(SCRIPT_DIR, 'MMLsettings.json')

# Initialize the list of possible background images
bg_images = []
image_chances = {}

# Special case image
special_case_image = 'Sky Snake.jpg'

# Load custom images from the custom folder (only .jpg files allowed)
custom_images = []
if os.path.exists(custom_images_dir):
    try:
        custom_images = [f for f in os.listdir(custom_images_dir) if f.lower().endswith('.jpg') and f != special_case_image]
        if custom_images:
            print(f'Found custom images: {custom_images}')
    except Exception as e:
        print(f'Error loading custom images from {custom_images_dir}: {e}')
else:
    print(f'Custom images folder not found: {custom_images_dir}')

bg_images.extend(custom_images)

# Load default images from the images folder (only .jpg files allowed)
default_images = []
if os.path.exists(images_dir):
    try:
        default_images = [f for f in os.listdir(images_dir) if f.lower().endswith('.jpg') and f != special_case_image]
        print(f'Loaded default images: {default_images}')
    except Exception as e:
        print(f'Error loading default images from {images_dir}: {e}')
else:
    print(f'Default images folder not found: {images_dir}')

bg_images.extend(default_images)

# Load the JSON file to check for EDF 6 completion
edf6_progress = 0.0
special_case_active = False
try:
    with open(json_file_path, 'r', encoding='utf-8') as f:
        data = json.load(f)
        edf6_progress = data.get('progress', {}).get('EDF 6', 0.0)
        print(f'EDF 6 completion: {edf6_progress}%')
        if edf6_progress >= 70.0:
            special_case_active = True
except Exception as e:
    print(f'Failed to read JSON file: {e}')

# Add special case image only if active
if special_case_active:
    bg_images.append(special_case_image)

# Calculate equal chance for each image
total_images = len(bg_images)
if total_images > 0:
    equal_chance = 1.0 / total_images
    for image in bg_images:
        image_chances[image] = equal_chance
else:
    print("No images found. Using placeholder image.")
    fallback_image = 'VShapedToobr.jpg'
    fallback_path = os.path.join(images_dir, fallback_image)
    if not os.path.exists(fallback_path):
        print(f"Fallback image not found at {fallback_path}. Background image selection will fail.")
        bg_image_path = None
    else:
        bg_images.append(fallback_image)
        image_chances[fallback_image] = 1.0

# Debug output of image chances
print('Image Chances:')
for image, chance in image_chances.items():
    print(f'  {image}: {chance:.2%}')

# Select a random image based on weighted chances
if image_chances:
    selected_bg_image = random.choices(list(image_chances.keys()), weights=list(image_chances.values()), k=1)[0]
    print(f'Selected background image: {selected_bg_image}')
else:
    selected_bg_image = None
    print("No images available for selection.")

# Determine the image path (check if custom or default)
if selected_bg_image:
    if selected_bg_image in custom_images:
        bg_image_path = os.path.join(custom_images_dir, selected_bg_image)
    else:
        bg_image_path = os.path.join(images_dir, selected_bg_image)

    # Verify the image file exists
    if not os.path.exists(bg_image_path):
        print(f'Background image not found: {bg_image_path}')
        fallback_path = os.path.join(images_dir, 'VShapedToobr.jpg')
        if os.path.exists(fallback_path):
            bg_image_path = fallback_path
        else:
            bg_image_path = None
else:
    bg_image_path = None

def set_titlebar_image(root, image_path):
    try:
        root.iconbitmap(image_path)
    except Exception as e:
        print(f"Failed to set title bar image: {e}")

def set_taskbar_image(root, image_path):
    try:
        img = Image.open(image_path)

        if sys.platform.startswith('win'):
            img = img.resize((256, 256), Image.Resampling.LANCZOS)
            img.save(icon_path, format='ICO')
            ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID('myappid')
            root.iconbitmap(icon_path)
        else:
            img = ImageTk.PhotoImage(img)
            root.iconphoto(False, img)
    except Exception as e:
        print(f"Failed to set taskbar image: {e}")

def set_icons(root, base_dir):
    if os.path.exists(icon_path):
        set_taskbar_image(root, icon_path)
        set_titlebar_image(root, icon_path)
    else:
        print(f"Icon file not found at: {icon_path}")