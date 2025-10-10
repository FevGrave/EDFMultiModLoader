import os, re, sys, threading, webbrowser, requests, shutil, subprocess, json, time, uuid, zipfile
import tkinter as tk, tkinter.messagebox as messagebox, eggs as eggs, random
import tkinter.font as tkFont, EDF_ModloaderHeadFunc as funcs, ImageResources as img_res
from PIL import Image, ImageTk, ImageFont
from ImageResources import *
from EDF_ModloaderHeadFunc import *
from collections import defaultdict

'''
#TODO
Conflict Detection
Load Order Management
Are not implemented yet, but are planned for future releases.

get coding support for nexus, and GET PREMIUM PAYWALL YEETED INTO THE SUN, ie paying once for a lifetime of premium support. Or plugin you'r
finalize R2Modman code share support for MML, IE UUID SUPPORT.
EDF EDF EDF

EarthDefenseForceModloaderHead.py
🚨 EDF 6 Thunderstore Page Support Needed
EDF 6 Thunderstore (to be created)
A dedicated EDF 6 page will centralize the modded multiplayer EDF community!

Existing pages for reference:

EDF 5 Thunderstore
EDF 4.1 Thunderstore
🌟 EDF Multi-Mod-Loader (MML) Ecosystem Overview
EDF Multi-Mod-Loader (MML) is a comprehensive, AI- and community-driven, open-source Python application for managing mods, patches, and plugins for Earth Defense Force 6 (EDF 6), built on top of Blue Amulet’s Modloader for the EDF XGS engine.
MML features a robust, Tkinter-based GUI and supports both Steam and Epic versions of EDF 6.
It is extensible for EDF 4.1 and 5, but not supported at the moment and will need additional logic for missing features.

🖥️ Key Features
LanguageManager: Dynamic loading and switching of UI translations from JSON files.
Customizable UI: Theme colors, font sizes, and background images (random/manual selection).
Game Management: Launches EDF games via Steam/Epic, manages modloader status, and provides quick access to save folders.
Mod Management: Displays mod/patch/plugin counts, enables folder access, and supports mod importing via .r2z files (R2Modman profiles or drag-and-drop).
Update System: Checks for and downloads updates for both MML and BlueAmulet's EDFModLoader.
Batch File Execution: Runs specified .bat files for building itself and related scripts.
Social & Documentation Links: Grouped links to official channels, documentation, and community resources.
Console & Logging: Scrollable console for status messages, errors, and command outputs.
Easter Eggs: Hidden commands and fun features for users to discover.
🏗️ Structure
Global configuration and color/theme management.
Language and font management utilities.
Core UI construction functions (create_ui, create_game_launch_bar, etc.).
Mod and game management logic (update_mods, build_tables, repair_tables, etc.).
Event handlers for user actions and command processing.
Helper functions for background images, tooltips, and error handling.
🚧 Current Status
MML is mostly ready for use!
Robust mod importing, patching, and management features.
.r2z zip file support for R2Modman profiles (UUID code sharing not yet implemented).
Modded public lobbies are forced to be private for stability and safety.
Save editor is not yet implemented, but close to being ready.
All information here is to inform what has been developed so far and what is possible with the current toolset.
Some advanced features (conflict detection, load order management) are planned for future releases.
The HAKKEN engine is currently Python-based and may be replaced with a C language version for performance.
The code is modular, extensible, and open to community contributions.
CustomTkinter is planned for a more modern, user-friendly look while keeping the EDF series UI style.
📦 What gets loaded on R2Modman servers for EDF?
Mod_config_data.json (MCD):
Each mod is defined by a (ModNameHere)Mod_config_data.json file—a combinable metadata/config table for new weapons/categories, mission packs, UI/subtitle text, and uninstall manifests.

Main tree paths in Mod_config_data.json:

MOD_INFO: Author, mod name, version, download link, and small notes (not a changelog).
DataReplacementTable: Text or data patches.
NewToAddTextTableEntries: New UI/localization text.
NewToAddModeList: Custom mission pack pairs for online and offline. (Modded mission pack saves are incomplete.)
NewToAddSoldierWeaponCategory & NewToAddWeaponCatalog: New weapon slots and assignments.
NewToAddWeaponTables: New weapons and stats.
DirManifestToFilesUninstaller: Uninstall manifest.
CHANGELOG: Version history.
Documentation:
A detailed guide (Notes.txt) is included, explaining every section of the config file, best practices, and how to use the loader and "HAKKEN" core tools.
'''

class LanguageManager:
    def __init__(self, default_language="en"):
        self.current_language = default_language
        self.translations = {}
        self.language_dir = os.path.join(os.path.dirname(__file__), "languages")
        self.load_translations(default_language)

    def load_translations(self, language_code):
        lang_file = os.path.join(self.language_dir, f"{language_code}.json")
        try:
            if os.path.exists(lang_file):
                with open(lang_file, "r", encoding="utf-8") as f:
                    self.translations = json.load(f)
                self.current_language = language_code
                print(f"Loaded translations for language: {language_code}")
            else:
                print(f"Language file {lang_file} not found. Falling back to English.")
                self.load_translations("en")
        except Exception as e:
            print(f"Error loading translations for {language_code}: {e}")
            if language_code != "en":
                self.load_translations("en")

    def get(self, key, **kwargs):
        text = self.translations.get(key, key)
        try:
            return text.format(**kwargs) if kwargs else text
        except KeyError:
            print(f"Warning: Missing format variables for key '{key}'")
            return text

# Initialize language manager
lang_manager = LanguageManager(settings.get("language", "en"))
translatable_widgets = []

def get_version():
    return "0.0.9.2-LARGE QUACK"

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

# Shared request input variable to ensure handlers always read current text
request_code_var = tk.StringVar()
request_code_entry = None  # will hold the Entry widget instance for direct reads

# Command usage stats for normalized_code function tree
command_counts = defaultdict(int)

RUN_BAT_FILES_ENABLED = True  # Set to False to hide the debug button for build HAKKEN exe button or other MML batch files

BAT_FILES_DIRS = ( # Change this to where the batch files you want run here
    r"F:\SteamLibrary\steamapps\common\EARTH DEFENSE FORCE 6", # ALL FILES TO DO MML EXPORT DIR
    r"F:\SteamLibrary\steamapps\common\EARTH DEFENSE FORCE 6\Mods\EDF 6 MOD SETTINGS MAKER", # HAKKEN DIR
    r"F:\SteamLibrary\steamapps\common\EARTH DEFENSE FORCE 6\EDF_ModloaderHead_B", #MML DIR
)

EXCLUDED_BAT_FILES = { #
    "Python Install PREREQUISETS.bat",  # BLACK list any batch files you want to exclude here
}

def increment_cmd(tag):
    command_counts[tag] += 1

def render_command_stats():
    show_error("=== Request command usage ===")
    total = command_counts.get("total", 0)
    show_error(f"total: {total}")
    # Sort by count desc, then name
    for key, val in sorted([(k, v) for k, v in command_counts.items() if k != "total"], key=lambda kv: (-kv[1], kv[0])):
        show_error(f"{key}: {val}")

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

        clear_error()
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
            pil_font = ImageFont.truetype(font_path, size)
            custom_font = tkFont.Font(family=pil_font.getname()[0], size=size)
            return custom_font
        except Exception as e:
            print(f"Error loading custom font: {e}. Using default font.")
            return tkFont.Font(size=size)
    else:
        print(f"Font file not found at {font_path}. Using default font.")
        return tkFont.Font(size=size)

def update_global_fonts():
    global global_font, global_font_h
    settings = funcs.get_settings()
    font_sizes = settings.get("font_sizes", {"global_font": 10, "global_font_h": 12})
    global_font = load_custom_font(font_sizes.get("global_font", 10))
    global_font_h = load_custom_font(font_sizes.get("global_font_h", 12))
    # Reapply fonts to all widgets (this requires iterating over translatable_widgets)
    for item in translatable_widgets:
        attr, widget, key, kwargs = item if len(item) == 4 else (item[0], item[1], item[2], {})
        if attr in ['text', 'textvariable']:
            if 'font' in widget.keys():
                widget.config(font=global_font if attr == 'text' else global_font_h)

def set_font_size(font_key, size):
    settings = funcs.get_settings()
    settings["font_sizes"] = settings.get("font_sizes", {"global_font": 10, "global_font_h": 12})
    settings["font_sizes"][font_key] = size
    with open("MMLsettings.json", "w") as f:
        json.dump(settings, f, indent=4)
    update_global_fonts()

update_global_fonts()
global_fill_color = TextColor()

def get_button_style(command=None, translation_key=None):
    style = {
        'font': global_font,
        'bg': ButtonBackGround(),
        'fg': TextColor(),
        'activebackground': ButtonPressedBackGround(),
        'activeforeground': PressedTextColor(),
        'relief': 'groove',
        'bd': 2,
        'cursor': 'hand2'
    }
    if command:
        style['command'] = command
    tooltip_text = lang_manager.get(f"tooltip_{translation_key}") if translation_key else None
    return style, tooltip_text

def apply_hover_and_tooltip(widget, tooltip_text=None, hover_bg=None, hover_fg=None, normal_bg=None, normal_fg=None):
    """Apply hover effect and tooltip to a widget with unified event handling and debounce."""
    # Skip if no effects are needed
    if not tooltip_text and not (hover_bg or hover_fg):
        return
    
    # Use settings for hover colors if not provided
    hover_bg = hover_bg or settings.get("colors", {}).get("hover_bg", "#555555")
    hover_fg = hover_fg or settings.get("colors", {}).get("hover_fg", "#ffffff")
    
    # Use current widget colors if not provided
    normal_bg = normal_bg or widget.cget("bg")
    normal_fg = normal_fg or widget.cget("fg")
    
    # Store normal colors to prevent override issues
    if not hasattr(widget, "_normal_bg"):
        widget._normal_bg = normal_bg
        widget._normal_fg = normal_fg
    
    # Create tooltip window if tooltip_text is provided
    tooltip = None
    if tooltip_text:
        tooltip = tk.Toplevel(widget)
        tooltip.withdraw()
        tooltip.wm_overrideredirect(True)
        
        label = tk.Label(
            tooltip,
            text=tooltip_text,
            bg=settings.get("colors", {}).get("tooltip_bg", "#333333"),
            fg=settings.get("colors", {}).get("tooltip_fg", "#ffffff"),
            font=load_custom_font(10),
            bd=1,
            relief="solid",
            padx=4,
            pady=2,
            wraplength=300
        )
        label.pack()
        widget.tooltip_window = tooltip  # Store reference to prevent garbage collection
    
    def on_enter(event):
        # Apply hover effect immediately
        widget.config(bg=hover_bg, fg=hover_fg)
        
        # Show tooltip with a 200ms delay
        if tooltip:
            def show_tooltip():
                if not hasattr(widget, "tooltip_visible") or not widget.tooltip_visible:
                    x = widget.winfo_rootx() + event.x + 5
                    y = widget.winfo_rooty() + event.y + 5
                    
                    # Keep tooltip within screen bounds
                    screen_width = widget.winfo_screenwidth()
                    screen_height = widget.winfo_screenheight()
                    tooltip_width = label.winfo_reqwidth()
                    tooltip_height = label.winfo_reqheight()
                    
                    if x + tooltip_width > screen_width:
                        x = widget.winfo_rootx() - tooltip_width - 5
                    if y + tooltip_height > screen_height:
                        y = widget.winfo_rooty() - tooltip_height - 5
                    
                    tooltip.wm_geometry(f"+{x}+{y}")
                    tooltip.deiconify()
                    widget.tooltip_visible = True
            
            # Cancel any existing tooltip delay
            if hasattr(widget, "tooltip_id"):
                widget.after_cancel(widget.tooltip_id)
            widget.tooltip_id = widget.after(200, show_tooltip)
    
    def on_leave(event):
        # Revert hover effect
        widget.config(bg=widget._normal_bg, fg=widget._normal_fg)
        
        # Hide tooltip and cancel any pending show
        if tooltip:
            tooltip.withdraw()
            widget.tooltip_visible = False
            if hasattr(widget, "tooltip_id"):
                widget.after_cancel(widget.tooltip_id)
    
    # Remove existing bindings to prevent duplicates
    widget.unbind("<Enter>")
    widget.unbind("<Leave>")
    
    # Apply unified bindings
    widget.bind("<Enter>", on_enter)
    widget.bind("<Leave>", on_leave)

def get_label_style():
    """Returns common style options for labels."""
    return {
        'font': global_font_h,
        'bg': JustBackGround(),
        'fg': TextColor()
    }

def get_label_style_alt(command=None, translation_key=None):
    style = {
        'font': global_font,
        'bg': TextColor(),
        'fg': ButtonBackGround(),
        'activebackground': PressedTextColor(),
        'activeforeground': ButtonPressedBackGround()
    }
    if command:
        style['command'] = command
    tooltip_text = lang_manager.get(f"tooltip_{translation_key}") if translation_key else None
    return style, tooltip_text

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
    return text_id  # Return the text item ID for later updates

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
    "Get Into Modding / Useful Links": [
        ("Documentation / Wiki", "https://github.com/KCreator/Earth-Defence-Force-Documentation/wiki"),
        ("Maybe Birb's Guide on 'HOW TO MOD EDF'", "https://steamcommunity.com/sharedfiles/filedetails/?id=3083510169"),
        ("Loadout Planner / Mission Database", "https://invadersfromplanet.space/"),
    ],
    "Blue Amulet's Modloader": [
        ("Source Code", "https://github.com/BlueAmulet/EDFModLoader")
    ],
    "Official EDF Channel's Socials": [
        ("Official EDF EN on X", "https://x.com/EDF_OFFICIAL_EN"),
        ("Official EDF JP on X", "https://x.com/EDF_OFFICIAL"),
        ("Official EDF Reddit", "https://www.reddit.com/r/EDF/"),
        ("Official EDF Discord", "https://discord.com/invite/EDF"),
        ("Official EDF Wiki", "https://theearthdefenseforce.fandom.com/"),
    ],
    "FevGrave's Socials": [
        ("X", "https://x.com/FevGrave"),
        ("Reddit", "https://www.reddit.com/user/FevGrave/"),
        ("MML Source Code", "https://github.com/FevGrave/EDFMultiModLoader"),
        ("Discord Model / Thumbnail Request Form", "https://discord.com/channels/207292314064781312/1272000404875378718"),
        ("Discord MML Form", "https://discord.com/channels/207292314064781312/1284693030003019797"),
        ("Ko-Fi", "https://ko-fi.com/D1D41FKS1S"),
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
        show_error(f"Detected current_game: {current_game}")
        break
print(f"Current game detected: {current_game}")  # Add this

def get_game_dir():
    settings = funcs.get_settings()
    base_dir = settings.get("base_dir", "")
    script_dir = os.path.dirname(os.path.abspath(__file__ if '__file__' in globals() else sys.executable))
    
    # Try base_dir from settings
    if base_dir and os.path.isdir(base_dir):
        mods_dir = os.path.join(base_dir, "Mods", "EDF 6 MOD SETTINGS MAKER")
        if os.path.isdir(mods_dir):
            return base_dir
    
    # Fallback to script_dir or common Steam paths
    potential_paths = [
        script_dir,
        os.path.join(script_dir, ".."),
        os.path.join(script_dir, "..", ".."),
        r"F:\SteamLibrary\steamapps\common",
        r"C:\Program Files (x86)\Steam\steamapps\common"
    ]
    
    for path in potential_paths:
        for game_name in GAME_FOLDERS.keys():
            full_path = os.path.normpath(os.path.join(path, game_name))
            if os.path.isdir(full_path):
                mods_dir = os.path.join(full_path, "Mods", "EDF 6 MOD SETTINGS MAKER")
                if os.path.isdir(mods_dir):
                    global current_game
                    current_game = game_name
                    settings["base_dir"] = full_path
                    with open("MMLsettings.json", "w") as f:
                        json.dump(settings, f, indent=4)
                    return full_path
    
    # Log failure and return script_dir as last resort
    show_error(f"Warning: Could not find valid game directory. Using script directory: {script_dir}")
    return script_dir

# Set the taskbar and title bar images
set_icons(root, BASE_DIR)

# Load the background image
if os.path.exists(bg_image_path):
    bg_photo = load_resized_background_image(bg_image_path, width(), height())
else:
    print(f"Background image not found: {bg_image_path}")
    bg_photo = None

# Create a canvas and set the background image
canvas = tk.Canvas(root, width=width(), height=height())
canvas.pack(fill="both", expand=True)
if bg_photo:
    canvas.create_image(0, 0, image=bg_photo, anchor="nw")

def set_random_background_image():
    global bg_photo
    image_path = get_random_background_path()
    if not image_path or not os.path.exists(image_path):
        show_error("⚠️ Failed to select a valid background image.")
        return

    try:
        new_bg = Image.open(image_path).convert("RGBA")
        new_bg_resized = new_bg.resize((width(), height()), Image.Resampling.LANCZOS)  # Resize to 675x920
        bg_photo = ImageTk.PhotoImage(new_bg_resized)

        canvas.delete("background")  # Clear previous background
        bg_id = canvas.create_image(0, 0, image=bg_photo, anchor="nw", tags="background")
        canvas.tag_lower(bg_id)  # Ensure it’s behind all GUI widgets

        show_error(f"✅ Random background image applied: {os.path.basename(image_path)}")
    except Exception as e:
        show_error(f"❌ Failed to load image: {str(e)}")

def set_background_image_manual(image_name):
    global bg_photo  # Keep image alive to prevent garbage collection

    # Check allowed extensions
    valid_extensions = ('.jpg', '.jpeg', '.png', '.webp')
    if not image_name.lower().endswith(valid_extensions):
        show_error(f"❌ Unsupported image format: '{image_name}'. Use JPG, PNG, or WEBP.")
        return

    # Resolve image path
    if os.path.exists(os.path.join(custom_images_dir, image_name)):
        image_path = os.path.join(custom_images_dir, image_name)
    elif os.path.exists(os.path.join(images_dir, image_name)):
        image_path = os.path.join(images_dir, image_name)
    else:
        show_error(f"❌ Image '{image_name}' not found in custom or default folders.")
        return

    try:
        # Open and resize the image
        new_bg = Image.open(image_path).convert("RGBA")
        new_bg_resized = new_bg.resize((width(), height()), Image.Resampling.LANCZOS)
        bg_photo = ImageTk.PhotoImage(new_bg_resized)

        canvas.delete("background")  # Clear previous background
        bg_id = canvas.create_image(0, 0, image=bg_photo, anchor="nw", tags="background")
        canvas.tag_lower(bg_id)  # Push behind widgets

        show_error(f"✅ Background changed to '{image_name}'")
    except Exception as e:
        show_error(f"❌ Failed to load image: {str(e)}")

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

def check_for_update(prefer_prerelease=True):
    clear_error()
    try:
        gui_release_api_url = 'https://api.github.com/repos/FevGrave/EDFMultiModLoader/releases'
        headers = {'Accept': 'application/vnd.github.v3+json'}
        
        response = requests.get(gui_release_api_url, headers=headers)
        response.raise_for_status()
        releases = response.json()
        
        # Determine which release to check for
        if prefer_prerelease:
            latest_release = next((release for release in releases if not release.get('prerelease', False)), None)
            release_type = "stable release"
        else:
            latest_release = next((release for release in releases if release.get('prerelease', False)), None)
            release_type = "pre-release"
        
        if not latest_release:
            show_error(f"No {release_type} found.")
            return
        
        latest_version = latest_release.get('tag_name', '0.0.0').strip()
        assets = latest_release.get('assets', [])
        current_version = get_version().strip()

        if current_version == latest_version:
            show_error("You are using the latest EDF Multi Mod Loader version.")
            show_error("Use the cmds of 'help', 'h', 'HELP' in the Request Mod Code")
            show_error("changelog.txt")
        elif current_version < latest_version:
            update_prompt = messagebox.askyesno(
                "EDF MML Update Available",
                f"{release_type.capitalize()} version {latest_version} is available! You are currently using {current_version}. Do you want to update now?"
            )
            if update_prompt:
                executable_name = "EDF MML.exe"
                download_url = next((asset['browser_download_url'] for asset in assets if asset['name'] == executable_name), None)

                if download_url:
                    download_and_replace_executable(download_url, executable_name)
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
        ml_release_api_url = 'https://api.github.com/repos/BlueAmulet/EDFModLoader/releases/latest'
        response = requests.get(ml_release_api_url)
        response.raise_for_status()
        data = response.json()
        latest_version = data['tag_name']
        assets = data['assets']
        extract_to = get_game_dir()
        print(f"Using extract_to for check_for_ba_update: {extract_to}")  # Debug

        zip_targets = {
            "EDFModLoader.zip": None,
            "Plugins6.zip": "EARTH DEFENSE FORCE 6",
            "Plugins5.zip": "EARTH DEFENSE FORCE 5",
            "Plugins41.zip": "EARTH DEFENSE FORCE 4.1"
        }

        for zip_name, game_filter in zip_targets.items():
            if game_filter and current_game != game_filter:
                continue
            for asset in assets:
                if asset['name'] == zip_name:
                    zip_url = asset['browser_download_url']
                    funcs.download_and_extract_zip(zip_url, zip_name, extract_to, show_error)
                    break
            else:
                show_error(f"{zip_name} not found in GitHub release.")

        show_error(f"Updated to version {latest_version} completed.")
        ep = os.path.join(extract_to, "Mods", "ExtraPatches")
        dp = os.path.join(extract_to, "Mods", "DisabledPatches")
        if os.path.exists(ep):
            if os.path.exists(dp): 
                shutil.rmtree(dp)
            os.rename(ep, dp)
            show_error('Renamed "ExtraPatches" to "DisabledPatches".')
        else:
            show_error('"ExtraPatches" folder not found.')
    except requests.exceptions.RequestException as e:
        show_error(f"Update failed: {str(e)}")
    except Exception as e:
        show_error(f"Unexpected error: {str(e)}")

def update_mods():
    update_mod_counts()
    clear_error()
    try:
        parent_dir = get_game_dir()
        print(f"Using parent_dir for update_mods: {parent_dir}")  # Debug
        funcs.update_mods(show_error, parent_dir=parent_dir)
    except Exception as e:
        show_error(f"Failed to update mods: {str(e)}")

def build_tables():
    update_mod_counts()
    clear_error()
    show_error("Generating Content Please Wait...")
    error_block.update()
    threading.Thread(target=run_build_tables).start()

def run_build_tables():
    try:
        current_dir = os.getcwd()
        print(f"Current directory: {current_dir}")  # Debug
        settings = load_settings(current_dir)
        if settings is None:
            raise ValueError("Failed to load settings")
        
        modloader_style = settings.get("modloader_HAKKEN_style", "NI")
        exe_name = "EDF HAKKEN NI.exe" if modloader_style == "NI" else "EDF HAKKEN.exe"
        print(f"Selected EXE: {exe_name}")  # Debug
        
        show_error(f"Starting build process using: {exe_name}")
        funcs.build_tables(show_error, exe_name=exe_name)
        clear_error()
        show_error("Build process completed successfully.")
    except Exception as e:
        show_error(f"An error occurred during the build process: {str(e)}")
        error_block.update()

def repair_tables():
    clear_error()
    try:
        current_dir = get_game_dir()
        print(f"Using current_dir for repair_tables: {current_dir}")  # Debug
        show_error("Starting table repair process...")
        if not current_dir or not os.path.isdir(current_dir):
            raise ValueError(f"Invalid game directory: {current_dir}")
        funcs.repair_tables(show_error, current_dir)
    except Exception as e:
        show_error(f"Failed to repair tables: {str(e)}")
        
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
        parent_dir = get_game_dir()
        print(f"Using parent_dir for update_mods: {parent_dir}")  # Debug
        funcs.update_mods(show_error, parent_dir=parent_dir)
    except Exception as e:
        show_error(f"Failed to update mods: {str(e)}")

def build_tables():
    update_mod_counts()
    clear_error()  # Clear errors first
    show_error("Generating Content Please Wait...")
    error_block.update()  # Update the UI

    # Run the task in a separate thread
    threading.Thread(target=run_build_tables).start()

def run_build_tables():
    try:
        # Load settings to check modloader_HAKKEN_style
        current_dir = os.getcwd()
        print(f"Current directory: {current_dir}")  # Debug
        settings = load_settings(current_dir)
        if settings is None:
            raise ValueError("Failed to load settings")
        
        modloader_style = settings.get("modloader_HAKKEN_style", "NI")  # Default to "NI"
        exe_name = "EDF HAKKEN NI.exe" if modloader_style == "NI" else "EDF HAKKEN.exe"
        print(f"Selected EXE: {exe_name}")  # Debug
        
        # Pass the selected EXE to build_tables
        show_error(f"Starting build process using: {exe_name}")
        funcs.build_tables(show_error, exe_name=exe_name)
        show_error("Build process completed successfully.")
    except Exception as e:
        show_error(f"An error occurred during the build process: {str(e)}")
        error_block.update()

def repair_tables():
    clear_error()
    try:
        current_dir = get_game_dir()
        print(f"Using current_dir for repair_tables: {current_dir}")  # Debug
        if not current_dir or not os.path.isdir(current_dir):
            raise ValueError(f"Invalid game directory: {current_dir}")
        funcs.repair_tables(show_error, current_dir)
    except Exception as e:
        show_error(f"Failed to repair tables: {str(e)}")

def create_mml_installer_tools(canvas, y_pos):
    def check_for_ba_update():
        clear_error()
        try:
            ml_release_api_url = 'https://api.github.com/repos/BlueAmulet/EDFModLoader/releases/latest'
            response = requests.get(ml_release_api_url)
            response.raise_for_status()
            data = response.json()
            latest_version = data['tag_name']
            assets = data['assets']
            extract_to = r'F:\\SteamLibrary\\steamapps\\common\\EARTH DEFENSE FORCE 6'

            zip_targets = {
                "EDFModLoader.zip": None,
                "Plugins6.zip": "EARTH DEFENSE FORCE 6",
                "Plugins5.zip": "EARTH DEFENSE FORCE 5",
                "Plugins41.zip": "EARTH DEFENSE FORCE 4.1"
            }

            for zip_name, game_filter in zip_targets.items():
                if game_filter and current_game != game_filter:
                    continue
                for asset in assets:
                    if asset['name'] == zip_name:
                        zip_url = asset['browser_download_url']
                        funcs.download_and_extract_zip(zip_url, zip_name, extract_to, show_error)
                        break
                else:
                    show_error(f"{zip_name} not found in GitHub release.")

            show_error(f"Updated to version {latest_version} completed.")
            ep = os.path.join(extract_to, "Mods", "ExtraPatches")
            dp = os.path.join(extract_to, "Mods", "DisabledPatches")
            if os.path.exists(ep):
                if os.path.exists(dp): shutil.rmtree(dp)
                os.rename(ep, dp)
                show_error('Renamed "ExtraPatches" to "DisabledPatches".')
            else:
                show_error('"ExtraPatches" folder not found.')
        except requests.exceptions.RequestException as e:
            show_error(f"Update failed: {str(e)}")
        except Exception as e:
            show_error(f"Unexpected error: {str(e)}")

    def update_mods():
        update_mod_counts()
        clear_error()
        try:
            parent_dir = get_game_dir()
            print(f"Using parent_dir for update_mods: {parent_dir}")  # Debug
            funcs.update_mods(show_error, parent_dir=parent_dir)
        except Exception as e:
            show_error(f"Failed to update mods: {str(e)}")

    def run_build_tables():
        try:
            settings = load_settings(os.getcwd())
            style = settings.get("modloader_HAKKEN_style", "NI")
            exe_name = "EDF HAKKEN NI.exe" if style == "NI" else "EDF HAKKEN.exe"
            show_error(f"Starting build: {exe_name}")
            funcs.build_tables(show_error, exe_name=exe_name)
            show_error("Build process completed.")
        except Exception as e:
            show_error(f"Build error: {str(e)}")
            error_block.update()

    def build_tables():
        update_mod_counts()
        clear_error()
        show_error("Generating content...")
        error_block.update()
        threading.Thread(target=run_build_tables).start()

    def repair_tables():
        clear_error()
        try:
            current_dir = get_game_dir()
            print(f"Using current_dir for repair_tables: {current_dir}")  # Debug
            if not current_dir or not os.path.isdir(current_dir):
                raise ValueError(f"Invalid game directory: {current_dir}")
            funcs.repair_tables(show_error, current_dir)
        except Exception as e:
            show_error(f"Failed to repair tables: {str(e)}")

    tools_frame = tk.Frame(root, bg=bgY())
    buttons = [
        ("update_modloader_ba", check_for_ba_update, "update_modloader_ba"),
        ("update_mods", update_mods, "update_mods"),
        ("build_tables", build_tables, "build_tables"),
        ("repair_tables", repair_tables, "repair_tables"),
        ("mods_panel", lambda: toggle_mods_panels(show_error), "mods_panel")
    ]
    for idx, (translation_key, cmd, tooltip_key) in enumerate(buttons):
        style, tooltip = get_label_style_alt(cmd, tooltip_key)
        b = tk.Button(tools_frame, text=lang_manager.get(translation_key), **style)
        apply_hover_and_tooltip(b, tooltip)
        translatable_widgets.append(('text', b, translation_key))
        b.pack(side="left", padx=get_padding(idx, len(buttons)))
    canvas.create_window(width() // 2, y_pos, window=tools_frame, anchor="center")
    return y_pos + 30

def create_game_launch_bar(canvas, y_position):
    global translatable_widgets, toggle_button
    # Add a label above the dropdown, play button, toggle button, and progress tracker button
    label = tk.Label(
        root,
        text=lang_manager.get("edf_game_to_launch"),
        font=global_font_h,
        bg=JustBackGround(),
        fg=TextColor(),
    )
    translatable_widgets.append(('text', label, "edf_game_to_launch"))
    canvas.create_window(width() // 2, y_position, window=label)
    y_position += 35

    # Create a frame for all elements in this section
    game_launch_frame = tk.Frame(root, bg=bgY(), highlightthickness=0)

    # Dropdown menu for selecting games
    selected_game = tk.StringVar(value="Earth Defense Force 6")
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
    apply_hover_and_tooltip(game_dropdown, lang_manager.get("tooltip_game_dropdown"))
    game_dropdown.pack(side="left", padx=(2, 5))

    # Add the "Play This Game" button
    def handle_launch():
        game_key = selected_game.get()
        app_ids = GAME_FOLDERS.get(game_key)
        if not app_ids:
            show_error(f"Game '{game_key}' not found in GAME_FOLDERS.")
            return
        if len(app_ids) == 1:
            funcs.launch_game([app_ids[0]], show_error)
        else:
            if platform_choice == "epic" and len(app_ids) > 1:
                funcs.launch_game(app_ids, show_error)
            else:
                funcs.launch_game([app_ids[0]], show_error)

    style, tooltip = get_label_style_alt(command=handle_launch, translation_key="play_this_game")
    play_button = tk.Button(game_launch_frame, text=lang_manager.get("play_this_game"), **style)
    apply_hover_and_tooltip(play_button, tooltip)
    translatable_widgets.append(('text', play_button, "play_this_game"))
    play_button.pack(side="left", padx=(5, 5))

    # Toggle button
    style, tooltip = get_button_style(command=toggle_platform, translation_key="current_platform")
    toggle_button = tk.Button(
        game_launch_frame,
        text=lang_manager.get("current_platform", platform=platform_choice.capitalize()),
        **style
    )
    apply_hover_and_tooltip(toggle_button, tooltip)
    translatable_widgets.append(('text', toggle_button, "current_platform", {'platform': platform_choice.capitalize()}))
    toggle_button.pack(side="left", padx=(5, 5))

    # Progress tracker button
    style, tooltip = get_label_style_alt(command=launch_progress_tracker, translation_key="online_progress_tracker")
    progress_tracker_button = tk.Button(game_launch_frame, text=lang_manager.get("online_progress_tracker"), **style)
    apply_hover_and_tooltip(progress_tracker_button, tooltip)
    translatable_widgets.append(('text', progress_tracker_button, "online_progress_tracker"))
    progress_tracker_button.pack(side="left", padx=(5, 0))

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

def update_modloader_status():
    try:
        current_status = funcs.get_modloader_status()
        modloader_status.set(lang_manager.get("toggle_modloader_status", status=current_status))
        # Update translatable_widgets entry for the modloader toggle button
        if modloader_toggle_button:
            for i, item in enumerate(translatable_widgets):
                if item[1] == modloader_toggle_button:
                    translatable_widgets[i] = ('textvariable', modloader_toggle_button, "toggle_modloader_status", {'status': current_status})
                    break
            update_ui_translations()  # Reapply all translations to ensure consistency
    except Exception as e:
        show_error(str(e))

def show_error(error_key_or_msg, **kwargs):
    error_block.config(state=tk.NORMAL)
    text = lang_manager.get(error_key_or_msg, **kwargs) if error_key_or_msg in lang_manager.translations else error_key_or_msg
    error_block.insert(tk.END, text + '\n')
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
    global mods_button, patches_button, plugins_button
    mods_frame = tk.Frame(root, bg=bgY())

    # MODS BUTTON and LABEL
    style, tooltip = get_button_style(command=lambda: open_mod_folder(r"Mods\EDF 6 MOD SETTINGS MAKER\MOD CONFIG DATA PLACED HERE"), translation_key="mods")
    mods_button = tk.Button(mods_frame, text=lang_manager.get("mods"), **style)
    apply_hover_and_tooltip(mods_button, tooltip)
    translatable_widgets.append(('text', mods_button, "mods"))
    mods_button.pack(side="left", padx=(0, 2))
    
    total_mods_label = tk.Label(mods_frame, textvariable=total_mods, **get_label_style())
    total_mods_label.pack(side="left", padx=(0, 2))

    # PATCHES BUTTON and LABEL
    style, tooltip = get_button_style(command=lambda: open_mod_folder(r"Mods\Patches"), translation_key="patches")
    patches_button = tk.Button(mods_frame, text=lang_manager.get("patches"), **style)
    apply_hover_and_tooltip(patches_button, tooltip)
    translatable_widgets.append(('text', patches_button, "patches"))
    patches_button.pack(side="left", padx=(0, 2))
    
    total_patches_label = tk.Label(mods_frame, textvariable=total_patches, **get_label_style())
    total_patches_label.pack(side="left", padx=(0, 2))

    # PLUGINS BUTTON and LABEL
    style, tooltip = get_button_style(command=lambda: open_mod_folder(r"Mods\Plugins"), translation_key="plugins")
    plugins_button = tk.Button(mods_frame, text=lang_manager.get("plugins"), **style)
    apply_hover_and_tooltip(plugins_button, tooltip)
    translatable_widgets.append(('text', plugins_button, "plugins"))
    plugins_button.pack(side="left", padx=(0, 2))
    
    total_plugins_label = tk.Label(mods_frame, textvariable=total_plugins, **get_label_style())
    total_plugins_label.pack(side="left", padx=(0, 2))

    labels_and_buttons.append(canvas.create_window(width() // 2, y_position, window=mods_frame))
    return y_position + 35

def toggle_platform():
    global platform_choice, toggle_button
    platform_choice = "epic" if platform_choice == "steam" else "steam"
    settings = get_settings()
    settings["edf6_platform"] = platform_choice
    save_settings(settings)
    if toggle_button:
        toggle_button.config(text=lang_manager.get("current_platform", platform=platform_choice.capitalize()))
        # Update translatable_widgets entry
        for i, item in enumerate(translatable_widgets):
            if item[1] == toggle_button:
                translatable_widgets[i] = ('text', toggle_button, "current_platform", {'platform': platform_choice.capitalize()})
                break

def create_mod_hosting_services(canvas, y_position):
    y_pos = y_position
    print(f"Mod Hosting Services y_pos start: {y_pos}")  # Debug

    # Note: Header is now in create_ui, so this function only handles the frame
    hosting_frame = tk.Frame(root, bg=bgY())
    selected_game = tk.StringVar(value="Earth Defense Force 6")

    def update_links(selected_game):
        print(f"Updating links for game: {selected_game}")  # Debug
        for widget in dynamic_links_frame.winfo_children():
            widget.destroy()
        links = game_to_mod_host_links.get(selected_game, [])
        print(f"Links found: {links}")  # Debug
        if not links:
            tk.Label(dynamic_links_frame, text=lang_manager.get("no_mod_hosting_available"), bg=bgY(), fg=TextColor()).pack(side="left")
            translatable_widgets.append(('text', dynamic_links_frame.winfo_children()[0], "no_mod_hosting_available", {}))
        for i, (label, url) in enumerate(links):
            label_key = label.lower().replace(" ", "_")  # e.g., "Nexus Mods" -> "nexus_mods"
            style, _ = get_button_style(command=lambda u=url: open_link(u))
            button = tk.Button(dynamic_links_frame, text=lang_manager.get(label_key), **style)
            apply_hover_and_tooltip(button, lang_manager.get("tooltip_mod_hosting_link", label=lang_manager.get(label_key), game=selected_game))
            translatable_widgets.append(('text', button, label_key, {}))
            button.pack(side="left", padx=get_padding(i, len(links)))
        dynamic_links_frame.update()

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
    apply_hover_and_tooltip(dropdown, lang_manager.get("tooltip_game_dropdown"))
    translatable_widgets.append(('text', dropdown, "tooltip_game_dropdown", {}))
    dropdown.pack(side="left", padx=(2, 5))

    dynamic_links_frame = tk.Frame(hosting_frame, bg=bgY())
    dynamic_links_frame.pack(side="left", padx=5)

    style, tooltip = get_label_style_alt(command=import_local_r2z, translation_key="import_r2z")
    import_r2z_button = tk.Button(hosting_frame, text=lang_manager.get("import_r2z"), **style)
    apply_hover_and_tooltip(import_r2z_button, tooltip)
    translatable_widgets.append(('text', import_r2z_button, "import_r2z", {}))
    import_r2z_button.pack(side="left", padx=(5, 0))

    update_links(selected_game.get())
    canvas.create_window(width() // 2, y_pos, window=hosting_frame, anchor="center")
    print(f"Hosting frame placed at y_pos: {y_pos}")  # Debug
    return y_pos

def import_local_r2z():
    """Open a file dialog to select a .r2z file, move it to Ziped_Mods, and process it."""
    clear_error()
    try:
        # Open file dialog to select .r2z file
        file_path = filedialog.askopenfilename(
            title="Select R2Z Profile File",
            filetypes=[("R2Z Files", "*.r2z"), ("All Files", "*.*")]
        )
        if not file_path:
            show_error("⚠️ No file selected.")
            return

        # Validate file extension
        if not file_path.lower().endswith(".r2z"):
            show_error("❌ Selected file is not a .r2z file.")
            return

        # Generate a UUID-like identifier from the filename (or use a random UUID)
        uuid_code = os.path.splitext(os.path.basename(file_path))[0]
        if not re.match(r"^[0-9a-fA-F\-]{36}$", uuid_code):
            uuid_code = str(uuid.uuid4())  # Fallback to random UUID if filename isn't UUID-like

        # Target directory
        target_dir = os.path.join(os.getcwd(), "Ziped_Mods")
        os.makedirs(target_dir, exist_ok=True)
        target_path = os.path.join(target_dir, f"{uuid_code}.r2z")

        # Move or copy the file to Ziped_Mods
        if os.path.abspath(file_path) != os.path.abspath(target_path):
            shutil.copy2(file_path, target_path)
            show_error(f"✅ Copied .r2z file to: {target_path}")
        else:
            show_error(f"ℹ️ .r2z file already at target location: {target_path}")

        # Verify file is a valid zip and list contents
        try:
            with zipfile.ZipFile(target_path, 'r') as z:
                contents = z.namelist()
                show_error(f"📦 Zip contents: {contents}")
        except zipfile.BadZipFile:
            show_error(f"❌ The selected file is not a valid zip archive.")
            os.remove(target_path)  # Clean up invalid file
            return

        # Call funcs.process_r2z_profile to unpack and process
        if hasattr(funcs, 'process_r2z_profile'):
            show_error("ℹ️ Using funcs.process_r2z_profile to process .r2z file.")
            if funcs.process_r2z_profile(uuid_code, show_error):
                show_error(f"✔️ R2Z profile processed successfully.")
                funcs.update_mods(show_error)  # Refresh mods
            else:
                show_error(f"⚠️ Failed to process R2Z profile.")
        else:
            show_error(f"❌ funcs.process_r2z_profile not found. Using fallback processing.")
            if fallback_process_r2z_profile(uuid_code, target_path):
                show_error(f"✔️ R2Z profile processed successfully (fallback).")
                try:
                    funcs.update_mods(show_error)  # Refresh mods
                except AttributeError:
                    show_error("⚠️ funcs.update_mods not found. Mods may need manual refresh.")
            else:
                show_error(f"⚠️ Failed to process R2Z profile (fallback).")

    except Exception as e:
        show_error(f"❌ Error importing .r2z file: {str(e)}")

def fallback_process_r2z_profile(uuid_code, r2z_file):
    """Fallback function to unpack .r2z file, skipping r2modman-specific data."""
    try:
        extract_path = os.path.join("Ziped_Mods", uuid_code)
        os.makedirs(extract_path, exist_ok=True)

        # Define r2modman-specific files and patterns to skip
        r2mm_files = [
            "manifest.json", "export.r2x", "changelog.txt", "doorstop_config.ini",
            "config.json", "r2modman_settings.json", "readme.md", "license",
            "requirements.txt"
        ]
        r2mm_patterns = [
            ".github/", ".git/", "__pycache__/", "tests/", "docs/"
        ]

        # Unpack the .r2z file, skipping unwanted files
        with zipfile.ZipFile(r2z_file, 'r') as zip_ref:
            extracted_files = 0
            for file_info in zip_ref.infolist():
                file_name = file_info.filename

                # Skip directories
                if file_info.is_dir():
                    continue

                # Check for r2modman-specific files or patterns
                skip_file = False
                # Match exact filenames (case-insensitive)
                base_name = os.path.basename(file_name).lower()
                if base_name in r2mm_files:
                    show_error(f"⚠️ Skipped r2modman file in .r2z: {file_name}")
                    continue

                # Match patterns in file path
                for pattern in r2mm_patterns:
                    if pattern in file_name.lower():
                        show_error(f"⚠️ Skipped r2modman-related file in .r2z: {file_name}")
                        skip_file = True
                        break

                if skip_file:
                    continue

                # Extract the file
                zip_ref.extract(file_info, extract_path)
                show_error(f"✔️ Extracted: {file_name}")
                extracted_files += 1

        # If no files were extracted (all were skipped), log a warning
        if extracted_files == 0:
            show_error("⚠️ No mod files extracted from .r2z (all files were r2modman-specific).")
            shutil.rmtree(extract_path)
            show_error(f"🗑️ Cleaned up temporary directory: {extract_path}")
            return True  # Still considered successful, as skipping was intentional

        # Move mod files to target directory, preserving structure
        mod_target_dir = os.path.join(os.getcwd(), "Mods", "EDF 6 MOD SETTINGS MAKER", "MOD CONFIG DATA PLACED HERE")
        os.makedirs(mod_target_dir, exist_ok=True)

        for root, dirs, files in os.walk(extract_path):
            # Determine relative path to preserve mod directory structure
            rel_path = os.path.relpath(root, extract_path)
            if rel_path == ".":
                # Top-level files (not in a mod subdirectory)
                target_mod_dir = mod_target_dir
            else:
                # Preserve mod subdirectory (e.g., mods/Chimera-System_Clock -> MOD CONFIG DATA PLACED HERE/Chimera-System_Clock)
                target_mod_dir = os.path.join(mod_target_dir, rel_path.replace("mods/", "", 1))

            os.makedirs(target_mod_dir, exist_ok=True)

            for file in files:
                src_path = os.path.join(root, file)
                dst_path = os.path.join(target_mod_dir, file)
                # Avoid overwriting by appending a suffix if file exists
                base, ext = os.path.splitext(dst_path)
                counter = 1
                while os.path.exists(dst_path):
                    dst_path = f"{base}_{counter}{ext}"
                    counter += 1
                shutil.move(src_path, dst_path)
                show_error(f"➡️ Moved mod file to: {dst_path}")

        # Clean up extracted directory
        shutil.rmtree(extract_path)
        show_error(f"🗑️ Cleaned up temporary directory: {extract_path}")
        show_error(f"✅ R2Z profile for {uuid_code} extracted successfully.")
        return True

    except Exception as e:
        show_error(f"❌ Error in fallback processing: {str(e)}")
        return False

def handle_request_drop_off(request_code=None):
    """Handle the request drop-off button click with support for text-based commands."""
    # Capture the input on the main thread to avoid Tkinter cross-thread issues
    if request_code is None or not isinstance(request_code, str):
        try:
            # Prefer StringVar, but fall back to direct Entry read if needed
            value = request_code_var.get()
            if not value.strip():
                global request_code_entry
                if request_code_entry is not None:
                    value = request_code_entry.get()
            request_code = value
        except Exception:
            request_code = ""
    captured_code = str(request_code)

    def process_request(code):
        def is_valid_uuid(candidate):
            # Basic UUID format validation of 36 characters in HEX For R2Modman code sharing
            return bool(re.match(r"^[0-9a-fA-F\-]{36}$", candidate))
            #0195686c-6290-f2e2-f0a8-c208f1b368e8
        clear_error()

        # Validate captured input
        if not code.strip():
            show_error("Error: Request code cannot be empty!")
            return None

        normalized_code = code.strip().lower()  # Normalize the input by trimming whitespace and converting to lowercase
        increment_cmd("total")
        
        if normalized_code in ["debug_cmd"]:
            increment_cmd("debug_cmd")
            render_command_stats()
            # keep console clear toggle
            # clear_error()  # optional

        elif normalized_code in ["bg list"]:
            increment_cmd("bg_list")
            result = cmd_bg_list(return_text=True)
            show_error(result)

        elif normalized_code == "bg":
            increment_cmd("bg")
            show_error("Usage: bg random | bg r | bg <image_name> | bg list")

        elif normalized_code.startswith("bg "):
            cmd = normalized_code.strip().lower()
            if cmd == "bg random" or cmd == "bg r":
                increment_cmd("bg_random")
                set_random_background_image()
            elif cmd.startswith("bg "):
                increment_cmd("bg_named")
                image_name = normalized_code[3:].strip()  # Extract the image name after "bg "
                if not image_name:
                    show_error("❌ No image name provided. Use 'bg [image_name]' with a valid JPG, PNG, or WEBP file.")
                    return
                valid_extensions = ('.jpg', '.jpeg', '.png', '.webp')
                if not image_name.lower().endswith(valid_extensions):
                    show_error(f"❌ Unsupported image format: '{image_name}'. Use JPG, PNG, or WEBP.")
                    return
                set_background_image_manual(image_name)
            else:
                show_error(f"Unknown command: {normalized_code}")

        elif normalized_code in ["no install", "ni"]:
            increment_cmd("no_install")
            show_error("Processing No Install (NI) request...")
            repair_tables()
            funcs.build_tables(show_error, exe_name="EDF HAKKEN NI.exe")
            update_setting("modloader_HAKKEN_style", "NI")

        elif normalized_code in ["install", "i"]:
            increment_cmd("install")
            show_error("Processing Install (I) request...")
            repair_tables()
            funcs.build_tables(show_error, exe_name="EDF HAKKEN.exe")
            update_setting("modloader_HAKKEN_style", "I")

        elif normalized_code in ["help", "h"]:
            increment_cmd("help")
            show_error("'help', 'h', 'HELP': Show console commands (SCROLL DOWN IN THIS WINDOW)")
            show_error("'install', 'i': Install all files that will be generated from the 'Build Tables' button. AUTO_BUILDS\n")
            show_error("'no install', 'ni': Debug mode - generates files but does NOT install them. AUTO_BUILDS\n")
            show_error("'credits', 'who_made_this' Prints who has had a hand in making this tool set \n")
            show_error("EASTER EGGS HIDDEN WITHIN ME, ALWAYS LOWERCASE, SPACES ARE _, THREE WORDS MAX, NUMBERS SPELT ARE CRINGE, SO DO THE ARABIC SYMBOLS AS A EXAMPLE COMMAND beans_1234567890_test, NUMBERS ARE ALWAYS ARE SURROUND BY _, IF YE SEEK A TRAIL, hint_me")

        elif normalized_code in ["bob_the_builder"]:
            increment_cmd("bob_the_builder")
            clear_error()
            run_bat_files_from_dirs()

        elif normalized_code in ["e_d_f"]:
            increment_cmd("e_d_f")
            clear_error()
            eggs.display_letters(show_error, clear_error)

        elif normalized_code in ["credits", "who_made_this"]:
            increment_cmd("credits")
            clear_error()
            eggs.edf_credits_scroll(show_error, clear_error, speed=0.1)

        elif normalized_code in ["hint_me"]:
            increment_cmd("hint_me")
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
            increment_cmd("moo")
            show_error("You found an Easter Egg! 🥚🐣")
            time.sleep(3)
            clear_error()
            eggs.asciicow(show_error)

        elif normalized_code in ["erased_future", "time_rewrite"]:
            increment_cmd("erased_future")
            show_error("You found a Classified Easter Egg! 🕵️‍♂️")
            time.sleep(3)
            clear_error()
            eggs.erased_future_transmission(show_error, clear_error)

        elif normalized_code in ["beans_1234567890_test"]:
            increment_cmd("beans_test")
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
            increment_cmd("edf_marquee")
            show_error("You found an Easter Egg! 🥚🐣")
            time.sleep(3)
            clear_error()
            eggs.side_scroll_edf_multiline(show_error, clear_error, speed=0.1)

        elif normalized_code in ["chant_edf"]:
            increment_cmd("chant_edf")
            show_error("You found an Easter Egg! 🥚🐣")
            time.sleep(3)
            clear_error()
            eggs.play_edf_chant(show_error, clear_error)

        elif normalized_code in ["storm_1_transmission"]:
            increment_cmd("storm_1_transmission")
            show_error("You found an Easter Egg! 🥚🐣")
            time.sleep(3)
            clear_error()
            eggs.someegg(show_error)

        elif normalized_code in ["incoming_transmission"]:
            increment_cmd("incoming_transmission")
            show_error("You found an Easter Egg! 🥚🐣")
            time.sleep(3)
            clear_error()
            eggs.edf_quotes(show_error)

        elif normalized_code in ["deployment_orders", "mission_briefing"]:
            increment_cmd("deployment_orders")
            show_error("You found an Easter Egg! 🥚🐣")
            time.sleep(3)
            clear_error()
            eggs.edf_mission_generator(show_error)

        elif normalized_code in ["jesus", "jesus_christ"]:
            increment_cmd("jesus")
            clear_error()
            eggs.get_daily_bible_verse(show_error, clear_error)

        elif is_valid_uuid(normalized_code):
            increment_cmd("uuid")
            show_error(f"Valid Mod request UUID")
            show_error(f"R2MODMAN UUID processing not implemented in this tool.")
            # Add R2MODMAN UUID processing logic here
            #update_mods()

        else:
            increment_cmd("unknown")
            show_error("Error: Invalid request code or command!")

    # Run the processing in a separate thread with the captured input
    threading.Thread(target=lambda: process_request(captured_code), daemon=True).start()

def create_mod_request_input(canvas, y_position):
    y_pos = y_position

    # Add the header above the input field
    header_label = tk.Label(
        root,
        text=lang_manager.get("request_code_header"),
        font=global_font_h,
        bg=JustBackGround(),
        fg=TextColor()
    )
    translatable_widgets.append(('text', header_label, "request_code_header"))
    canvas.create_window(width() // 2, y_pos, window=header_label)
    y_pos += 30

    # Create a frame to hold the input field and button
    input_frame = tk.Frame(
        root,
        bg=bgY(),
        highlightthickness=0,
        bd=0,
        relief="groove"
    )
    # Add the text input field
    global request_code_var
    global request_code_entry
    text_input = tk.Entry(
        input_frame,
        textvariable=request_code_var,
        font=global_font,
        width=65,
        bg="#EDFEDF",
        fg="black",
        relief="groove"
    )
    request_code_entry = text_input  # keep a direct handle on the Entry for fallback reads
    apply_hover_and_tooltip(text_input, lang_manager.get("tooltip_request_code_input"))
    text_input.pack(side="left", padx=get_padding(2, 4), pady=0)
    text_input.bind("<Return>", lambda event: handle_request_drop_off())
    translatable_widgets.append(('text', text_input, "tooltip_request_code_input"))

    # Add the "Request Drop Off Now" button
    style, tooltip = get_label_style_alt(command=lambda: handle_request_drop_off(), translation_key="request_drop_off_now")
    drop_off_button = tk.Button(input_frame, text=lang_manager.get("request_drop_off_now"), **style)
    apply_hover_and_tooltip(drop_off_button, tooltip)
    translatable_widgets.append(('text', drop_off_button, "request_drop_off_now"))
    drop_off_button.pack(side="left", padx=get_padding(3, 4), pady=0)

    # Add the input frame to the canvas
    canvas.create_window(width() // 2, y_pos, window=input_frame, anchor="center")
    y_pos += 5
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

    for group_name, links in social_media_groups.items():
        # Add a label for the group with translated key
        group_key = group_name.lower().replace(" ", "_").replace("/", "_").replace("'", "")
        group_label = tk.Label(
            root,
            text=lang_manager.get(group_key, fallback=group_name),
            font=global_font,
            bg=JustBackGround(),
            fg=TextColor()
        )
        translatable_widgets.append(('text', group_label, group_key, {}))
        canvas.create_window(width() // 2, y_pos, window=group_label)
        y_pos += 26

        # Create a frame to hold the buttons horizontally
        frame = tk.Frame(root, bg=bgY())

        # Loop through the links and create buttons with tooltips
        for i, link_data in enumerate(links):
            if len(link_data) == 3:
                label, url, tooltip = link_data
                label_key = label.lower().replace(" ", "_").replace("/", "_").replace("'", "")
            else:
                label, url = link_data
                label_key = label.lower().replace(" ", "_").replace("/", "_").replace("'", "")
                tooltip = lang_manager.get(f"tooltip_{label_key}", label=label)

            style, _ = get_button_style(command=lambda u=url: search_nexus_mods() if u is None else open_link(u))
            button = tk.Button(frame, text=lang_manager.get(label_key, fallback=label), **style)
            apply_hover_and_tooltip(button, tooltip)
            translatable_widgets.append(('text', button, label_key, {}))
            button.pack(side="left", padx=get_padding(i, len(links)))

        canvas.create_window(width() // 2, y_pos, window=frame, anchor="center")
        y_pos += 30

    return y_pos

def update_ui_translations():
    print("Translatable widgets:", [(i, item) for i, item in enumerate(translatable_widgets)])  # Debug
    for i, item in enumerate(translatable_widgets):
        try:
            if len(item) == 3:
                attr, widget, key = item
                kwargs = {}
            elif len(item) == 4:
                attr, widget, key, kwargs = item[0], item[1], item[2], {} if len(item) < 4 else item[3]
            elif len(item) == 5:
                attr, widget, key, kwargs = item[0], item[1], item[2], item[3] if isinstance(item[3], dict) else {}
            else:
                print(f"Warning: Invalid translatable_widgets entry at index {i}: {item}")
                continue

            if attr == 'text':
                widget.config(text=lang_manager.get(key, **kwargs))
            elif attr == 'textvariable':
                if isinstance(widget, tk.Widget) and hasattr(widget, 'cget') and 'textvariable' in widget.keys():
                    widget_textvar = widget.cget('textvariable')
                    if isinstance(widget_textvar, tk.StringVar):
                        widget_textvar.set(lang_manager.get(key, **kwargs))
                    else:
                        print(f"Warning: Widget {key} has no valid textvariable")
                else:
                    print(f"Warning: Widget {key} is not configurable or has no textvariable")
            elif attr == 'canvas_text':
                if len(item) >= 4 and isinstance(item[1], tk.Canvas) and isinstance(item[2], int):
                    canvas, text_id = item[1], item[2]
                    canvas.itemconfig(text_id, text=lang_manager.get(key, **kwargs))
                else:
                    print(f"Warning: Invalid canvas_text entry at index {i}: {item}")
            tooltip_key = f"tooltip_{key}"
            if tooltip_key in lang_manager.translations:
                apply_hover_and_tooltip(widget, lang_manager.get(tooltip_key, **kwargs))
        except Exception as e:
            print(f"Error updating widget {key} at index {i}: {e}")
    root.title(lang_manager.get("title", version=get_version()))

def create_ui(canvas):
    global total_mods, total_patches, total_plugins, error_block, modloader_status, translatable_widgets
    total_mods = tk.StringVar(value="0")
    total_patches = tk.StringVar(value="0")
    total_plugins = tk.StringVar(value="0")
    modloader_status = tk.StringVar(value=lang_manager.get("toggle_modloader_status", status=funcs.get_modloader_status()))  # Initialize with current status
    translatable_widgets = []

    y_pos = 30
    vertical_spacing = 30

    # Dynamically detect available languages
    language_dir = os.path.join(os.path.dirname(__file__), "languages")
    available_languages = {}
    if os.path.exists(language_dir):
        for filename in os.listdir(language_dir):
            if filename.endswith(".json"):
                lang_code = filename.replace(".json", "")
                # Load the language file to get the "Full Word For Language" translation
                try:
                    with open(os.path.join(language_dir, filename), "r", encoding="utf-8") as f:
                        lang_data = json.load(f)
                        full_name = lang_data.get("Full Word For Language", lang_code.capitalize())
                        available_languages[full_name] = lang_code
                except Exception as e:
                    print(f"Error loading {filename}: {e}")
                    continue
    else:
        available_languages = {"English": "en"}  # Fallback if directory doesn't exist
        print(f"Warning: Languages directory not found at {language_dir}. Defaulting to English.")

    # Ensure English is always included as a fallback
    if "en" not in available_languages.values():
        available_languages["English"] = "en"

    selected_language = tk.StringVar(value=next((k for k, v in available_languages.items() if v == lang_manager.current_language), "English"))
    
    def update_language(*args):
        lang_code = available_languages[selected_language.get()]
        lang_manager.load_translations(lang_code)
        update_setting("language", lang_code)
        update_ui_translations()
    
    # Language and Font Size Selection Frame
    selection_frame = tk.Frame(root, bg=bgY())
    language_dropdown = tk.OptionMenu(selection_frame, selected_language, *available_languages.keys(), command=update_language)
    language_dropdown.config(
        bg=ButtonBackGround(),
        fg=TextColor(),
        activebackground=hover_bg(),
        activeforeground=hover_fg(),
        relief="groove",
        highlightthickness=0,
        cursor="hand2"
    )
    language_dropdown["menu"].config(
        bg=ButtonBackGround(),
        fg=TextColor(),
        activebackground=hover_bg(),
        activeforeground=hover_fg()
    )
    apply_hover_and_tooltip(language_dropdown, lang_manager.get("tooltip_language_dropdown"))
    translatable_widgets.append(('text', language_dropdown, "tooltip_language_dropdown"))
    language_dropdown.pack(side="left", padx=get_padding(0, 2))
    font_sizes = [8, 10, 12, 14, 16]
    selected_font_size = tk.StringVar(value=str(settings.get("font_sizes", {}).get("global_font", 10)))
    
    def update_font_size(*args):
        size = int(selected_font_size.get())
        set_font_size("global_font", size)
        set_font_size("global_font_h", size + 2)  # Maintain relative difference
        update_ui_translations()  # Reapply text to reflect new font sizes

    font_size_dropdown = tk.OptionMenu(selection_frame, selected_font_size, *font_sizes, command=update_font_size)
    font_size_dropdown.config(
        bg=ButtonBackGround(),
        fg=TextColor(),
        activebackground=hover_bg(),
        activeforeground=hover_fg(),
        relief="groove",
        highlightthickness=0,
        cursor="hand2"
    )
    font_size_dropdown["menu"].config(
        bg=ButtonBackGround(),
        fg=TextColor(),
        activebackground=hover_bg(),
        activeforeground=hover_fg()
    )
    apply_hover_and_tooltip(font_size_dropdown, "Select the base font size for the interface")
    translatable_widgets.append(('text', font_size_dropdown, "tooltip_font_size_dropdown"))
    font_size_dropdown.pack(side="left", padx=get_padding(1, 2))  # Second button, 5px left, 5px right

    canvas.create_window(width() // 2, y_pos, window=selection_frame)
    y_pos += vertical_spacing

    # Game Launch
    y_pos = create_game_launch_bar(canvas, y_pos)
    y_pos += vertical_spacing + 5

    # Game Management
    y_pos = create_mml_installer_tools(canvas, y_pos)

    # Toggle Buttons
    toggle_buttons_frame = tk.Frame(root, bg=bgY())
    toggle_buttons = [
        (modloader_status, toggle_modloader_status, "toggle_modloader_status"),
        ("open_current_dir", lambda: os.startfile(current_dir), "open_current_dir"),
    ]

    toggle_widgets = []  # Temporary list to store button references
    for idx, (text_or_var, command, translation_key) in enumerate(toggle_buttons):
        style, tooltip = get_button_style(command=command, translation_key=translation_key)
        button = tk.Button(
            toggle_buttons_frame,
            text=lang_manager.get(translation_key) if isinstance(text_or_var, str) else None,
            textvariable=text_or_var if isinstance(text_or_var, tk.StringVar) else None,
            **style
        )
        apply_hover_and_tooltip(button, tooltip)
        translatable_widgets.append(('text' if isinstance(text_or_var, str) else 'textvariable', button, translation_key))
        toggle_widgets.append(button)
        button.pack(side="left", padx=get_padding(idx, len(toggle_buttons)))

    labels_and_buttons.append(canvas.create_window(width() // 2, y_pos, window=toggle_buttons_frame))
    y_pos += vertical_spacing

    # Mod Information
    y_pos = create_mod_info_buttons(canvas, y_pos)
    y_pos += 5

    # Save Folders Management
    text_id = draw_centered_text_with_bg(canvas, width() // 2, y_pos, lang_manager.get("open_save_folders"), global_fill_color, JustBackGround(), font=global_font_h)
    translatable_widgets.append(('canvas_text', canvas, text_id, "open_save_folders"))
    y_pos += vertical_spacing + 5

    save_folder_frame = tk.Frame(root, bg=bgY())
    save_folder_buttons = [
        ("save_folder_41", lambda: funcs.open_save_folder(show_error, "EARTH DEFENSE FORCE 4.1"), "save_folder_41"),
        ("save_folder_5", lambda: funcs.open_save_folder(show_error, "EARTH DEFENSE FORCE 5"), "save_folder_5"),
        ("save_folder_6", lambda: funcs.open_save_folder(show_error, "EARTH DEFENSE FORCE 6"), "save_folder_6"),
    ]
    for idx, (translation_key, command, tooltip_key) in enumerate(save_folder_buttons):
        style, tooltip = get_button_style(command=command, translation_key=translation_key)
        button = tk.Button(save_folder_frame, text=lang_manager.get(translation_key), **style)
        apply_hover_and_tooltip(button, tooltip)
        translatable_widgets.append(('text', button, translation_key, {}))
        button.pack(side="left", padx=get_padding(idx, len(save_folder_buttons)))
    labels_and_buttons.append(canvas.create_window(width() // 2, y_pos, window=save_folder_frame))
    y_pos += vertical_spacing + 10

    # Mod Hosting Services
    text_id = draw_centered_text_with_bg(
        canvas,
        width() // 2,
        y_pos,
        lang_manager.get("mod_hosting_services"),
        global_fill_color,
        JustBackGround(),
        font=global_font_h
    )
    text_id = draw_centered_text_with_bg(canvas, width() // 2, y_pos, lang_manager.get("mod_hosting_services"), global_fill_color, JustBackGround(), font=global_font_h)
    translatable_widgets.append(('canvas_text', canvas, 12, "mod_hosting_services", {})) 
    y_pos += vertical_spacing
    y_pos = create_mod_hosting_services(canvas, y_pos)  # Call updated function
    y_pos += vertical_spacing

    # Mod Request Input
    y_pos = create_mod_request_input(canvas, y_pos)
    y_pos += vertical_spacing + 5

    # Console and Logs
    text_id = draw_centered_text_with_bg(canvas, width() // 2, y_pos, lang_manager.get("hq_pager_console"), global_fill_color, JustBackGround(), font=global_font_h)
    translatable_widgets.append(('canvas_text', canvas, 16, 'hq_pager_console'))
    y_pos += vertical_spacing + 35

    error_block = tk.Text(root, height=6, width=90, font=("Courier", 9), state=tk.DISABLED, bg=ButtonBackGround(), fg=TextColor(), wrap="word")
    canvas.create_window(width() // 2, y_pos, window=error_block)
    y_pos += 70

    style, tooltip = get_label_style_alt(command=clear_error, translation_key="clear_console")
    clear_console_button = tk.Button(root, text=lang_manager.get("clear_console"), **style)
    apply_hover_and_tooltip(clear_console_button, tooltip)
    translatable_widgets.append(('text', clear_console_button, "clear_console"))
    labels_and_buttons.append(canvas.create_window(width() // 2, y_pos, window=clear_console_button))
    y_pos += vertical_spacing

    global modloader_toggle_button
    modloader_toggle_button = toggle_widgets[0]  # Assuming first button is modloader toggle

    def update_modloader_status():
        try:
            current_status = funcs.get_modloader_status()
            modloader_status.set(lang_manager.get("toggle_modloader_status", status=current_status))
            # Update translatable_widgets entry for the modloader toggle button
            if modloader_toggle_button:
                for i, item in enumerate(translatable_widgets):
                    if item[1] == modloader_toggle_button:
                        translatable_widgets[i] = ('textvariable', modloader_toggle_button, "toggle_modloader_status", {'status': current_status})
                        break
                update_ui_translations()  # Reapply all translations to ensure consistency
        except Exception as e:
            show_error(str(e))

    # Update mod counts and statuses on startup
    update_mod_counts()
    start_monitoring_loop()
    update_modloader_status()
    create_social_media_links_horizontal(canvas, y_pos)
    
    y_pos += 230

    # Credits and BAT Files Buttons
    buttons_frame = tk.Frame(root, bg=bgY())
    button_configs = [
        (lambda: threading.Thread(target=lambda: eggs.edf_credits_scroll(show_error, clear_error), daemon=True).start(), "show_credits", "show_credits"),
    ]
    if RUN_BAT_FILES_ENABLED:
        button_configs.append((run_bat_files_from_dirs, "run_all_bat_files", "run_all_bat_files"))

    for idx, (command, translation_key, tooltip_key) in enumerate(button_configs):
        style, tooltip = get_label_style_alt(command=command, translation_key=translation_key)
        button = tk.Button(buttons_frame, text=lang_manager.get(translation_key), **style)
        apply_hover_and_tooltip(button, tooltip)
        translatable_widgets.append(('text', button, translation_key))
        button.pack(side="left", padx=get_padding(idx, len(button_configs)))

    labels_and_buttons.append(canvas.create_window(width() // 2, y_pos, window=buttons_frame))
    y_pos += vertical_spacing

# Use canvas to create the UI elements
create_ui(canvas)

start_update_check()

root.mainloop()



