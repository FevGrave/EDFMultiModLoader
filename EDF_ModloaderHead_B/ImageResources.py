import os, sys, random, ctypes, json, threading
import tkinter as tk
from PIL import Image, ImageTk, ImageSequence

# Define the script directory
if getattr(sys, 'frozen', False):
    SCRIPT_DIR = sys._MEIPASS
    CUSTOM_DIR = os.path.dirname(sys.executable)
else:
    SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
    CUSTOM_DIR = os.path.dirname(SCRIPT_DIR)

icon_path = os.path.join(SCRIPT_DIR, 'Icon_256.PNG')

# Paths to the images and custom images folders
images_dir = os.path.join(SCRIPT_DIR, 'images')
custom_images_dir = os.path.join(CUSTOM_DIR, 'Mods', 'EDF 6 MOD SETTINGS MAKER', 'mml_custom_images')

# JSON file path
json_file_path = os.path.join(CUSTOM_DIR, 'MMLsettings.json')

# Special case image
special_case_image = ['sky snake.jpg', 'sky snake_N.jpg']

# Load custom images (including duplicates)
custom_images = []
if os.path.exists(custom_images_dir):
    try:
        custom_images = [
            f for f in os.listdir(custom_images_dir)
            if f.lower().endswith(('.jpg', '.jpeg', '.png', '.webp'))
        ]
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
        default_images = [
            f for f in os.listdir(images_dir)
            if f.lower().endswith(('.jpg', '.jpeg', '.png', '.webp'))
        ]
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

# Remove or add special case images based on EDF 6 progress
if edf6_progress >= 70.0:
    for special_img in special_case_image:
        if special_img not in bg_images:
            bg_images.append(special_img)
            print(f'Added special case image: {special_img}')
else:
    removed = []
    bg_images = [img for img in bg_images if img.lower() not in [s.lower() for s in special_case_image]]
    removed = [s for s in special_case_image if s in custom_images or s in default_images]
    if removed:
        print(f'Removed special case images: {removed}')

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
        # Use 256x256 PNG directly
        img = Image.open(image_path).convert("RGBA")

        # Build both large and small versions
        img_256 = img.resize((256, 256), Image.Resampling.LANCZOS)
        img_32  = img.resize((32, 32), Image.Resampling.LANCZOS)

        tk_icon_large = ImageTk.PhotoImage(img_256)
        tk_icon_small = ImageTk.PhotoImage(img_32)

        # Register app for taskbar ID refresh
        ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID('edf_mml_0.0.9.2')

        # Best compatibility: apply both icons
        root.iconphoto(False, tk_icon_small, tk_icon_large)

    except Exception as e:
        print(f"Failed to set taskbar image: {e}")

def set_icons(root, base_dir):
    if os.path.exists(icon_path):
        set_taskbar_image(root, icon_path)
    else:
        print(f"Icon file not found at: {icon_path}")

def get_random_background_path():
    """Return a random background image path with weighted selection."""
    if not image_chances:
        return None
    selected = random.choices(list(image_chances.keys()), weights=list(image_chances.values()), k=1)[0]
    if selected in custom_images:
        return os.path.join(custom_images_dir, selected)
    else:
        return os.path.join(images_dir, selected)
    
def load_resized_background_image(path, target_width, target_height):
    """Load and resize a background image (PNG, JPG, WEBP) to fit the window."""
    try:
        img = Image.open(path).convert("RGBA")
        img = img.resize((target_width, target_height), Image.Resampling.LANCZOS)
        return ImageTk.PhotoImage(img)
    except Exception as e:
        print(f"❌ Failed to load or resize background image '{path}': {e}")
        return None

def cmd_bg_list(return_text=False):
    """Print and/or return all background images with their source folders."""
    lines = []
    if not bg_images:
        lines.append("⚠️ No background images found.")
    else:
        total = len(bg_images)
        uniform_chance = 1 / total
        lines.append(f"🖼️ Background Image Pool")
        lines.append(f"Each image has an equal chance of {uniform_chance:.2%}\n")

        for img in sorted(bg_images, key=str.casefold):
            if img in custom_images:
                source = "[custom]"
            elif img in default_images:
                source = "[default]"
            else:
                source = "[unknown]"
            lines.append(f"  {source} {img}")

    full_output = "\n".join(lines)
    print(full_output)
    if return_text:
        return full_output

def load_gif_background(canvas, root, show_error):
    from PIL import ImageSequence

    gif_path = os.path.join(images_dir, 'edf_easter.gif')
    if not os.path.exists(gif_path):
        show_error("GIF background not found!")
        return

    try:
        gif = Image.open(gif_path)

        # Get the current dimensions of the canvas or root window
        root.update_idletasks()
        width = canvas.winfo_width()
        height = canvas.winfo_height()
        if width < 100 or height < 100:  # fallback during early load
            width, height = 675, 920

        # Resize each frame to fit the canvas
        frames = [
            ImageTk.PhotoImage(frame.copy().convert("RGBA").resize((width, height), Image.Resampling.LANCZOS))
            for frame in ImageSequence.Iterator(gif)
        ]

        # Keep track of the animated image object to avoid garbage collection
        canvas._gif_frames = frames

        def animate(index=0):
            if frames:
                canvas.delete("gif_bg")  # Remove previous
                canvas.create_image(0, 0, image=frames[index], anchor='nw', tags="gif_bg")
                root.after(100, lambda: animate((index + 1) % len(frames)))

        animate()
        show_error("🎉 EDF GIF background enabled!")

    except Exception as e:
        show_error(f"Error loading/resizing GIF: {e}")
