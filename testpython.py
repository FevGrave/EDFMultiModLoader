import tkinter as tk
from tkinter import messagebox

def show_popup():
    # Create the root window
    root = tk.Tk()
    root.withdraw()  # Hide the root window

    # Show a message box
    messagebox.showinfo("Test Popup", "This is a test popup message!")

    # Close the root window after showing the popup
    root.destroy()

# Run the popup function
show_popup()
