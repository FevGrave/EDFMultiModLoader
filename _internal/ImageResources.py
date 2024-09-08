# ImageResources.py

import os
import sys
from PIL import Image, ImageTk
import ctypes

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
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
        
        # Convert .webp to .ico for Windows taskbar icon
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
