# ImageResources.py

import os, sys, random, ctypes
from PIL import Image, ImageTk

# List of possible background images
bg_images = [
    'page_bg_raw.jpg',
    'page_bg_raw01.jpg',
    'DebugBG.jpg',  # Add more images as needed
]

# Define the script directory
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))

# Path to the images folder
images_dir = os.path.join(SCRIPT_DIR, 'images')

# List all images in the images folder
bg_images = [file for file in os.listdir(images_dir) if file.endswith(('.jpg', '.png'))]

# Select a random background image
selected_bg_image = random.choice(bg_images)

# Set the full path for the selected background image
bg_image_path = os.path.join(images_dir, selected_bg_image)
# Define the icon image path
icon_path = os.path.join(SCRIPT_DIR, 'Icon_256.ico')

def set_titlebar_image(root, image_path):
    """
    Set the title bar icon for the Tkinter window.

    Args:
        root (Tk): The main Tkinter window.
        image_path (str): The path to the image file.
    """
    try:
        img = Image.open(image_path)
        img = ImageTk.PhotoImage(img)
        root.iconphoto(False, img)
    except Exception as e:
        print(f"Failed to set title bar image: {e}")

def set_taskbar_image(root, image_path):
    """
    Set the taskbar icon for the Tkinter window.

    Args:
        root (Tk): The main Tkinter window.
        image_path (str): The path to the image file.
    """
    try:
        img = Image.open(image_path)
        
        #.ico for Windows taskbar icon
        if sys.platform.startswith('win'):
            img = img.resize((64, 64), Image.ANTIALIAS)
            img.save(icon_path, format='ICO')
            ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID('myappid')
            root.iconbitmap(icon_path)
        else:
            # For other systems, set the window icon (Linux and Mac)
            img = ImageTk.PhotoImage(img)
            root.iconphoto(False, img)
    except Exception as e:
        print(f"Failed to set taskbar image: {e}")

def set_icons(root, base_dir):
    """Sets the taskbar and title bar images for the application."""
    if os.path.exists(icon_path):
        set_taskbar_image(root, icon_path)
        set_titlebar_image(root, icon_path)
    else:
        print(f"Icon file not found: {icon_path}")