import os, sys, random, ctypes, json
import tkinter as tk
from PIL import Image, ImageTk

# Define the script directory
if getattr(sys, 'frozen', False):
    SCRIPT_DIR = sys._MEIPASS
    CUSTOM_DIR = os.path.dirname(sys.executable)
else:
    SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
    CUSTOM_DIR = os.path.dirname(SCRIPT_DIR)

icon_path = os.path.join(SCRIPT_DIR, 'Icon_256.ICO')

# Paths to the images and custom images folders
images_dir = os.path.join(SCRIPT_DIR, 'images')
custom_images_dir = os.path.join(CUSTOM_DIR, 'Mods', 'EDF 6 MOD SETTINGS MAKER', 'mml_custom_images')

# JSON file path
json_file_path = os.path.join(CUSTOM_DIR, 'MMLsettings.json')

# Special case image
special_case_image = 'sky snake.jpg'

# Load custom images (including duplicates)
custom_images = []
if os.path.exists(custom_images_dir):
    try:
        custom_images = [f for f in os.listdir(custom_images_dir) if f.lower().endswith('.jpg')]
        if custom_images:
            print(f'Found custom images: {custom_images}')
    except Exception as e:
        print(f'Error loading custom images from {custom_images_dir}: {e}')
else:
    print(f'Custom images folder not found: {custom_images_dir}')

# Load default images (including duplicates)
default_images = []
if os.path.exists(images_dir):
    try:
        default_images = [f for f in os.listdir(images_dir) if f.lower().endswith('.jpg')]
        print(f'Loaded default images: {default_images}')
    except Exception as e:
        print(f'Error loading default images from {images_dir}: {e}')
else:
    print(f'Default images folder not found: {images_dir}')

# Combine images into bg_images (allowing duplicates)
bg_images = custom_images + default_images

# Load EDF 6 progress
edf6_progress = 0.0
try:
    with open(json_file_path, 'r', encoding='utf-8') as f:
        data = json.load(f)
        edf6_progress = data.get('progress', {}).get('EDF 6', 0.0)
except Exception as e:
    print(f'Failed to read JSON file: {e}')

print(f'EDF 6 Progress: {edf6_progress}%')

# Manage special case image (allowing multiple copies if present in folders)
special_case_count = bg_images.count(special_case_image)

if edf6_progress >= 70.0:
    if special_case_count == 0:
        bg_images.append(special_case_image)
        print(f'Added special case image: {special_case_image}')
else:
    bg_images = [img for img in bg_images if img.lower() != special_case_image]
    print(f'Removed special case image: {special_case_image}')

# Recalculate image probabilities with duplicates
image_chances = {}
total_images = len(bg_images)

if total_images > 0:
    for image in bg_images:
        image_chances[image] = image_chances.get(image, 0) + 1  # Count occurrences

    # Normalize probabilities
    for image in image_chances:
        image_chances[image] /= total_images
else:
    print("No images found. Using fallback.")
    fallback_image = 'Preemo.jpg'
    if os.path.exists(os.path.join(images_dir, fallback_image)):
        bg_images.append(fallback_image)
        image_chances[fallback_image] = 1.0

# Debugging output for image chances
print('Updated Image Chances:')
for image, chance in image_chances.items():
    print(f'  {image}: {chance:.2%}')

# Select a random image based on weighted chances
selected_bg_image = random.choices(list(image_chances.keys()), weights=list(image_chances.values()), k=1)[0]
print(f'Selected background image: {selected_bg_image}')

# Determine image path
if selected_bg_image:
    bg_image_path = os.path.join(custom_images_dir, selected_bg_image) if selected_bg_image in custom_images else os.path.join(images_dir, selected_bg_image)
    if not os.path.exists(bg_image_path):
        print(f'Background image not found: {bg_image_path}, using fallback.')
        fallback_path = os.path.join(images_dir, 'Preemo.jpg')
        bg_image_path = fallback_path if os.path.exists(fallback_path) else None
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
