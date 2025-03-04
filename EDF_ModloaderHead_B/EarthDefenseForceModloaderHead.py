import os, re, sys, threading, webbrowser, requests, shutil, subprocess, json, time, pytz
import tkinter as tk, tkinter.messagebox as messagebox, eggs as eggs, random
import tkinter.font as tkFont, EDF_ModloaderHeadFunc as funcs
from PIL import Image, ImageTk, ImageFont
from ImageResources import set_icons, bg_image_path
from EDF_ModloaderHeadFunc import load_settings, save_settings, settings, toggle_mods_panels, get_settings

'''
#TODO

get coding support for nexus
finalize R2Modman code share support
'''

def get_version():
    return "0.0.9-R2ModManTest"

def title():
    return "Earth Defense Force: Multi-Mod-Loader --- V " + get_version()

def width():
    return 675

def height():
    return 920

root = tk.Tk()
root.title(title())
root.geometry(f"{width()}x{height()}")
root.resizable(False, False)

RUN_BAT_FILES_ENABLED = True  # Set to False to hide the debug build HAKKEN exe button

BAT_FILES_DIRS = (
    r"F:\SteamLibrary\steamapps\common\EARTH DEFENSE FORCE 6\Mods\EDF 6 MOD SETTINGS MAKER",
    r"F:\SteamLibrary\steamapps\common\EARTH DEFENSE FORCE 6\EDF_ModloaderHead_B"
)

EXCLUDED_BAT_FILES = {
    "Python Install PREREQUISETS.bat"  # Add any batch files you want to exclude here
}

def run_bat_files_from_dirs():
    """Runs all .bat files from specified directories sequentially in a new thread."""
    def execute():
        all_bat_files = []

        # Collect all .bat files from directories while excluding specific files
        for dir_path in BAT_FILES_DIRS:
            if not os.path.exists(dir_path):
                show_error(f"Directory not found: {dir_path}")
                continue  # Skip to the next directory if one is missing

            bat_files = [
                os.path.join(dir_path, f)
                for f in os.listdir(dir_path)
                if f.endswith(".bat") and f not in EXCLUDED_BAT_FILES
            ]
            all_bat_files.extend(sorted(bat_files))

        if not all_bat_files:
            show_error("No .bat files found in the specified directories.")
            return

        show_error("Starting batch file execution...")

        # Run all .bat files in sequence
        for bat_file_path in all_bat_files:
            show_error(f"Running: {bat_file_path}")

            try:
                subprocess.run(bat_file_path, shell=True, check=True)
            except subprocess.CalledProcessError as e:
                show_error(f"Error executing {bat_file_path}: {str(e)}")
                break  # Stop execution on failure

        show_error("All batch files executed successfully.")

    # Run in a separate thread to keep the GUI responsive
    threading.Thread(target=execute, daemon=True).start()

set_current_dir = os.path.dirname(os.path.abspath(__file__ if '__file__' in globals() else sys.executable))
funcs.initialize_settings(set_current_dir)
settings = funcs.get_settings()
settings = load_settings(set_current_dir)

def update_setting(setting_key, setting_value, settings_file="MMLsettings.json"):
    """
    Update a specific setting in the settings file.

    Parameters:
    - setting_key (str): The key of the setting to update.
    - setting_value: The new value to assign to the setting.
    - settings_file (str): Path to the settings JSON file (default: "MMLsettings.json").

    Returns:
    - bool: True if the update was successful, False otherwise.
    """
    try:
        # Load the current settings
        if os.path.exists(settings_file):
            with open(settings_file, "r") as file:
                settings = json.load(file)
        else:
            settings = {}

        # Update the specified setting
        settings[setting_key] = setting_value

        # Save the updated settings back to the file
        with open(settings_file, "w") as file:
            json.dump(settings, file, indent=4)

        print(f"Setting '{setting_key}' updated to '{setting_value}' successfully.")
        return True
    except Exception as e:
        print(f"Error updating setting '{setting_key}': {str(e)}")
        return False

def JustBackGround():
    return settings.get("colors", {}).get("JustBackGround", "#484848")  # Default to gray if not found

def ButtonBackGround():
    return settings.get("colors", {}).get("ButtonBackGround", "#000000")  # Default to black if not found

def ButtonPressedBackGround():
    return settings.get("colors", {}).get("ButtonPressedBackGround", "#010e70")  # Default to dark blue

def hover_bg():
    return settings.get("colors", {}).get("hover_bg", "#555555")

def hover_fg():
    return settings.get("colors", {}).get("hover_fg", "#ffffff")

def TextColor():
    return settings.get("colors", {}).get("TextColor", "#B3FF00")  # Default to lime green

def PressedTextColor():
    return settings.get("colors", {}).get("PressedTextColor", "#ffffff")  # Default to white

def bgY():
    return"#EDFEDF"  # EDF EDF EDF EDF EDF EDF EDF EDF EDF EDF EDF EDF

def get_font_path():
    # If running as a bundled executable, use the executable's directory
    if hasattr(sys, '_MEIPASS'):
        return os.path.join(sys._MEIPASS, "fonts", "RobotoCondensed-Bold.ttf")
    # Otherwise, use the standard relative path
    else:
        return os.path.join(os.path.dirname(__file__), "fonts", "RobotoCondensed-Bold.ttf")

def load_custom_font(size=10):
    font_path = get_font_path()
    if os.path.exists(font_path):
        try:
            # Load the font using PIL's ImageFont
            pil_font = ImageFont.truetype(font_path, size)
            # Register the font with Tkinter
            custom_font = tkFont.Font(family=pil_font.getname()[0], size=size)
            return custom_font
        except Exception as e:
            print(f"Error loading custom font: {e}. Using default font.")
            return tkFont.Font(size=size)  # Fallback to default font if loading fails
    else:
        print(f"Font file not found at {font_path}. Using default font.")
        return tkFont.Font(size=size)  # Fallback to default font if not found

global_font = load_custom_font(10)
global_font_h = load_custom_font(12)
global_fill_color = TextColor()

def get_button_style(command=None):
    """Returns common style options for buttons with an optional command."""
    style = {
        'font': global_font,
        'bg': ButtonBackGround(),
        'fg': TextColor(),
        'activebackground': ButtonPressedBackGround(),
        'activeforeground': PressedTextColor(),
        'relief': 'groove',
        'bd': 2,
        'cursor': 'hand2'  # Change the cursor to a pointer when hovering
    }
    if command:
        style['command'] = command
    return style

def apply_hover_effect(button, hover_bg=hover_bg(), hover_fg=hover_fg(), normal_bg=None, normal_fg=None):
    """Adds a hover effect to a button."""
    if not normal_bg:
        normal_bg = button.cget("bg")
    if not normal_fg:
        normal_fg = button.cget("fg")

    def on_enter(event):
        button.config(bg=hover_bg, fg=hover_fg)

    def on_leave(event):
        button.config(bg=normal_bg, fg=normal_fg)

    button.bind("<Enter>", on_enter)
    button.bind("<Leave>", on_leave)

def get_label_style():
    """Returns common style options for labels."""
    return {
        'font': global_font_h,
        'bg': JustBackGround(),
        'fg': TextColor()
    }

def get_label_style_alt(command=None):
    """Returns Important style options for labels."""
    style = {
        'font': global_font,
        'bg': TextColor(),
        'fg': ButtonBackGround(),
        'activebackground': PressedTextColor(),
        'activeforeground': ButtonPressedBackGround()
    }
    if command:
        style['command'] = command
    return style

def draw_centered_text_with_bg(canvas, x, y, text, fill_color, bg_color, **style):
    # Create the text with centered alignment
    text_id = canvas.create_text(x, y, text=text, fill=fill_color, justify="center", **style)

    # Get bounding box coordinates of the created text (x1, y1, x2, y2)
    bbox = canvas.bbox(text_id)

    # Create a rectangle using the text's bounding box with added padding
    padding = 5
    rect_id = canvas.create_rectangle(
        bbox[0] - padding, bbox[1] - padding, bbox[2] + padding, bbox[3] + padding,
        fill=bg_color, outline=""
    )

    # Lower the rectangle to ensure it is behind the text
    canvas.tag_lower(rect_id, text_id)

def start_directory_monitoring():
    """Start monitoring mod, patch, and plugin directories for changes using polling."""
    
    def monitor_directories(interval=5):
        """Continuously monitor directories with periodic updates."""
        total_mods.set(funcs.get_mod_count(show_error))
        total_patches.set(funcs.get_patch_count(show_error))
        total_plugins.set(funcs.get_plugin_count(show_error))
        update_mod_counts()
        root.after(interval, monitor_directories)

    # Start the monitoring thread
    monitoring_thread = threading.Thread(target=monitor_directories, daemon=True)
    monitoring_thread.start()

def start_update_check():
    update_thread = threading.Thread(target=check_for_update)
    update_thread.daemon = True  # Daemon thread will automatically close when the main program exits
    update_thread.start()
    game_server_warn_thread = threading.Thread(target=warn_check)
    game_server_warn_thread.daemon = True
    game_server_warn_thread.start()

def warn_check():
    debug_mode = False  # Set to False to use real Tuesday reboot schedule
    debug_reboot_offset = 0  # Set debug reboot in X seconds (only when debug_mode is True)
    # Get current time in UTC
    now_utc = time.time()

    if debug_mode:
        show_error("⚠️ DEBUG SERVER TIMER MODE ENABLED   ⚠️")
        reboot_time = now_utc + debug_reboot_offset  # Debug countdown
    else:
        # Find the next Tuesday's reboot time
        days_until_tuesday = (1 - time.localtime().tm_wday) % 7  # 1 = Tuesday
        reboot_time = now_utc + (days_until_tuesday * 86400)  # Convert days to seconds
        reboot_time = time.mktime(time.gmtime(reboot_time)) + (15 * 3600)  # Set to 3 PM UTC

    def update_warning():
        now_time = time.time()
        remaining_time = reboot_time - now_time

        # Skip warnings if more than 12 hours remain
        if remaining_time > 2 * 3600:  
            root.after(3600000, update_warning)  # Check again in 1 hour
            return

        if remaining_time <= 0:
            # If time is up, start the reboot progress bar
            server_reboot_in_progress()
            return

        # Convert remaining time into hours, minutes, seconds
        hours = int(remaining_time // 3600)
        minutes = int((remaining_time % 3600) // 60)
        seconds = int(remaining_time % 60)

        countdown_str = f"Reboot in {hours}h {minutes}m {seconds}s"
        show_error(f"⚠️ WARNING: SERVERS WILL REBOOT SOON   ⚠️ - {countdown_str}")
        show_error("PLEASE BE ADVISED: ONLINE PLAY WILL BE AFFECTED")

        # Refresh countdown every second
        root.after(1000, update_warning)

    update_warning()

def server_reboot_in_progress():
    """Display 'SERVER REBOOT IN PROGRESS' with an ASCII loading bar effect"""
    clear_error()
    show_error("⚠️ SERVER REBOOT IN PROGRESS   ⚠️")

    bar_length = 87  # Width of the loading bar
    duration = 20 * 60  # 20 minutes in seconds
    start_time = time.time()  # Track actual start time
    server_check_notified = False  # Ensure "check the servers" only prints once

    def update_loading_bar():
        nonlocal server_check_notified  # Allow updating this inside the function
        elapsed_time = time.time() - start_time  # Get actual elapsed time
        remaining_time = duration - elapsed_time

        if remaining_time <= 0:
            clear_error()
            show_error("✅ COMPLETED SERVER REBOOT ✅")
            show_error("HAVE FUN")
            return

        # Calculate progress
        progress = int((elapsed_time / duration) * bar_length)
        progress_units = progress // 3  # Convert to "EDF" units (each "EDF" is 3 characters)
        
        # Ensure proper padding and alignment
        edf_fill = "EDF" * progress_units
        spaces_fill = " " * (bar_length - len(edf_fill))
        loading_bar = f"[{edf_fill}{spaces_fill}]%"

        clear_error()
        show_error("⚠️ SERVER REBOOT IN PROGRESS   ⚠️")
        show_error(loading_bar)

        # Notify users at 75% (15 minutes in)
        if elapsed_time >= duration * 0.75 and not server_check_notified:
            show_error("Check the servers they should be online again")
            server_check_notified = True  # Prevent multiple messages

        # Refresh every second
        root.after(1000, update_loading_bar)

    update_loading_bar()

for widget in root.winfo_children():
    if isinstance(widget, tk.Button):
        apply_hover_effect(widget, hover_bg="#555555", hover_fg="#ffffff")

# Initialize settings and load the current platform choice
platform_choice = settings.get("edf6_platform", "steam")
labels_and_buttons = []
set_current_dir = os.path.dirname(os.path.abspath(__file__ if '__file__' in globals() else sys.executable))
# Check if 'base_dir' is set; if not, save 'set_current_dir' as 'base_dir' in settings
if 'base_dir' not in settings:
    settings['base_dir'] = set_current_dir
    with open("MMLsettings.json", "w") as f:
        json.dump(settings, f, indent=4)
current_dir = settings.get("base_dir", "")
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# Determine the game based on the Steam and Epic launch # [Steam ID, Epic ID]
GAME_FOLDERS = {
    "EDF 41 WINGDIVER THE SHOOTER": ['574200'],
    "Earth Defense Force 4.1": ["410320"],
    "Earth Defense Force 5": ["1007040"],
    "Earth Defense Force 6": ["2291060", "129839"],
    "Earth Defense Force WB": ["1497950"],
    "Earth Defense Force WB2": ["2370170", "23328f"],
    "Earth Defense Force IR": ["1039890"],
    "Earth Defense Force IA": ["23530"],
}
# Grouped social media links
social_media_groups = {
    "Get Into Modding": [
        ("Documentation/Wiki", "https://github.com/KCreator/Earth-Defence-Force-Documentation/wiki"),
        ("Maybe Birb's Guide on 'HOW TO MOD EARTH DEFENSE FORCE'", "https://steamcommunity.com/sharedfiles/filedetails/?id=3083510169")
    ],
    "Blue Amulet's Modloader": [
        ("Source Code", "https://www.github.com/repos/BlueAmulet/EDFModLoader")
    ],
    "Official EDF Channel's socials": [
        ("Official EDF EN on X", "https://x.com/EDF_OFFICIAL_EN"),
        ("Official EDF JP on X", "https://x.com/EDF_OFFICIAL"),
        ("Official EDF Reddit", "https://www.reddit.com/r/EDF/"),
        ("Official EDF Discord", "https://discord.com/invite/EDF")
    ],
    "FevGrave's socials": [
        ("X", "https://x.com/FevGrave"),
        ("Reddit", "https://www.reddit.com/user/FevGrave/"),
        ("Source Code", "https://github.com/FevGrave/EDFMultiModLoader"),
        ("Discord Model/Thumbnail Request Form", "https://discord.com/channels/207292314064781312/1272000404875378718"),
        ("Discord MML Form", "https://discord.com/channels/207292314064781312/1284693030003019797")
    ]
}

game_to_mod_host_links = {
    "Earth Defense Force 6": [
        ("Nexus Mods", "https://www.nexusmods.com/earthdefenseforce6"),
        ("ModDB", "https://www.moddb.com/games/earth-defense-force-6"),
        ("Thunderstore", "https://edf-6.thunderstore.io/")  # Placeholder
    ],
    "Earth Defense Force 5": [
        ("Nexus Mods", "https://www.nexusmods.com/earthdefenseforce5"),
        ("ModDB", "https://www.moddb.com/games/earth-defense-force-5"),
        ("Thunderstore", "https://edf-5.thunderstore.io/")
    ],
    "Earth Defense Force 4.1": [
        ("Nexus Mods", "https://www.nexusmods.com/earthdefenseforce41theshadowofnewdespair"),
        ("ModDB", "https://www.moddb.com/games/earth-defense-force-41-the-shadow-of-new-despair/mods"),
        ("Thunderstore", "https://edf-4-1.thunderstore.io/")
    ]
}

current_game = None
for folder in GAME_FOLDERS.keys():
    if folder in BASE_DIR:
        current_game = folder
        break

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

def get_padding(index, total):
    """Helper function to calculate padding based on button position."""
    if total == 1:
        return (0, 0)  # No padding for a single button
    elif index == 0:
        return (0, 5)  # No left padding, right padding only for the first button
    elif index == total - 1:
        return (5, 0)  # Left padding only, no right padding for the last button
    else:
        return (5, 5)  # Both left and right padding for middle buttons

def open_link(url):
    webbrowser.open(url)

def check_for_update():
    clear_error()
    try:
        gui_release_api_url = 'https://api.github.com/repos/FevGrave/EDFMultiModLoader/releases'

        headers = {
            'Accept': 'application/vnd.github.v3+json',
        }
        response = requests.get(gui_release_api_url, headers=headers)
        response.raise_for_status()
        releases = response.json()
        latest_prerelease = next((release for release in releases if release.get('prerelease', False)), None)

        if not latest_prerelease:
            show_error("No pre-release found.")
            return

        latest_version = latest_prerelease.get('tag_name', '0.0.0').strip()
        assets = latest_prerelease.get('assets', [])
        current_version = get_version().strip()

        if current_version == latest_version:
            show_error("You are using the latest EDF Multi Mod Loader version.")
            show_error("Use the cmds of 'help', 'h', 'HELP' in the Request Mod Code")
            # If already up to date, show the changelog for this version
            show_error("changelog.txt")
        elif current_version < latest_version:
            # Prompt the user to update
            update_prompt = messagebox.askyesno(
                "EDF MML Update Available",
                f"Version {latest_version} is available! You are currently using {current_version}. Do you want to update now?"
            )
            if update_prompt:
                executable_name = "EDF MML.exe"
                download_url = next((asset['browser_download_url'] for asset in assets if asset['name'] == executable_name), None)

                if download_url:
                    download_and_replace_executable(download_url, executable_name)
                    # After update, show the changelog for the new version
                    show_error("changelog.txt")
                else:
                    show_error(f"Update failed: Could not find {executable_name} in the latest release assets.")
        else:
            show_error(f"Version {current_version} is not in our records! You are currently superseding our latest version {latest_version}. ARE YOU A SPY, OR A TIME TRAVELER?")
            show_error("Use the cmds of 'help', 'h', 'HELP' in the Request Mod Code")

    except requests.exceptions.RequestException as e:
        show_error(f"EDF MML failed to check for updates: {str(e)}")
    except Exception as e:
        show_error(f"An unexpected error occurred: {str(e)}")

def download_and_replace_executable(download_url, executable_name):
    try:
        # Download the new version of the executable
        response = requests.get(download_url, stream=True)
        response.raise_for_status()
        new_executable_path = os.path.join(os.path.dirname(sys.executable), "new_version.exe")

        # Save the downloaded executable to a temporary location
        with open(new_executable_path, "wb") as file:
            shutil.copyfileobj(response.raw, file)
        show_error("Downloaded the latest version.")

        # Ask the user to close the application before replacing the executable
        messagebox.showinfo(
            "Update Complete",
            "The update has been downloaded. Please close the application to complete the update."
        )

        # Replace the old executable with the new one
        os.replace(new_executable_path, os.path.join(os.path.dirname(sys.executable), executable_name))
        show_error("Application updated successfully. Please restart the application.")

        # Optionally, you can auto-restart the app after updating if desired
        # os.execv(sys.executable, ['python'] + sys.argv)

    except requests.exceptions.RequestException as e:
        show_error(f"Failed to download the update: {str(e)}")
    except Exception as e:
        show_error(f"An error occurred during the update process: {str(e)}")

def check_for_ba_update():
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
        # extract_to = os.path.dirname(BASE_DIR)  # Adjust path if necessary
        extract_to = r'F:\\SteamLibrary\\steamapps\\common\\EARTH DEFENSE FORCE 6'

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
            show_error('Renamed Folder within the "Mods" folder "ExtraPatches" to "DisabledPatches".')
        else:
            show_error('"ExtraPatches" folder not found.')

    except requests.exceptions.RequestException as e:
        show_error(f"Failed to check for updates: {str(e)}")
    except Exception as e:
        show_error(f"An unexpected error occurred: {str(e)}")

def update_mods():
    update_mod_counts()
    clear_error() 
    try:
        funcs.update_mods(show_error)  # Call the update mods function
    except Exception as e:
        show_error(str(e))

def build_tables():
    update_mod_counts()
    clear_error()  # Clear errors first
    show_error("Starting the EDF HAKKEN build process...")
    error_block.update()  # Update the UI

    # Run the task in a separate thread
    threading.Thread(target=run_build_tables).start()

def run_build_tables():
    try:
        # Load settings to check modloader_HAKKEN_style
        settings = load_settings(os.getcwd())
        modloader_style = settings.get("modloader_HAKKEN_style", "NI")  # Default to "NI" (No Installer)
        # Map styles to EXE names
        exe_name = "EDF HAKKEN NI.exe" if modloader_style == "NI" else "EDF HAKKEN.exe"
        # Pass the selected EXE to build_tables
        show_error(f"Starting build process using: {exe_name}")
        funcs.build_tables(show_error, exe_name=exe_name)
        show_error("Build process completed successfully.")
    except Exception as e:
        show_error(f"An error occurred during the build process: {str(e)}")
        error_block.update()

def repair_tables():
    clear_error()  # Clear errors first
    try:
        funcs.repair_tables(show_error, current_dir)
    except Exception as e:
        show_error(str(e))

def create_game_launch_bar(canvas, y_position):
    # Add a label above the dropdown, play button, toggle button, and progress tracker button
    label = tk.Label(
        root,
        text="EDF! Game to Launch",
        font=global_font_h,
        bg=JustBackGround(),
        fg=TextColor(),
    )
    canvas.create_window(width() // 2, y_position, window=label)
    y_position += 35

    # Create a frame for all elements in this section
    game_launch_frame = tk.Frame(root, bg=bgY(), highlightthickness=0)

    # Dropdown menu for selecting games
    selected_game = tk.StringVar(value="Earth Defense Force 6")  # Default selection
    game_dropdown = tk.OptionMenu(game_launch_frame, selected_game, *GAME_FOLDERS.keys())
    game_dropdown.config(
        bg=ButtonBackGround(),
        fg=TextColor(),
        activebackground=hover_bg(),
        activeforeground=hover_fg(),
        relief="groove",
        highlightthickness=0,
        cursor="hand2"
    )
    game_dropdown["menu"].config(
        bg=ButtonBackGround(),
        fg=TextColor(),
        activebackground=hover_bg(),
        activeforeground=hover_fg()
    )
    game_dropdown.pack(side="left", padx=(0, 10))

    # Add the "Play This Game" button
    def handle_launch():
        game_key = selected_game.get()
        app_ids = GAME_FOLDERS.get(game_key)
    
        if not app_ids:
            show_error(f"Game '{game_key}' not found in GAME_FOLDERS.")
            return

        if len(app_ids) == 1:  # Single ID available, default to Steam
            funcs.launch_game([app_ids[0]], show_error)
        else:
            if platform_choice == "epic" and len(app_ids) > 1:
                funcs.launch_game(app_ids, show_error)  # Pass both IDs, Epic is prioritized
            else:
                funcs.launch_game([app_ids[0]], show_error)  # Steam ID

    play_button = tk.Button(
        game_launch_frame,
        text="Play This Game",
        command=handle_launch,
        **get_label_style_alt()
    )
    apply_hover_effect(play_button)
    play_button.pack(side="left", padx=(0, 10))

    # Add the toggle button for platform selection
    global toggle_button
    toggle_button = tk.Button(
        game_launch_frame,
        text=f"Current Platform: {platform_choice.capitalize()}",
        command=toggle_platform,
        **get_button_style()
    )
    apply_hover_effect(toggle_button)
    toggle_button.pack(side="left", padx=(0, 10))

    # Add the "Progress Tracker" button
    progress_tracker_button = tk.Button(
        game_launch_frame,
        text="Online Progress Tracker",
        command=launch_progress_tracker,
        **get_label_style_alt()
    )
    apply_hover_effect(progress_tracker_button)
    progress_tracker_button.pack(side="left", padx=(0, 0))

    # Add the frame to the canvas
    canvas.create_window(width() // 2, y_position, window=game_launch_frame, anchor="center")
    return y_position

def launch_progress_tracker():
    try:
        # Determine the base directory based on frozen status
        BASE_DIR = os.path.dirname(sys.executable) if getattr(sys, 'frozen', False) else os.path.dirname(__file__)
        progress_tracker_exe = os.path.join(BASE_DIR, "ProgressTrackerPercent.exe")

        # Use shell=True to improve compatibility on Windows
        subprocess.Popen(progress_tracker_exe, shell=True, close_fds=True)
    except Exception as e:
        print(f"Failed to launch the progress tracker: {e}")

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

def start_monitoring_loop():
    update_mod_counts()  # Immediate first update
    root.after(5000, start_monitoring_loop)  # Repeat every 5 seconds

def update_mod_counts():
    try:
        # Get updated counts
        mods = int(funcs.get_mod_count(show_error))
        patches = int(funcs.get_patch_count(show_error))
        plugins = int(funcs.get_plugin_count(show_error))

        # Update the displayed counts
        total_mods.set(str(mods))
        total_patches.set(str(patches))
        total_plugins.set(str(plugins))

        # Dynamically enable/disable buttons
        mods_button.config(state="normal" if mods > 0 else "disabled")
        patches_button.config(state="normal" if patches > 0 else "disabled")
        plugins_button.config(state="normal" if plugins > 0 else "disabled")

    except Exception as e:
        show_error(f"Error updating counts: {str(e)}")

def open_mod_folder(folder_path):
    """Opens the specified folder path. Handles errors if the folder doesn't exist."""
    try:
        # Validate if the folder exists
        absolute_path = os.path.abspath(folder_path)
        if os.path.exists(absolute_path):
            os.startfile(absolute_path)  # Open the folder
        else:
            show_error(f"Failed to open folder: {absolute_path} does not exist.")
    except Exception as e:
        show_error(f"Failed to open folder: {str(e)}")

def create_mod_info_buttons(canvas, y_position):
    """Creates interactive buttons to replace labels for mod information."""
    global mods_button, patches_button, plugins_button  # Declare global for dynamic updates

    mods_frame = tk.Frame(root, bg=bgY())

    # Create buttons to open mod-related directories
    mods_button = tk.Button(
        mods_frame,
        text="Mods:",
        **get_button_style(lambda: open_mod_folder(r"Mods\EDF 6 MOD SETTINGS MAKER\MOD CONFIG DATA PLACED HERE"))
    )
    total_mods_label = tk.Label(mods_frame, textvariable=total_mods, **get_label_style())
    apply_hover_effect(mods_button)

    patches_button = tk.Button(
        mods_frame,
        text="Patches:",
        **get_button_style(lambda: open_mod_folder(r"Mods\Patches"))
    )
    total_patches_label = tk.Label(mods_frame, textvariable=total_patches, **get_label_style())
    apply_hover_effect(patches_button)

    plugins_button = tk.Button(
        mods_frame,
        text="Plugins:",
        **get_button_style(lambda: open_mod_folder(r"Mods\Plugins"))
    )
    total_plugins_label = tk.Label(mods_frame, textvariable=total_plugins, **get_label_style())
    apply_hover_effect(plugins_button)

    # Pack the buttons and labels
    mods_button.pack(side="left", padx=0)
    total_mods_label.pack(side="left", padx=(5, 5))
    patches_button.pack(side="left", padx=0)
    total_patches_label.pack(side="left", padx=(5, 5))
    plugins_button.pack(side="left", padx=0)
    total_plugins_label.pack(side="left", padx=(5, 5))
    plugins_button.pack(side="left", padx=0)
    
    # Add the frame to the canvas
    labels_and_buttons.append(canvas.create_window(width() // 2, y_position, window=mods_frame))
    return y_position + 35

def update_modloader_status():
    try:
        current_status = funcs.get_modloader_status()  # Get the current status
        modloader_status.set(f"Toggle Modloader Status: {current_status}")  # Update with prefixed text
    except Exception as e:
        show_error(str(e))

def toggle_platform():
    """Toggle between Steam and Epic for EDF6 and save the choice."""
    global platform_choice, toggle_button  # Ensure both are accessible
    platform_choice = "epic" if platform_choice == "steam" else "steam"

    # Update the settings dictionary
    settings = get_settings()
    settings["edf6_platform"] = platform_choice  # Update platform in settings
    save_settings(settings)  # Persist the updated settings

    # Update the toggle button text
    if toggle_button:
        toggle_button.config(text=f"Current Platform: {platform_choice.capitalize()}")

def create_mod_hosting_services(canvas, y_position):
    y_pos = y_position

    # Add "Mod Hosting Services" text
    draw_centered_text_with_bg(
        canvas,
        width() // 2,
        y_pos,
        "Mod Hosting Services",
        global_fill_color,  # Foreground color
        JustBackGround(),   # Background color
        font=global_font_h
    )
    y_pos += 30  # Spacing below the label

    # Add dropdown for game selection
    hosting_frame = tk.Frame(root, bg=bgY())
    selected_game = tk.StringVar(value="Earth Defense Force 6")  # Default game

    # Function to dynamically update mod hosting links
    def update_links(selected_game):
        # Clear the existing buttons in the frame
        for widget in dynamic_links_frame.winfo_children():
            widget.destroy()

        # Get the links for the selected game
        links = game_to_mod_host_links.get(selected_game, [])

        # Create buttons for each link
        for i, (label, url) in enumerate(links):
            button = tk.Button(dynamic_links_frame, text=label, command=lambda u=url: open_link(u), **get_button_style())
            apply_hover_effect(button)
            button.pack(side="left", padx=get_padding(i, len(links)))

    # Dropdown menu
    dropdown = tk.OptionMenu(hosting_frame, selected_game, *game_to_mod_host_links.keys(), command=update_links)
    dropdown.config(
        bg=ButtonBackGround(),
        fg=TextColor(),
        activebackground=hover_bg(),
        activeforeground=hover_fg(),
        relief="solid",
        highlightthickness=0,
        cursor="hand2"
    )
    dropdown["menu"].config(
        bg=ButtonBackGround(),
        fg=TextColor(),
        activebackground=hover_bg(),
        activeforeground=hover_fg()
    )
    dropdown.pack(side="left", padx=(0, 10))  # Add padding between dropdown and buttons

    # Create a frame for dynamic mod hosting links
    dynamic_links_frame = tk.Frame(hosting_frame, bg=bgY())
    dynamic_links_frame.pack(side="left")  # Pack it into the hosting frame

    # Initialize the links with the default game
    update_links(selected_game.get())

    # Place the hosting frame on the canvas
    canvas.create_window(width() // 2, y_pos, window=hosting_frame, anchor="center")
    return y_pos  # Return the updated y_position

def handle_request_drop_off(request_code):
    """Handle the request drop-off button click with support for text-based commands."""
    
    def is_valid_uuid(candidate):
        # Basic UUID format validation of 36 characters in HEX For R2Modman code sharing
        return bool(re.match(r"^[0-9a-fA-F\-]{36}$", candidate))

    def process_request():
        clear_error()
        if not request_code.strip():
            show_error("Error: Request code cannot be empty!")
            return None
        normalized_code = request_code.strip().lower() # Normalize the input by trimming whitespace and converting to lowercase
        if is_valid_uuid(normalized_code):
            show_error(f"Processing Mod request with UUID: {normalized_code}")
            # Add R2MODMAN UUID processing logic here
            update_mods()
        
        elif normalized_code in ["debug_cmd"]:
            clear_error()

        elif normalized_code in ["no install", "ni"]:
            show_error("Processing No Install (NI) request...")
            funcs.build_tables(show_error, exe_name="EDF HAKKEN NI.exe")
            update_setting("modloader_HAKKEN_style", "NI")

        elif normalized_code in ["install", "i"]:
            show_error("Processing Install (I) request...")
            funcs.build_tables(show_error, exe_name="EDF HAKKEN.exe")
            update_setting("modloader_HAKKEN_style", "I")

        elif normalized_code in ["help", "h"]:
            show_error("'help', 'h', 'HELP': Show console commands (SCROLL DOWN IN THIS WINDOW)")
            show_error("'install', 'i': Install all files that will be generated from the 'Build Tables' button. AUTO_BUILDS\n")
            show_error("'no install', 'ni': Debug mode - generates files but does NOT install them. AUTO_BUILDS\n")
            show_error("'credits', 'who_made_this' Prints who has had a hand in making this tool set \n")
            show_error("EASTER EGGS HIDDEN WITHIN ME, ALWAYS LOWERCASE, SPACES ARE _, THREE WORDS MAX, NUMBERS SPELT ARE CRINGE, SO DO THE ARABIC SYMBOLS AS A EXAMPLE COMMAND beans_1234567890_test, NUMBERS ARE ALWAYS ARE SURROUND BY _, IF YE SEEK A TRAIL, hint_me")

        elif normalized_code in ["bob_the_builder"]:
            clear_error()
            run_bat_files_from_dirs()

        elif normalized_code in ["e_d_f"]:
            clear_error()
            eggs.display_letters(show_error, clear_error)

        elif normalized_code in ["credits", "who_made_this"]:
            clear_error()
            eggs.edf_credits_scroll(show_error, clear_error, speed=0.1)

        elif normalized_code in ["hint_me"]:
            rhyming_hints = [
                "Want text to scroll like a marquee? This command makes words glide smoothly in EDF style.",  # edf_marquee
                "Summon the storm with one transmission. A message from the battlefield awaits.",  # storm_1_transmission
                "Need some EDF wisdom? Grab some quotes. Soldier chatter and war cries incoming.",  # edf_quotes
                "A chant of war, a battle cry. Use this command and watch morale fly.",  # chant_edf
                "A mission starts, a briefing’s here. A call for deployment, orders are loud and clear.",  # deployment_orders / mission_briefing
                "Incoming, A voice rings out, a warning near. A transmission now, for all to hear.",  # incoming_transmission
                "Cows do moo, but so can you. Type it now and get a clue.",  # moo
                "A soldier’s tale, of hero’s might. Call this command, reveal the fight.",  # storm_1_transmission
                "The past is lost to time, the path unclear. A future erased, yet something is coming to rewrite or destroy.",  # erased_future / time_rewrite
                "E TO THE D TO THE F"  # e_d_f
            ]
            show_error(f"🤔 HINT: {random.choice(rhyming_hints)}")

        elif normalized_code in ["moo"]:
            show_error("You found an Easter Egg! 🥚🐣")
            time.sleep(3)
            clear_error()
            eggs.asciicow(show_error)

        elif normalized_code in ["erased_future", "time_rewrite"]:
            show_error("You found a Classified Easter Egg! 🕵️‍♂️")
            time.sleep(3)
            clear_error()
            eggs.erased_future_transmission(show_error, clear_error)

        elif normalized_code in ["beans_1234567890_test"]:
            show_error("You found an Easter Egg! 🥚🐣")
            time.sleep(1)
            show_error("Wait... you actually used that?")
            time.sleep(2)
            show_error("Well, I guess you need a reward...")
            time.sleep(2)
            show_error("The hints in 'hint_me' do hold the words to combine into an Easter egg command.")
            time.sleep(2)
            show_error("Just look at the rhymes... they guide your way!")
            show_error("10 different eggs can be found minus me...")

        elif normalized_code in ["edf_marquee"]:
            show_error("You found an Easter Egg! 🥚🐣")
            time.sleep(3)
            clear_error()
            eggs.side_scroll_edf_multiline(show_error, clear_error, speed=0.1)

        elif normalized_code in ["chant_edf"]:
            show_error("You found an Easter Egg! 🥚🐣")
            time.sleep(3)
            clear_error()
            eggs.play_edf_chant(show_error, clear_error)

        elif normalized_code in ["storm_1_transmission"]:
            show_error("You found an Easter Egg! 🥚🐣")
            time.sleep(3)
            clear_error()
            eggs.someegg(show_error)

        elif normalized_code in ["incoming_transmission"]:
            show_error("You found an Easter Egg! 🥚🐣")
            time.sleep(3)
            clear_error()
            eggs.edf_quotes(show_error)

        elif normalized_code in ["deployment_orders", "mission_briefing"]:
            show_error("You found an Easter Egg! 🥚🐣")
            time.sleep(3)
            clear_error()
            eggs.edf_mission_generator(show_error)

        else:
            show_error("Error: Invalid request code or command!")

    # Run the processing in a separate thread
    threading.Thread(target=process_request, daemon=True).start()

def create_mod_request_input(canvas, y_position):
    y_pos = y_position

    # Add the header above the input field
    header_label = tk.Label(
        root,
        text="Request Mod Code: Air Force Drop-Off (R2modman Code Sharing{incomplete})",
        font=global_font_h,
        bg=JustBackGround(),
        fg=TextColor()
    )
    canvas.create_window(width() // 2, y_pos, window=header_label)
    y_pos += 30  # Adjust spacing below the header

    # Create a frame to hold the slider, input field, and button
    input_frame = tk.Frame(
        root,
        bg=bgY(),
        highlightthickness=0,
        bd=0,
        relief="groove"
    )
    # Add the text input field
    text_var = tk.StringVar()
    text_input = tk.Entry(
        input_frame,
        textvariable=text_var,
        font=global_font,
        width=int(65),
        bg="#EDFEDF",
        fg="black",
        relief="groove"
    )
    text_input.pack(side="left", padx=get_padding(2, 4), pady=0)

    # Add the "Request Drop Off Now" button
    drop_off_button = tk.Button(
        input_frame,
        text="Request Drop Off Now",
        command=lambda: [
            handle_request_drop_off(text_var.get())
        ],
        **get_label_style_alt()
    )
    drop_off_button.pack(side="left", padx=get_padding(3, 4), pady=0)
    apply_hover_effect(drop_off_button)

    # Add the input frame to the canvas
    canvas.create_window(
        width() // 2,
        y_pos,
        window=input_frame,
        anchor="center"
    )
    y_pos += 5  # Adjust spacing below the input field

    return y_pos

def search_nexus_mods():
    # Define the search term and target URL
    search_term = "Earth Defense Force"
    base_url = "https://www.nexusmods.com/games"
    params = {"search": search_term}

    try:
        # Send a GET request
        response = requests.get(base_url, params=params)

        if response.status_code == 200:
            # Use regex to extract search results
            pattern = re.compile(r'<span class="result-term">(.*?)</span>')
            search_results = pattern.findall(response.text)

            # Print each search result
            if search_results:
                for result in search_results:
                    print(result.strip())
            else:
                print("No search results found.")
        else:
            print(f"Failed to load the page. Status code: {response.status_code}")
    except requests.RequestException as e:
        print(f"An error occurred: {e}")

def create_social_media_links_horizontal(canvas, y_position):
    y_pos = y_position

    # Loop through each group and create a horizontal frame for each
    for group_name, links in social_media_groups.items():
        # Add a label for the group
        group_label = tk.Label(
            root,
            text=group_name,
            font=global_font,
            bg=JustBackGround(),
            fg=TextColor()
        )
        canvas.create_window(width() // 2, y_pos, window=group_label)
        y_pos += 26  # Adjust spacing as necessary

        # Create a frame to hold the buttons horizontally
        frame = tk.Frame(root, bg=bgY())
        
        # Loop through the links and create buttons
        for i, (label, url) in enumerate(links):
            command = lambda u=url: search_nexus_mods() if u is None else open_link(u)
            button = tk.Button(frame, text=label, command=command, **get_button_style())
            button.pack(side="left", padx=get_padding(i, len(links)))
            apply_hover_effect(button)

        # Center-align the frame and increment y-position
        canvas.create_window(width() // 2, y_pos, window=frame, anchor="center")
        y_pos += 30 
    return y_pos  # Return the updated y_position

# Create UI elements
def create_ui(canvas):
    global total_mods, total_patches, total_plugins, error_block, modloader_status
    total_mods = tk.StringVar(value="0")
    total_patches = tk.StringVar(value="0")
    total_plugins = tk.StringVar(value="0")

    y_pos = 30  # Starting vertical position
    vertical_spacing = 30  # Consistent spacing value

    # === Game Launch ===
    y_pos = create_game_launch_bar(canvas, y_pos)
    y_pos += vertical_spacing + 5

    # === Directory Management ===
    draw_centered_text_with_bg(canvas, width() // 2, y_pos, "MML Installed Dir Only", global_fill_color, JustBackGround(), font=global_font_h)
    y_pos += vertical_spacing + 5

    # === Game Management ===
    game_management_frame = tk.Frame(root, bg=bgY())
    game_management_buttons = [
        ("Check for B.A.M.L Update", check_for_ba_update),
        ("Update Mods", update_mods),
        ("Build Tables", build_tables),
        ("Repair Tables", repair_tables),
        ("Mods Panel", lambda: toggle_mods_panels(show_error)),
    ]


    # Create and pack buttons using `get_padding`
    for idx, (text, command) in enumerate(game_management_buttons):
        button = tk.Button(game_management_frame, text=text, command=command, **get_label_style_alt())
        button.pack(side="left", padx=get_padding(idx, len(game_management_buttons)))
        apply_hover_effect(button)

    labels_and_buttons.append(canvas.create_window(width() // 2, y_pos, window=game_management_frame))
    y_pos += vertical_spacing

    # === Toggle Buttons ===
    toggle_buttons_frame = tk.Frame(root, bg=bgY())
    modloader_status = tk.StringVar(value=f"Toggle Modloader Status: {funcs.get_modloader_status()}")
    toggle_buttons = [
        (modloader_status, toggle_modloader_status),
        ("Open The Current Dir", lambda: os.startfile(current_dir)),
    ]

    # Create and pack toggle buttons using `get_padding`
    for idx, (text_or_var, command) in enumerate(toggle_buttons):
        button = tk.Button(
            toggle_buttons_frame,
            text=text_or_var if isinstance(text_or_var, str) else None,
            textvariable=text_or_var if isinstance(text_or_var, tk.StringVar) else None,
            command=command,
            **get_button_style(),
        )
        apply_hover_effect(button)
        button.pack(side="left", padx=get_padding(idx, len(toggle_buttons)))

    labels_and_buttons.append(canvas.create_window(width() // 2, y_pos, window=toggle_buttons_frame))
    y_pos += vertical_spacing

    # === Mod Information ===
    y_pos = create_mod_info_buttons(canvas, y_pos)
    y_pos += 5

    # === Save Folders Management ===
    draw_centered_text_with_bg(canvas, width() // 2, y_pos, "Open Save Folders", global_fill_color, JustBackGround(), font=global_font_h)
    y_pos += vertical_spacing + 5

    save_folder_frame = tk.Frame(root, bg=bgY())
    save_folder_buttons = [
        ("4.1", lambda: funcs.open_save_folder(show_error, "EARTH DEFENSE FORCE 4.1")),
        ("5", lambda: funcs.open_save_folder(show_error, "EARTH DEFENSE FORCE 5")),
        ("6", lambda: funcs.open_save_folder(show_error, "EARTH DEFENSE FORCE 6")),
    ]

    # Create and pack save folder buttons using `get_padding`
    for idx, (text, command) in enumerate(save_folder_buttons):
        button = tk.Button(save_folder_frame, text=text, command=command, **get_button_style())
        apply_hover_effect(button)
        button.pack(side="left", padx=get_padding(idx, len(save_folder_buttons)))

    labels_and_buttons.append(canvas.create_window(width() // 2, y_pos, window=save_folder_frame))
    y_pos += vertical_spacing + 10

    # === Mod Hosting Services ===
    y_pos = create_mod_hosting_services(canvas, y_pos)
    y_pos += vertical_spacing + 5

    # === Mod Request Input ===
    y_pos = create_mod_request_input(canvas, y_pos)
    y_pos += vertical_spacing + 5

    # === Console and Logs ===
    draw_centered_text_with_bg(canvas, width() // 2, y_pos, "HQ Pager Console", global_fill_color, JustBackGround(), font=global_font_h)
    y_pos += vertical_spacing + 35

    error_block = tk.Text(root, height=6, width=90, font=("Courier", 9), state=tk.DISABLED, bg=ButtonBackGround(), fg=TextColor(), wrap="word")
    canvas.create_window(width() // 2, y_pos, window=error_block)
    y_pos += 70

    clear_console_button = tk.Button(root, text="Clear Console", **get_label_style_alt(clear_error))
    apply_hover_effect(clear_console_button)  # Apply default hover effect

    # Add the button to the canvas
    labels_and_buttons.append(
        canvas.create_window(width() // 2, y_pos, window=clear_console_button)
    )
    y_pos += vertical_spacing

    # Update mod counts and statuses on startup
    update_mod_counts()
    start_monitoring_loop()
    update_modloader_status()
    create_social_media_links_horizontal(canvas, y_pos)
    
    y_pos += 200
    # Add button to UI if RUN_BAT_FILES_ENABLED is True
    if RUN_BAT_FILES_ENABLED:
        y_pos += 30  # Adjust the y position for the new button
        bat_button = tk.Button(root, text="Run All BAT Files (Two Directories)", command=run_bat_files_from_dirs, **get_label_style_alt())
        apply_hover_effect(bat_button) 
        canvas.create_window(width() // 2, y_pos, window=bat_button)

# Use canvas to create the UI elements
create_ui(canvas)

start_update_check()

root.mainloop()
