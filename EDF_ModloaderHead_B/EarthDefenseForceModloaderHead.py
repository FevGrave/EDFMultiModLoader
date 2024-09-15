import os, sys, webbrowser, requests, shutil, tkinter as tk, EDF_ModloaderHeadFunc as funcs, ConfigManifestUninstaller as uninstaller
import tkinter.filedialog as filedialog
from PIL import Image, ImageTk
from ImageResources import set_icons, bg_image_path
from EDF_ModloaderHeadFunc import load_settings, save_settings, settings, toggle_mods_panels, parent_dir  # Import the updated functions

'''Python 3.10.1 Build
pyinstaller.exe --noconfirm .\EDF_ModloaderHead_B\EarthDefenseForceModloaderHead.py
'''

def get_version():
    return "0.0.4.1-RC"

# Define functions to return window width, height, font, and simplify the style formats into DEFs
def width():
    return 675

def height():
    return 920

# Load settings once at the start to get the current colors
settings = load_settings()  # Make sure this loads your settings including colors

def ButtonBackGround():
    return settings.get("colors", {}).get("ButtonBackGround", "#000000")  # Default to black if not found

def ButtonPressedBackGround():
    return settings.get("colors", {}).get("ButtonPressedBackGround", "#010e70")  # Default to dark blue

def TextColor():
    return settings.get("colors", {}).get("TextColor", "#B3FF00")  # Default to Lime green

def PressedTextColor():
    return settings.get("colors", {}).get("PressedTextColor", "#ffffff")  # Default to white

def bgY():
    return"#EDFEDF"

global_font = ("AR UDJingXiHeiB5", 10)
global_fill_color = TextColor()

def get_button_style(command=None):
    """Returns common style options for buttons with an optional command."""
    style = {
        'font': global_font,
        'bg': ButtonBackGround(),
        'fg': TextColor(),
        'activebackground': ButtonPressedBackGround(),
        'activeforeground': PressedTextColor()
    }
    if command:
        style['command'] = command
    return style

def get_label_style():
    """Returns common style options for labels."""
    return {
        'font': global_font,
        'bg': ButtonBackGround(),
        'fg': TextColor(),
        'activebackground': ButtonPressedBackGround(),
        'activeforeground': PressedTextColor()
    }

def get_fill_color_style():
    """Returns common style options including global_fill_color."""
    return {
        'fill': global_fill_color,
        'font': global_font
    }

def draw_centered_text_with_bg(canvas, x, y, text, fill_color, bg_color, **style):
    # Create the text with centered alignment
    text_id = canvas.create_text(x, y, text=text, fill=fill_color, justify="center", **style)

    # Get bounding box coordinates of the created text (x1, y1, x2, y2)
    bbox = canvas.bbox(text_id)

    # Create a rectangle using the text's bounding box with added padding
    padding = 10
    rect_id = canvas.create_rectangle(
        bbox[0] - padding, bbox[1] - padding, bbox[2] + padding, bbox[3] + padding,
        fill=bg_color, outline=""
    )

    # Lower the rectangle to ensure it is behind the text
    canvas.tag_lower(rect_id, text_id)

# Initialize settings and load the current platform choice
platform_choice = settings.get("edf6_platform", "steam")
labels_and_buttons = []
current_dir = os.path.dirname(os.path.abspath(__file__ if '__file__' in globals() else sys.executable))
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# Determine the game based on the directory and Steam launch
GAME_FOLDERS = {
    "EARTH DEFENSE FORCE 4.1": ["410320"],
    "EARTH DEFENSE FORCE 5": ["1007040"],
    "EARTH DEFENSE FORCE 6": ["2291060", "129839"] # [Steam ID, Epic ID]
}
# Grouped social media links
social_media_groups = {
    "FevGrave's socials": [
        ("X", "https://x.com/FevGrave"),
        ("Reddit", "https://www.reddit.com/user/FevGrave/"),
        ("Source Code", "https://github.com/FevGrave/EDFMultiModLoader")
    ],
    "Official EDF Channel's socials": [
        ("Official EDF EN on X", "https://x.com/EDF_OFFICIAL_EN"),
        ("Official EDF JP on X", "https://x.com/EDF_OFFICIAL"),
        ("Official EDF Reddit", "https://www.reddit.com/r/EDF/"),
        ("Official EDF Discord", "https://discord.com/invite/EDF")
    ]
}

current_game = None
for folder in GAME_FOLDERS.keys():
    if folder in BASE_DIR:
        current_game = folder
        break

# Initialize the main window
root = tk.Tk()
root.title("Earth Defense Force: Multi-Mod-Loader --- V " + get_version())
root.geometry(f"{width()}x{height()}")  # Set the size of the window
root.resizable(False, False) # LOCKED WINDOW SIZE

# Set the taskbar and title bar images
set_icons(root, BASE_DIR)

# Load the background image
if os.path.exists(bg_image_path):
    bg_image = Image.open(bg_image_path)
    bg_photo = ImageTk.PhotoImage(bg_image)
else:
    print(f"Background image not found: {bg_image_path}")
    bg_photo = None


# Create a canvas and set the background image
canvas = tk.Canvas(root, width=width(), height=height())
canvas.pack(fill="both", expand=True)
if bg_photo:
    canvas.create_image(0, 0, image=bg_photo, anchor="nw")
    
# Define functions to open social media links
def open_link(url):
    webbrowser.open(url)

# Define functions to be passed to EDF_ModloaderHeadFunc.py
def check_for_update():
    clear_error()
    try:
        # GitHub API URL to fetch the latest release information
        ml_release_api_url = 'https://api.github.com/repos/BlueAmulet/EDFModLoader/releases/latest'
        
        # Send request to GitHub API
        response = requests.get(ml_release_api_url)
        response.raise_for_status()  # Raise an HTTPError for bad responses
        data = response.json()
        
        # Extract the necessary information from the release data
        latest_version = data['tag_name']
        assets = data['assets']

        # Define the directory where the files will be downloaded and extracted
        extract_to = os.path.dirname(BASE_DIR)  # Adjust path if necessary

        # Attempt to download and extract EDFModLoader.zip
        edf_modloader_zip_name = "EDFModLoader.zip"
        modloader_found = False
        for asset in assets:
            if asset['name'] == edf_modloader_zip_name:
                modloader_found = True
                zip_url = asset['browser_download_url']
                funcs.download_and_extract_zip(zip_url, edf_modloader_zip_name, extract_to, show_error)
                break

        if not modloader_found:
            show_error(f"EDFModLoader.zip was not found in the release assets. Please ensure it is uploaded correctly.")

        # Determine which plugin ZIP file is needed based on the current game
        plugin_zip_name = None
        if current_game == "EARTH DEFENSE FORCE 6":
            plugin_zip_name = "Plugins6.zip"
        elif current_game == "EARTH DEFENSE FORCE 5":
            plugin_zip_name = "Plugins5.zip"
        elif current_game == "EARTH DEFENSE FORCE 4.1":
            plugin_zip_name = "Plugins41.zip"

        if plugin_zip_name:
            found_plugin = False
            for asset in assets:
                if asset['name'] == plugin_zip_name:
                    found_plugin = True
                    zip_url = asset['browser_download_url']
                    funcs.download_and_extract_zip(zip_url, plugin_zip_name, extract_to, show_error)
                    break

            if not found_plugin:
                show_error(f"Could not find the specific plugin ZIP file: {plugin_zip_name}. Ensure it is uploaded to the release assets.")
        else:
            show_error("No valid game selected or recognized.")

        # Final message confirming the update
        show_error(f"Updated to version {latest_version} completed.")

        # Rename "Mods\ExtraPatches" to "DisabledPatches" if it exists
        extra_patches_dir = os.path.join(extract_to, "Mods", "ExtraPatches")
        disabled_patches_dir = os.path.join(extract_to, "Mods", "DisabledPatches")

        if os.path.exists(extra_patches_dir):
            if os.path.exists(disabled_patches_dir):
                shutil.rmtree(disabled_patches_dir)
            os.rename(extra_patches_dir, disabled_patches_dir)
            show_error('Renamed Folder within "Mods\ExtraPatches" to "DisabledPatches".')
        else:
            show_error('"ExtraPatches" folder not found.')

        # Check current version against GitHub's latest
        current_version = get_version().strip()
        gui_release_api_url = 'https://api.github.com/repos/FevGrave/EDFMultiModLoader/releases/latest'
        
        response = requests.get(gui_release_api_url)
        response.raise_for_status()
        data = response.json()
        latest_version = data.get('tag_name', '0.0.0').strip()

        # Version check
        if latest_version != current_version:
            show_error(f"Update available: {latest_version} (current: {current_version})")
        else:
            show_error("You are using the latest version.")
        

    except requests.exceptions.RequestException as e:
        show_error(f"Failed to check for updates: {str(e)}")
    except Exception as e:
        show_error(f"An unexpected error occurred: {str(e)}")

def update_mods():
    clear_error() 
    try:
        funcs.update_mods(show_error)  # Call the update mods function
    except Exception as e:
        show_error(str(e))

def build_tables():
    clear_error()  # Clear errors first
    try:
        funcs.build_tables(show_error)
    except Exception as e:
        show_error(str(e))

def repair_tables():
    clear_error()  # Clear errors first
    try:
        funcs.repair_tables(show_error)
    except Exception as e:
        show_error(str(e))

def uninstall_a_mod():
    clear_error()
    try:
        # Use a file dialog to let the user choose a manifest file
        manifest_file = filedialog.askopenfilename(
            title="Select a *Mod_config_data.json File to Uninstall",
            initialdir=os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "Mods", "EDF 6 MOD SETTINGS MAKER", "MOD CONFIG DATA PLACED HERE")),
            filetypes=(("JSON files", "*.json"), ("All files", "*.*"))
        )

        if manifest_file:
            show_error(f"Selected manifest file: {manifest_file}")
            
            # Set the base path to the directory containing the Mods folder
            base_dir = os.path.abspath(os.path.join(os.path.dirname(manifest_file), "..", ".."))
            show_error(f"Base directory set to: {base_dir}")

            # Pass the manifest file and the base directory to the uninstaller
            uninstaller.load_manifest_and_uninstall(manifest_file, base_dir)
            show_error("Mod uninstalled successfully.")
            
            # Remove the manifest file after processing
            try:
                os.remove(manifest_file)
                show_error(f"Manifest file removed: {manifest_file}")
            except Exception as e:
                show_error(f"Failed to remove manifest file: {manifest_file}. Error: {e}")
        else:
            show_error("No manifest file selected.")
    except Exception as e:
        show_error(str(e))

def show_help():
    clear_error() 
    try:
        funcs.show_help(show_error)
    except Exception as e:
        show_error(str(e))

def toggle_modloader_status():
    clear_error() 
    try:
        funcs.toggle_modloader_status(show_error)
        update_modloader_status()
    except Exception as e:
        show_error(str(e))

def show_error(error_msg):
    error_block.config(state=tk.NORMAL)
    error_block.insert(tk.END, error_msg + '\n')
    error_block.config(state=tk.DISABLED)

def clear_error():
    error_block.config(state=tk.NORMAL)
    error_block.delete(1.0, tk.END)
    error_block.config(state=tk.DISABLED)
    root.update_idletasks()

def update_mod_counts():
    try:
        total_mods.set(funcs.get_mod_count(show_error))
        total_patches.set(funcs.get_patch_count(show_error))
        total_plugins.set(funcs.get_plugin_count(show_error))
    except Exception as e:
        show_error(str(e))

def update_modloader_status():
    try:
        modloader_status.set(funcs.get_modloader_status())
    except Exception as e:
        show_error(str(e))

def launch_game(option):
    clear_error() 
    try:
        funcs.launch_game(option, show_error)
    except Exception as e:
        show_error(str(e))

def toggle_platform():
    """Toggle between Steam and Epic for EDF6 and save the choice."""
    global platform_choice  # Ensure global scope to modify the variable
    platform_choice = "epic" if platform_choice == "steam" else "steam"
    settings["edf6_platform"] = platform_choice
    save_settings(settings)  # Save the updated settings to the file
    toggle_button.config(text=f"Current Platform: {platform_choice.capitalize()}")

# Function to create the toggle button and add it to the list
def create_toggle_button(canvas, y_pos):
    global toggle_button  # Declare global to reference it inside other functions if needed
    toggle_button = tk.Button(root, text=f"Current Platform: {platform_choice.capitalize()}", 
                              command=toggle_platform, **get_button_style())
    labels_and_buttons.append(canvas.create_window(width() // 2, y_pos, window=toggle_button))
    y_pos + 30

# Create UI elements for grouped social media links horizontally
def create_social_media_links_horizontal(canvas, y_position):
    y_pos = y_position

    # Loop through each group and create a horizontal frame for each
    for group_name, links in social_media_groups.items():
        # Add a label for the group using the label style
        group_label = tk.Label(root, text=group_name, **get_label_style())
        canvas.create_window(width() // 2, y_pos, window=group_label)
        y_pos += 26  # Adjust spacing as necessary

        # Create a frame to hold the buttons horizontally with specific padding
        frame = tk.Frame(root, bg=bgY())

        for i, (label, url) in enumerate(links):
            # Create the button using the button style, adding the command separately
            button = tk.Button(frame, text=label, **get_button_style(lambda u=url: open_link(u)))
            
            # Adjust padding for the first and last buttons
            if i == 0:
                button.pack(side="left", padx=(0, 5))  # No left padding, only right padding
            elif i == len(links) - 1:
                button.pack(side="left", padx=(5, 0))  # Only left padding, no right padding
            else:
                button.pack(side="left", padx=5)  # Both left and right padding

        # Align the frame in the center without extra space at the ends
        canvas.create_window(width() // 2, y_pos, window=frame, anchor="center")
        y_pos += 30  # Adjust spacing for the next group

# Create UI elements
def create_ui(canvas):
    # Creating a frame to hold the six buttons side by side, with a background color
    button_frame = tk.Frame(root, bg=bgY())

    # Creating buttons using the get_button_style function
    check_update_button = tk.Button(button_frame, text="Check for Update", **get_button_style(check_for_update))
    update_mods_button = tk.Button(button_frame, text="Update Mods", **get_button_style(update_mods))
    build_tables_button = tk.Button(button_frame, text="Build Tables", **get_button_style(build_tables))
    repair_tables_button = tk.Button(button_frame, text="Repair Tables", **get_button_style(repair_tables))
    toggle_mods_panels_button = tk.Button(button_frame, text="Mods Panel", **get_button_style(lambda: toggle_mods_panels(show_error)))
    get_into_modding_button = tk.Button(button_frame, text="Get Into Modding", **get_button_style(show_help))

    # Pack the buttons side by side
    check_update_button.pack(side="left", padx=(0, 5))
    update_mods_button.pack(side="left", padx=5)
    build_tables_button.pack(side="left", padx=5)
    repair_tables_button.pack(side="left", padx=5)
    toggle_mods_panels_button.pack(side="left", padx=5)
    get_into_modding_button.pack(side="left", padx=(5, 0))

    y_pos = 30
    labels_and_buttons.append(canvas.create_window(width() // 2, y_pos, window=button_frame))
    y_pos += 35

    # Creating a text element using get_fill_color_style
    draw_centered_text_with_bg(canvas, width() // 2, y_pos, "EDF! Game to Launch", global_fill_color, ButtonBackGround(), font=global_font)

    buttons = []
    y_pos += 35
    for game, app_id in GAME_FOLDERS.items():
        button = tk.Button(root, text=game, **get_button_style(lambda opt=app_id: launch_game(opt)))
        canvas.create_window(width() // 2, y_pos, window=button)
        buttons.append(button)
        y_pos += 30

    y_pos = create_toggle_button(canvas, y_pos)
    y_pos = 30 

    # Add the overhead text and buttons for opening save folders
    y_pos += 195
    draw_centered_text_with_bg(canvas, width() // 2, y_pos, "Open Save Folders", global_fill_color, ButtonBackGround(), font=global_font)
    y_pos += 30

    save_folder_frame = tk.Frame(root, bg=bgY())
    save_folder_41_button = tk.Button(save_folder_frame, text="4.1", **get_button_style(lambda: funcs.open_save_folder(show_error, "EARTH DEFENSE FORCE 4.1")))
    save_folder_5_button = tk.Button(save_folder_frame, text="5", **get_button_style(lambda: funcs.open_save_folder(show_error, "EARTH DEFENSE FORCE 5")))
    save_folder_6_button = tk.Button(save_folder_frame, text="6", **get_button_style(lambda: funcs.open_save_folder(show_error, "EARTH DEFENSE FORCE 6")))

    save_folder_41_button.pack(side="left", padx=(0, 5))
    y_pos += 2
    save_folder_5_button.pack(side="left", padx=5)
    y_pos += 2
    save_folder_6_button.pack(side="left", padx=(5, 0))

    labels_and_buttons.append(canvas.create_window(width() // 2, y_pos, window=save_folder_frame))
    y_pos += 35

    global total_mods, total_patches, total_plugins, error_block, modloader_status
    total_mods = tk.StringVar(value="0")
    total_patches = tk.StringVar(value="0")
    total_plugins = tk.StringVar(value="0")

    modloader_status = tk.StringVar(value="Disabled")
    # Create a frame to hold both buttons side by side
    toggle_buttons_frame = tk.Frame(root, bg=bgY())

    # Create the "Toggle Modloader Status" button
    toggle_modloader_button = tk.Button(toggle_buttons_frame, text="Toggle Modloader Status:", **get_button_style(toggle_modloader_status))
    toggle_modloader_button.pack(side="left", padx=(0, 5))  # Padding to the right

    open_current_dir_button = tk.Button(toggle_buttons_frame, text="Open Current Dir", **get_button_style(lambda: os.startfile(parent_dir)))
    open_current_dir_button.pack(side="left", padx=(5, 0))

    # Add the frame with both buttons to the canvas
    labels_and_buttons.append(canvas.create_window(width() // 2, y_pos, window=toggle_buttons_frame))

    y_pos += 30
    labels_and_buttons.append(canvas.create_window(width() // 2, y_pos, window=tk.Label(root, textvariable=modloader_status, **get_label_style())))
    y_pos += 35

    draw_centered_text_with_bg(canvas, width() // 2, y_pos, "Error Block", global_fill_color, ButtonBackGround(), font=global_font)

    y_pos += 95
    error_block = tk.Text(root, height=9, font=global_font, state=tk.DISABLED, bg=ButtonBackGround(), fg=TextColor())
    canvas.create_window(width() // 2, y_pos, window=error_block)
    y_pos += 90
    labels_and_buttons.append(canvas.create_window(width() // 2, y_pos, window=tk.Button(root, text="Clear Error Block", **get_button_style(clear_error))))
    y_pos += 30

    # Create a frame for "Total Mods, Patches, and Plugins"
    mods_frame = tk.Frame(root, bg=bgY())
    mods_label = tk.Label(mods_frame, text="Mods:", **get_label_style())
    total_mods_label = tk.Label(mods_frame, textvariable=total_mods, **get_label_style())
    patches_label = tk.Label(mods_frame, text="Patches:", **get_label_style())
    total_patches_label = tk.Label(mods_frame, textvariable=total_patches, **get_label_style())
    plugins_label = tk.Label(mods_frame, text="Plugins:", **get_label_style())
    total_plugins_label = tk.Label(mods_frame, textvariable=total_plugins, **get_label_style())

    mods_label.pack(side="left", padx=0)
    total_mods_label.pack(side="left", padx=0)
    patches_label.pack(side="left", padx=(10, 0))
    total_patches_label.pack(side="left", padx=0)
    plugins_label.pack(side="left", padx=(10, 0))
    total_plugins_label.pack(side="left", padx=0)

    labels_and_buttons.append(canvas.create_window(width() // 2, y_pos, window=mods_frame))
    y_pos += 105

    notes_text = """EDF! EDF! EDF! EDF! EDF! EDF! EDF!
Created By:
BlueAmulet
(Modloader)
FevGrave
(GUI, MML Table Generator, BG Images)
{VVV STILL A WIP VVV}
MoistGoat
(Advanced MissionPack Settings)
EDF! EDF! EDF! EDF! EDF! EDF! EDF!"""
    # Draw the notes_text with centered alignment and a matching background
    draw_centered_text_with_bg(canvas, width() // 2, y_pos, notes_text, global_fill_color, ButtonBackGround(), font=global_font, width=600)

    y_pos += 103
    # Update mod counts and modloader status on startup
    update_mod_counts()
    update_modloader_status()

    y_pos += 2  # Adjust spacing as necessary
    create_social_media_links_horizontal(canvas, y_pos)

# Use canvas to create the UI elements
create_ui(canvas)

# Start the Tkinter event loop
root.mainloop()
