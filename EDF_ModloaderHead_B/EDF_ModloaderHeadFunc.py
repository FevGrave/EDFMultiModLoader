#====================================================================================================
# EDF_ModloaderHeadFunc.py

import os, sys, shutil, requests, subprocess, json, hashlib, zipfile, zipfile, glob, time
import tkinter.filedialog as filedialog, tkinter as tk, ConfigManifestUninstaller as uninstaller
from tkinter import messagebox
from tkinter import ttk

# Initialize as None to be set by an external function
set_current_dir = None
settings = None

def initialize_settings(current_dir):
    global set_current_dir, settings
    set_current_dir = current_dir
    settings = load_settings(set_current_dir)

def load_settings(set_current_dir):
    """Load settings from a JSON file, with default fallback and validation."""
    settings_file = "MMLsettings.json"
    default_settings = {
        "edf6_platform": "steam",
        "platform_can_be": "steam|epic",
        "modloader_HAKKEN_style": "NI",  # Change to "I" Installer or "NI" NO INSTALL,
        "base_dir": set_current_dir,
        "language": "en",
        "font_sizes": {
            "global_font": 10,
            "global_font_h": 12
        },
        "colors": {
            "JustBackGround": "#484848",
            "ButtonBackGround": "#000000",
            "ButtonPressedBackGround": "#010e70",
            "hover_bg": "#555555",
            "hover_fg": "#ffffff",
            "TextColor": "#B3FF00",
            "PressedTextColor": "#ffffff",
            "Helpful Color Blind Site": "https://davidmathlogic.com/colorblind/#%23484848-%23000000-%23010E70-%23FFFFFF"
        },
        "modloader_status": "Enabled",
        "modloader_status_can_be": "Enabled|Disabled, DONT EDIT AS THIS IS VISUAL TEXT",
        "progress": {
            "Last Game": "EDF 6",
            "EDF World Brothers 2": 0.0,  # Sep 2024
            "(WB2) Extra Mission Pack: Robo Saurous vs the Mecharmy": 0.0,
            "EDF 6": 0.0,  # Jul 2024 (West)
            "( 6 ) DLC Lost Days": 0.0,
            "( 6 ) DLC Visions of Malice": 0.0,
            "EDF World Brothers": 0.0,  # May 2021
            "(WB ) Additional Mission Pack: Another ResCUBE": 0.0,
            "EDF: Iron Rain": 0.0,  # Apr 2019
            "(IR ) Golden Storm": 0.0,
            "EDF 5 Online": 0.0,  # Dec 2018
            "EDF 5 Offline": 0.0,
            "( 5 ) DLC Mission Pack 1": 0.0,
            "( 5 ) DLC Mission Pack 2": 0.0,
            "EDF 4.1 Online": 0.0,  # Apr 2016
            "EDF 4.1 Offline": 0.0,
            "(4.1) DLC Mission Pack 1": 0.0,
            "(4.1) DLC Mission Pack 2": 0.0,
            "EDF 2025": 0.0,  # Feb 2014
            "(2025) DLC Mission Pack 1": 0.0,
            "(2025) DLC Mission Pack 2": 0.0,
            "(2025) DLC Mission Pack 3": 0.0,
            "EDF 2 Portable (Vita)": 0.0,  # Apr 2013
            "EDF 2017 Portable (Vita)": 0.0,  # Jan 2013
            "EDF Insect Armageddon": 0.0,  # Jul 2011
            "EDF 2017": 0.0,  # Mar 2007
            "EDF 2": 0.0,  # Jul 2005
            "Monster Attack (2003)": 0.0,  # Mar 2004 (EU)
            "Custom Mod Pack": 0.0
        },
        "Custom Mod Pack": {
            "ClassCount": 4,
            "Difficulties": 5,
            "Missions": 100,
            "NoLimits": 0.7
        }
    }

    try:
        if os.path.exists(settings_file):
            with open(settings_file, 'r') as file:
                settings = json.load(file)
                for key, value in default_settings.items():
                    if key not in settings:
                        settings[key] = value
                return settings
    except json.JSONDecodeError:
        print("Error loading settings, reverting to defaults.")

    save_settings(default_settings)
    return default_settings

def save_settings(settings):
    """Save settings to a JSON file."""
    settings_file = "MMLsettings.json"
    try:
        with open(settings_file, 'w') as file:
            json.dump(settings, file, indent=4)
    except Exception as e:
        print(f"Error saving settings: {e}")

def get_settings():
    """Getter for settings."""
    return settings

# Set the global variable for the script directory
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__ if '__file__' in globals() else sys.executable))
modloader_status_file = "winmm.dll"

# Define the directory for saving and unpacking updates
# Initialize settings and set parent_dir
settings = load_settings(set_current_dir)  # Load settings into the global variable

# Set parent_dir from the base_dir within settings
parent_dir = settings.get("base_dir", set_current_dir)  # Fallback to set_current_dir if not specified
UPDATE_DIR = parent_dir

PLUGIN_DIRS = {
    "EARTH DEFENSE FORCE 4.1": "Plugins41",
    "EARTH DEFENSE FORCE 5": "Plugins5",
    "EARTH DEFENSE FORCE 6": "Plugins6",
}

#====================================================================================================
#TABLES

# Function to build tables, choosing between Python script or EXE based on the `use_exe` flag
def build_tables(error_msg, exe_name="EDF HAKKEN NI.exe"):
    use_exe = True  # Set to False to test Python script
    
    # Set parent_dir to the correct base directory
    parent_dir = r"F:\SteamLibrary\steamapps\common\EARTH DEFENSE FORCE 6"  # Adjusted to match EXE location
    if parent_dir is None:
        raise ValueError("parent_dir is not defined or None")
    
    output_directory = parent_dir
    current_directory = os.path.abspath(os.path.join(parent_dir, "Mods", "EDF 6 MOD SETTINGS MAKER"))
    
    print(f"parent_dir: {parent_dir}")
    print(f"output_directory: {output_directory}")
    print(f"current_directory: {current_directory}")
    
    mod_dir = os.path.join(parent_dir, "Mods", "EDF 6 MOD SETTINGS MAKER")
    print(f"Files in {mod_dir}: {os.listdir(mod_dir)}")  # Debug: List files in directory
    
    try:
        if use_exe:
            exe_path = os.path.join(mod_dir, exe_name)
            print(f"EXE path: {exe_path}")
            if not os.path.isfile(exe_path):
                raise FileNotFoundError(f"EXE file not found: {exe_path}. Available EXEs: {glob.glob(os.path.join(mod_dir, '*.exe'))}")
            result = subprocess.run(
                [exe_path, output_directory, current_directory],
                capture_output=True,
                text=True,
                shell=True
            )
        else:
            script_path = os.path.join(mod_dir, "ConfigBuildAllNoInstaller.py")
            print(f"Python script path: {script_path}")
            if not os.path.isfile(script_path):
                raise FileNotFoundError(f"Python script not found: {script_path}")
            result = subprocess.run(
                ["python", script_path, output_directory, current_directory],
                capture_output=True,
                text=True,
                shell=True
            )

        error_msg(result.stdout)
        if result.stderr:
            error_msg("Error: " + result.stderr)
    except Exception as e:
        error_msg(f"Exception occurred: {str(e)}")

# Repair Tables: Copy files from a directory and paste them at the parent directory
def repair_tables(error_msg, current_dir):
    try:
        if not current_dir or not isinstance(current_dir, (str, bytes, os.PathLike)):
            error_msg(f"Invalid current directory: Directory path is empty or invalid (got: {current_dir})")
            return

        if not os.path.isdir(current_dir):
            error_msg(f"Current directory does not exist: {current_dir}")
            return

        source_dir = os.path.join(current_dir, "Mods", "EDF 6 MOD SETTINGS MAKER", "DO NOT TOUCH ORIGINAL CONFIG DATA")
        dest_dir = os.path.join(current_dir, "Mods", "EDF 6 MOD SETTINGS MAKER")

        if not os.path.exists(source_dir):
            error_msg(f"Source directory does not exist: {source_dir}")
            return

        if not os.path.exists(dest_dir):
            error_msg(f"Destination directory does not exist: {dest_dir}")
            return

        # Create backup directory with timestamp
        backup_dir = os.path.join(dest_dir, f"Backup_{time.strftime('%Y%m%d_%H%M%S')}")
        os.makedirs(backup_dir, exist_ok=True)
        error_msg(f"Created backup directory: {backup_dir}")

        copied_files = []
        backed_up_files = []
        for filename in os.listdir(source_dir):
            if filename.endswith(".json"):  # Filter for .json files
                full_file_path = os.path.join(source_dir, filename)
                dest_file_path = os.path.join(dest_dir, filename)
                if os.path.isfile(full_file_path):
                    # Backup existing file if it exists
                    if os.path.exists(dest_file_path):
                        backup_file_path = os.path.join(backup_dir, filename)
                        shutil.move(dest_file_path, backup_file_path)
                        backed_up_files.append(filename)
                        error_msg(f"Backed up existing file: {filename} to {backup_dir}")
                    # Copy (overwrite) the file
                    shutil.copy(full_file_path, dest_dir)
                    copied_files.append(filename)
                    error_msg(f"Overwrote file: {filename}")

        if backed_up_files:
            error_msg(f"Backed up files: {', '.join(backed_up_files)}")
        if copied_files:
            error_msg(f"Tables repaired successfully. Overwrote files: {', '.join(copied_files)}")
        else:
            error_msg("No .json files found in source directory to copy.")
    except PermissionError as e:
        error_msg(f"Permission error while repairing tables: {str(e)}")
    except shutil.Error as e:
        error_msg(f"Error copying files: {str(e)}")
    except Exception as e:
        error_msg(f"Unexpected error while repairing tables: {str(e)}")

#====================================================================================================
#Funtions

def open_save_folder(error_msg, game_key=None):
    try:
        # Secure base paths
        onedrive_docs = os.path.join(os.getenv('USERPROFILE', ''), "OneDrive", "Documents")
        local_docs = os.path.join(os.getenv('USERPROFILE', ''), "Documents")
        local_appdata = os.getenv('LOCALAPPDATA', '')

        # Canonical save folder mappings
        save_paths = {
            "EARTH DEFENSE FORCE 4.1": [
                os.path.join(onedrive_docs, "My Games", "EDF4.1", "SAVE_DATA"),
                os.path.join(local_docs, "My Games", "EDF4.1", "SAVE_DATA")
            ],
            "EARTH DEFENSE FORCE 5": [
                os.path.join(onedrive_docs, "My Games", "EDF5", "SAVE_DATA"),
                os.path.join(local_docs, "My Games", "EDF5", "SAVE_DATA")
            ],
            "EARTH DEFENSE FORCE 6": [
                os.path.join(local_appdata, "EarthDefenceForce6", "SAVE_DATA")
            ]
        }

        if game_key not in save_paths:
            error_msg("Unknown game. Cannot determine save folder.")
            return

        attempted_paths = save_paths[game_key]
        for path in attempted_paths:
            if os.path.exists(path):
                subfolders = [f.path for f in os.scandir(path) if f.is_dir()]
                if subfolders:
                    subprocess.Popen(['explorer', subfolders[0]])
                    return
                else:
                    error_msg(f"Save directory found but contains no subfolders:\n{path}")
                    return

        # If we reach here, all paths failed
        joined_paths = "\n".join(attempted_paths)
        error_msg(f"Save folder not found. Tried:\n{joined_paths}")

    except Exception as e:
        error_msg(f"Exception while opening save folder:\n{str(e)}")

def launch_game(app_ids, error_msg):
    try:
        # Retrieve the most recent settings
        current_settings = get_settings()
        current_platform = current_settings.get("edf6_platform", "steam")

        if len(app_ids) == 1:  # Single ID available, default to Steam
            if app_ids[0].isdigit():
                steam_command = f"steam://run/{app_ids[0]}"
                subprocess.run(["start", steam_command], shell=True)
                error_msg(f"Launching EDF game with Steam App ID: {app_ids[0]}")
            else:
                error_msg("Invalid Steam App ID. Unable to launch the game. Unfortualy ")
            return

        # Handle platform-specific launches
        if current_platform == "steam":
            if app_ids[0].isdigit():  # Steam ID must be valid
                steam_command = f"steam://run/{app_ids[0]}"
                subprocess.run(["start", steam_command], shell=True)
                error_msg(f"Launching EDF game with Steam App ID: {app_ids[0]}")
            else:
                error_msg("Invalid Steam App ID. Unable to launch the game.")
        elif current_platform == "epic":
            if len(app_ids) > 1 and app_ids[1]:  # Epic ID must be present and valid
                epic_command = f"com.epicgames.launcher://apps/{app_ids[1]}?action=launch=true"
                subprocess.run(["start", epic_command], shell=True)
                error_msg(f"Launching EDF game with Epic Games Store App ID: {app_ids[1]}")
            else:
                error_msg(f"Epic Games platform is not supported for this game. "
                        f"Epic ID found: {app_ids[1] if len(app_ids) > 1 else 'None'}")
        else:
            error_msg("Unknown platform choice. Unable to launch the game.")
    except Exception as e:
        error_msg(f"Failed to launch EDF game with App IDs {app_ids}: {str(e)}")

def toggle_modloader_status(error_msg):
    try:
        if os.path.exists(modloader_status_file):
            os.rename(modloader_status_file, modloader_status_file + ".disabled")
            error_msg("Modloader disabled")
        else:
            os.rename(modloader_status_file + ".disabled", modloader_status_file)
            error_msg("Modloader enabled")
    except Exception as e:
        error_msg(f"Failed to toggle modloader status: {str(e)}")

def get_modloader_status():
    modloader_path = modloader_status_file  # Path to the modloader file (adjust path if necessary)
    disabled_modloader_path = modloader_path + ".disabled"  # Path to the disabled modloader file

    # Check for the presence of the modloader or its disabled counterpart
    if os.path.exists(modloader_path):
        return "Enabled"
    elif os.path.exists(disabled_modloader_path):
        return "Disabled"
    else:
        return "Lost.Unknown.MIA"  # Modloader file is not found

def show_error(error_msg):
    # Logic to display an error message
    messagebox.showerror("Error", error_msg)

#====================================================================================================
#Total addons

def get_mod_count(error_msg):
    try:
        mod_info_path = "Mods/EDF 6 MOD SETTINGS MAKER/MOD CONFIG DATA PLACED HERE"
        mod_files = [f for f in os.listdir(mod_info_path) if f.endswith(".json")]
        return str(len(mod_files))
    except Exception as e:
        error_msg(f"Failed to find ../Mods/EDF 6 MOD SETTINGS MAKER/MOD CONFIG DATA PLACED HERE")
        print(f"{str(e)}")
        return "0"

def get_patch_count(error_msg):
    try:
        count = len([file for file in os.listdir("Mods/Patches") if file.endswith(".txt")])
        return str(count)
    except Exception as e:
        error_msg(f"Failed find ../Mods/Patches")
        print(f"{str(e)}")
        return "0"

def get_plugin_count(error_msg):
    try:
        plugins_dir = os.path.join("Mods", "Plugins")
        plugins_dll_path = os.path.join(plugins_dir, "Patcher.dll")
        if not os.path.exists(plugins_dll_path):
            error_msg(f"'Patcher.dll' not found at {plugins_dll_path}")
            return "0"
        count = len(os.listdir(plugins_dir))
        return str(count)
    except Exception as e:
        error_msg(f"Failed to find ../Mods/Plugins")
        print(f"{str(e)}")
        return "0"

# Simple Error Logger
def show_error(message):
    print(f"Error: {message}")

#===================================================================================================

def validate_zip(file_path, error_msg):
    """Check if the downloaded zip file is valid."""
    if not os.path.exists(file_path):
        error_msg(f"File {file_path} does not exist.")
        return False

    try:
        with zipfile.ZipFile(file_path, 'r') as zip_ref:
            # Test the integrity of the zip file
            bad_file = zip_ref.testzip()
            if bad_file:
                error_msg(f"Corrupted file found in the archive: {bad_file}")
                return False
    except zipfile.BadZipFile:
        error_msg(f"The zip file {file_path} is invalid or corrupted.")
        return False

    return True

#====================================================================================================
#MODLOADER

def download_and_extract_zip(zip_url, zip_name, extract_to, error_msg):
    """Download a ZIP file from the given URL, validate it, and extract it. Then check for specific .exe files."""
    try:
        # Download the ZIP file
        response = requests.get(zip_url)
        response.raise_for_status()
        zip_path = os.path.join(extract_to, zip_name)
        with open(zip_path, 'wb') as file:
            file.write(response.content)

        # Validate the downloaded zip file
        if not validate_zip(zip_path, error_msg):
            error_msg(f"Validation failed for {zip_name}. File is not valid or is corrupted.")
            return

        # Extract the ZIP file
        with zipfile.ZipFile(zip_path, 'r') as zip_ref:
            zip_ref.extractall(extract_to)

        error_msg(f"Downloaded and extracted {zip_name}")

        # Check for specific .exe files in the extracted contents
        check_for_specific_exe_files(extract_to, error_msg)

    except requests.exceptions.RequestException as e:
        error_msg(f"Failed to download {zip_name}: {str(e)}")
    except zipfile.BadZipFile as e:
        error_msg(f"Failed to extract {zip_name}: {str(e)}")
    except Exception as e:
        error_msg(f"An unexpected error occurred while processing {zip_name}: {str(e)}")

def check_for_specific_exe_files(directory, error_msg, found_executables=set()):
    """Check for specific .exe files in the specified directory and its subdirectories."""
    specific_exes = {"EDF41.exe", "EDF5.exe", "EDF6.exe"}  # Using a set for faster lookups
    new_found_exes = []

    for root, dirs, files in os.walk(directory):
        for file in files:
            if file in specific_exes and file not in found_executables:
                exe_path = os.path.join(root, file)
                new_found_exes.append(file)  # Append only the filename
                found_executables.add(file)  # Mark this executable as found
    
    if new_found_exes:
        for exe_file in new_found_exes:
            error_msg(f"Found executable: {exe_file}")  # Print only the filename
    elif not found_executables:
        error_msg("No specific executables (EDF41.exe, EDF5.exe, EDF6.exe) found in the current directory.")

#====================================================================================================
# MODS SYSTEM

def validate_mod_info(mod_data, error_msg):
    required_fields = ['AUTHOR', 'MOD NAME', 'LINK', 'VERSION']
    for mod in mod_data.get("MOD_INFO", []):
        missing_fields = [field for field in required_fields if not mod.get(field)]
        if missing_fields:
            error_msg(f"Missing {', '.join(missing_fields)} in {mod.get('MOD NAME', 'Unknown Mod')}")
            return False
    return True

def check_mod_compatibility(json_data, error_msg):
    """
    Checks 'MOD NAME' and 'Incompatible with' fields from the JSON data.
    
    Args:
        json_data (dict): The parsed JSON data containing mod information.
        error_msg (callable): Function to log error messages.
        
    Returns:
        dict: A dictionary with mod names as keys and their incompatible mods as values.
    """
    mod_info = json_data.get("MOD_INFO", [])
    compatibility_info = {}
    
    for mod in mod_info:
        mod_name = mod.get("MOD NAME", "Unknown")
        incompatible_mods = mod.get("Incompatible with", "")
        
        if isinstance(incompatible_mods, str):
            incompatible_list = [mod.strip() for mod in incompatible_mods.split(",") if mod.strip()]
        else:
            incompatible_list = incompatible_mods
        
        compatibility_info[mod_name] = incompatible_list
    
    return compatibility_info

def process_mod_config(output_directory, current_directory, error_msg, config_filename="EDF_MML_Mod_config_data.json"):
    """
    Processes the mod config file and checks compatibility.
    
    Args:
        output_directory (str): Directory where output files are written.
        current_directory (str): Directory where the script is running.
        error_msg (callable): Function to log error messages.
        config_filename (str): Name of the JSON config file.
    
    Returns:
        dict: Compatibility information or None if the file is not found.
    """
    config_path = os.path.join(current_directory, config_filename)
    
    try:
        with open(config_path, "r", encoding="utf-8") as file:
            json_data = json.load(file)
        
        compatibility = check_mod_compatibility(json_data, error_msg)
        
        output_file = os.path.join(output_directory, "mod_compatibility_report.txt")
        os.makedirs(output_directory, exist_ok=True)
        with open(output_file, "w", encoding="utf-8") as report:
            for mod_name, incompatible_mods in compatibility.items():
                report.write(f"Mod Name: {mod_name}\n")
                report.write(f"Incompatible with: {', '.join(incompatible_mods) if incompatible_mods else 'None'}\n")
                report.write("\n")
        
        error_msg(f"Compatibility report written to: {output_file}")
        return compatibility
    
    except FileNotFoundError:
        error_msg(f"Error: Could not find '{config_filename}' in {current_directory}")
        return None
    except json.JSONDecodeError:
        error_msg(f"Error: '{config_filename}' is not a valid JSON file")
        return None
    except Exception as e:
        error_msg(f"Unexpected error processing '{config_filename}': {str(e)}")
        return None

def update_mods(error_msg, parent_dir=r"F:\SteamLibrary\steamapps\common\EARTH DEFENSE FORCE 6"):
    mod_info_path = os.path.join(parent_dir, "Mods", "EDF 6 MOD SETTINGS MAKER", "MOD CONFIG DATA PLACED HERE")
    
    try:
        if not os.path.isdir(parent_dir):
            error_msg(f"Parent directory does not exist: {parent_dir}")
            return

        if not os.path.isdir(mod_info_path):
            error_msg(f"Mod info directory does not exist: {mod_info_path}")
            return

        mod_files = [f for f in os.listdir(mod_info_path) if f.endswith(".json")]
        if not mod_files:
            error_msg("No JSON mod files found in mod info directory.")
            return

        processed_mods = []
        for mod_file in mod_files:
            try:
                mod_data = load_mod_data(mod_info_path, mod_file, error_msg)
                if not mod_data:
                    error_msg(f"Skipped {mod_file}: Failed to load mod data.")
                    continue

                mod_info = mod_data.get("MOD_INFO", [])
                if not mod_info:
                    error_msg(f"Skipped {mod_file}: No MOD_INFO found in mod data.")
                    continue

                for mod in mod_info:
                    mod_name = mod.get("name", "Unnamed mod")
                    if mod_name == "Unnamed mod":
                        error_msg(f"Warning: Mod in {mod_file} has no 'name' field.")
                    download_mod(mod, error_msg)
                    processed_mods.append(mod_name)

            except json.JSONDecodeError as e:
                error_msg(f"Failed to parse JSON in {mod_file}: {str(e)}")
                continue
            except Exception as e:
                error_msg(f"Error processing {mod_file}: {str(e)}")
                continue

        if processed_mods:
            error_msg(f"Mod update check completed. Processed mods: {', '.join(processed_mods)}")
        else:
            error_msg("No mods were processed.")
    except FileNotFoundError:
        error_msg(f"Mod info directory not found: {mod_info_path}")
    except Exception as e:
        error_msg(f"Unexpected error during mod update: {str(e)}")

def load_mod_data(mod_info_path, mod_file, error_msg):
    try:
        with open(os.path.join(mod_info_path, mod_file), "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception as e:
        error_msg(f"Error loading {mod_file}: {str(e)}")
        return None

def load_mod_data(mod_info_path, mod_file, error_msg):
    try:
        with open(os.path.join(mod_info_path, mod_file), "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception as e:
        error_msg(f"Error loading {mod_file}: {str(e)}")
        return None

def download_mod(mod, error_msg):
    try:
        mod_name = mod.get("name", mod.get("MOD NAME", "Unnamed mod"))
        mod_version = mod.get("VERSION", "Unknown")
        mod_url = mod.get("LINK", "")
        source = mod.get("DOWNLOAD FROM", "Unknown")

        version_file_path = os.path.join("Ziped_Mods", f"{mod_name}_version.txt")
        needs_update = mod_needs_update("", version_file_path, mod_version, error_msg)

        if not needs_update and mod_name == "EDF_MML-Core":
            error_msg(f"No update needed for {mod_name}.")
            return

        if not mod_url:
            error_msg(f"No download URL for {mod_name}. Skipping.")
            return

        error_msg(f"Checking update for {mod_name} (Version: {mod_version}, Source: {source})")
        # Placeholder: Simulate download
        error_msg(f"Simulated download for {mod_name} from {mod_url}")
    except Exception as e:
        error_msg(f"Failed to download mod {mod_name}: {str(e)}")

# Placeholder for load_mod_data (adjust based on actual implementation)
def load_mod_data(mod_info_path, mod_file, error_msg):
    try:
        with open(os.path.join(mod_info_path, mod_file), "r") as f:
            return json.load(f)
    except Exception as e:
        error_msg(f"Error loading {mod_file}: {str(e)}")
        return None

# Placeholder for download_mod (adjust based on actual implementation)
def download_mod(mod, error_msg):
    try:
        # Simulate downloading mod (replace with actual logic)
        mod_name = mod.get("name", "Unnamed mod")
        error_msg(f"Downloading mod: {mod_name}")
        # Add actual download logic here
    except Exception as e:
        error_msg(f"Failed to download mod {mod.get('name', 'Unnamed mod')}: {str(e)}")

def handle_error(e, context=""):
    """Handle and log errors more clearly."""
    if context:
        print(f"Error in {context}: {str(e)}")
    else:
        print(f"Error: {str(e)}")

def load_mod_data(mod_info_path, mod_file, error_msg):
    """Load mod data from a JSON file using UTF-8 encoding."""
    try:
        with open(os.path.join(mod_info_path, mod_file), 'r', encoding='utf-8') as file:
            return json.load(file)
    except Exception as e:
        error_msg(f"Failed to load mod data from {mod_file}: {str(e)}")
        return None

def process_mods(mod_data, mods_dir, error_msg):
    """Process each mod in the mod data."""

    # Handle GitHub mods
    for mod in mod_data.get("MOD_INFO", []):
        mod_name = mod.get("MOD NAME")
        source = mod.get('DOWNLOAD FROM')
        if source == 'GITHUB':
            download_from_github(mod)
        elif source == 'NEXUS':
            download_from_nexus(mod)
        else:
            error_msg(f"Unknown download source: {source}")
        mod_url = mod.get("LINK")
        mod_version = mod.get("VERSION")

        if not mod_name or not mod_url or not mod_version:
            error_msg(f"Mod data is incomplete for one of the GitHub mods. Skipping...")
            continue

        mod_file_path = os.path.join(mods_dir, f"{mod_name}.zip")
        version_file_path = os.path.join(mods_dir, f"{mod_name}_version.txt")

        if mod_needs_update(mod_file_path, version_file_path, mod_version, error_msg):
            download_and_save_mod(mod_url, mod_file_path, version_file_path, mod_version, error_msg, source="GitHub")
            error_msg(f"Downloaded and saved {mod_file_path} from GitHub.")
            install_mod(mod_file_path, mods_dir, error_msg)

    # Handle Nexus Mods
    for mod in mod_data.get("NEXUS_INFO", []):
        mod_name = mod.get("MOD NAME")
        mod_url = mod.get("LINK")
        mod_version = mod.get("VERSION")

        if not mod_name or not mod_url or not mod_version:
            error_msg(f"Mod data is incomplete for one of the Nexus mods. Skipping...")
            continue

        mod_file_path = os.path.join(mods_dir, f"{mod_name}.zip")
        version_file_path = os.path.join(mods_dir, f"{mod_name}_version.txt")

        if mod_needs_update(mod_file_path, version_file_path, mod_version, error_msg):
            download_from_nexus(mod_name, mod_url, mod_file_path, version_file_path, mod_version, error_msg)
            error_msg(f"Downloaded and saved {mod_name} from Nexus Mods as {mod_file_path}.")
            install_mod(mod_file_path, mods_dir, error_msg)

    # Final success message
    error_msg("Mod updated successfully")

def install_mod(mod_file_path, mods_dir, error_msg):
    extract_dir = os.path.splitext(mod_file_path)[0]
    install_dir = os.path.join(os.path.dirname(mods_dir), "Mods")

    try:
        if not os.path.exists(install_dir):
            os.makedirs(install_dir)

        # Extract the mod files
        with zipfile.ZipFile(mod_file_path, 'r') as zip_ref:
            zip_ref.extractall(extract_dir)

        # Check for nested directories and move files
        while len(os.listdir(extract_dir)) == 1 and os.path.isdir(os.path.join(extract_dir, os.listdir(extract_dir)[0])):
            extract_dir = os.path.join(extract_dir, os.listdir(extract_dir)[0])

        # Move the files into the Mods folder
        for item in os.listdir(extract_dir):
            source = os.path.join(extract_dir, item)
            destination = os.path.join(install_dir, item)
            if os.path.isdir(source):
                shutil.move(source, destination)
            else:
                shutil.move(source, install_dir)
            error_msg(f"Installed {item} from {mod_file_path}")

        # Clean up the extracted directory
        shutil.rmtree(extract_dir)
    except Exception as e:
        error_msg(f"Failed to install {mod_file_path}: {str(e)}")

def process_r2z_profile(mod_name, error_msg):
    """Process a .r2z file, extracting mod files to target directories while preserving mod folder structure."""
    # Configurable target directories
    config_dir = os.path.join("Mods", "EDF 6 MOD SETTINGS MAKER", "MOD CONFIG DATA PLACED HERE")
    image_dir = os.path.join("Mods", "EDF 6 MOD SETTINGS MAKER", "mml_custom_images")
    
    # Supported file extensions
    supported_extensions = ('.json', '.png')
    
    # r2modman-specific files and patterns to skip
    r2mm_files = [
        "manifest.json", "export.r2x", "changelog.txt", "doorstop_config.ini",
        "config.json", "r2modman_settings.json", "readme.md", "license",
        "requirements.txt"
    ]
    r2mm_patterns = [
        ".github/", ".git/", "__pycache__/", "tests/", "docs/"
    ]

    try:
        r2z_path = os.path.join("Ziped_Mods", f"{mod_name}.r2z")
        if not os.path.exists(r2z_path):
            error_msg(f"❌ R2Z file not found: {r2z_path}")
            return False

        # Calculate checksum for multiplayer verification
        hasher = hashlib.md5()
        with open(r2z_path, 'rb') as f:
            for chunk in iter(lambda: f.read(4096), b''):
                hasher.update(chunk)
        checksum = hasher.hexdigest()
        error_msg(f"ℹ️ R2Z checksum: {checksum}")

        os.makedirs(config_dir, exist_ok=True)
        os.makedirs(image_dir, exist_ok=True)

        with zipfile.ZipFile(r2z_path, 'r') as zip_ref:
            extracted_files = 0
            for file_info in zip_ref.infolist():
                file = file_info.filename

                # Skip directories
                if file_info.is_dir():
                    continue

                # Check for r2modman-specific files or patterns
                base_name = os.path.basename(file).lower()
                if base_name in r2mm_files:
                    error_msg(f"⚠️ Skipped r2modman file in .r2z: {file}")
                    continue
                if any(pattern in file.lower() for pattern in r2mm_patterns):
                    error_msg(f"⚠️ Skipped r2modman-related file in .r2z: {file}")
                    continue

                # Check file extension
                if file.lower().endswith('.png'):
                    target_dir = image_dir
                elif file.lower().endswith(('.json', '.txt', '.cfg')):
                    target_dir = config_dir
                else:
                    error_msg(f"⚠️ Skipped unsupported file in .r2z: {file}")
                    continue

                # Preserve mod folder structure (e.g., ModnameFolder1/Mods/file)
                rel_path = file
                if rel_path.startswith('mods/'):
                    rel_path = rel_path[len('mods/'):]  # Remove 'mods/' prefix
                elif '/mods/' in rel_path:
                    rel_path = rel_path[rel_path.index('/mods/') + len('/mods/'):]  # Extract after '/mods/'
                else:
                    rel_path = os.path.basename(file)  # Fallback to basename if no 'mods/' found

                output_path = os.path.join(target_dir, rel_path)

                # Ensure output directory exists
                os.makedirs(os.path.dirname(output_path), exist_ok=True)

                # Avoid overwriting by appending suffix
                base, ext = os.path.splitext(output_path)
                counter = 1
                while os.path.exists(output_path):
                    output_path = f"{base}_{counter}{ext}"
                    counter += 1

                # Extract file
                with open(output_path, 'wb') as out_file:
                    out_file.write(zip_ref.read(file))
                error_msg(f"✔️ Extracted {file} to {output_path}")
                extracted_files += 1

            if extracted_files == 0:
                error_msg("⚠️ No supported files extracted from .r2z.")
                return False

        error_msg(f"✅ R2Z profile for {mod_name} extracted successfully.")
        return True

    except Exception as e:
        error_msg(f"❌ Failed to process R2Z for {mod_name}: {str(e)}")
        return False

def download_mod(mod, error_msg):
    mod_name = mod.get("MOD NAME")
    mod_url = mod.get("LINK")
    mod_version = mod.get("VERSION")
    source = mod.get('DOWNLOAD FROM (GITHUB|NEXUS)')

    if not mod_name or not mod_url or not mod_version:
        error_msg(f"Missing details for mod: {mod_name}")
        return False

    mod_file_path = os.path.join("Ziped_Mods", f"{mod_name}.zip")
    version_file_path = os.path.join("Ziped_Mods", f"{mod_name}_version.txt")

    # Check if the mod needs an update
    needs_update = mod_needs_update(mod_file_path, version_file_path, mod_version, error_msg)

    if not needs_update:
        # Consolidate to a single message
        error_msg(f"No update needed for {mod_name}.")
        return False

    # Process based on the source of the mod
    try:
        if source == 'GITHUB':
            download_from_github(mod, mod_file_path, version_file_path, mod_version, error_msg)
        elif source == 'NEXUS':
            print("permission to get download links from the API, this is for premium users only")
            return 
            download_from_nexus(
                mod.get("MOD NAME"),
                mod.get("MOD_ID"),  # Ensure the mod dictionary includes MOD_ID
                mod.get("FILE_ID"),  # Ensure the mod dictionary includes FILE_ID
                mod_file_path,
                version_file_path,
                mod_version,
                error_msg
            )

        else:
            error_msg(f"Unknown source for mod {mod_name}.")
            return False

        # After download, proceed to install
        if validate_zip(mod_file_path, error_msg):  # Validate before installing
            install_mod(mod_file_path, "Ziped_Mods", error_msg)
            error_msg(f"{mod_name} updated successfully.")
        else:
            error_msg(f"Failed to install {mod_name}: File is not a valid zip file.")

        return True
    except Exception as e:
        error_msg(f"Failed to download mod {mod_name}: {str(e)}")
        return False

def download_from_github(mod, mod_file_path, version_file_path, mod_version, error_msg):
    """Download a mod from GitHub using the provided information."""
    mod_url = mod.get("LINK")
    
    if not mod_url:
        error_msg(f"Mod {mod.get('MOD NAME')} does not have a valid GitHub link.")
        return
    
    try:
        # Download the mod from GitHub
        response = requests.get(mod_url)
        response.raise_for_status()

        # Save the downloaded mod content
        with open(mod_file_path, 'wb') as file:
            file.write(response.content)

        # Save the version information
        with open(version_file_path, 'w') as version_file:
            version_file.write(mod_version)

        error_msg(f"Downloaded and saved {mod.get('MOD NAME')} from GitHub.")
    except requests.exceptions.RequestException as e:
        error_msg(f"Failed to download {mod.get('MOD NAME')} from GitHub: {str(e)}")

def download_from_nexus(mod_name, mod_id, file_id, mod_file_path, version_file_path, mod_version, error_msg):
    """Download a mod from Nexus Mods using the REST API."""
    
    if not mod_id or not file_id:
        error_msg(f"Invalid mod or file ID for {mod_name}.")
        return False

    try:
        # Load API key
        api_key = "Nexus Mods API KEY"
        if not api_key:
            error_msg("❌ Nexus Mods API key not found.")
            return False

        # Define API headers
        api_headers = {
            'apikey': api_key,
            'Accept': 'application/json',
            'User-Agent': 'EDF MML/0.0.9-R2ModManTest (seanmattingly47@gmail.com)'
        }

        # Construct the API request URL
        api_url = f"https://api.nexusmods.com/v1/games/earthdefenseforce6/mods/{mod_id}/files/{file_id}/download_link.json"
        print(f"🔍 Checking Nexus Mods API: {api_url}")  # Debugging

        response = requests.get(api_url, headers=api_headers)
        
        # Print response status and content
        print(f"🔍 API Response Status: {response.status_code}")
        print(f"🔍 API Response Content: {response.text}")

        if response.status_code == 403:
            error_msg("❌ Access denied. Your API key may lack the required permissions.")
            return False
        if response.status_code == 404:
            error_msg(f"❌ Mod or file not found: {mod_name}. Check the mod ID and file ID.")
            return False

        response.raise_for_status()
        data = response.json()

        # Extract the download URL
        download_url = data.get("download_url")
        if not download_url:
            error_msg(f"❌ No download URL found for {mod_name}.")
            return False

        # Now download the actual mod file
        response = requests.get(download_url, headers=api_headers, stream=True)
        response.raise_for_status()

        # Save the downloaded mod content
        with open(mod_file_path, 'wb') as file:
            for chunk in response.iter_content(chunk_size=8192):
                file.write(chunk)

        # Save version information
        with open(version_file_path, 'w') as version_file:
            version_file.write(mod_version)

        error_msg(f"✅ Successfully downloaded {mod_name} from Nexus Mods.")
        return True

    except requests.exceptions.RequestException as e:
        error_msg(f"❌ Failed to download {mod_name} from Nexus Mods: {str(e)}")
        return False

def mod_needs_update(mod_file_path, version_file_path, latest_version, error_msg):
    """Determine if a mod update is required by comparing local and latest versions."""
    try:
        # If the version file exists, check its contents
        if os.path.isfile(version_file_path):
            with open(version_file_path, 'r') as version_file:
                current_version = version_file.read().strip()

            # Return False if the version matches, indicating no update needed
            if current_version == latest_version:
                error_msg(f"{os.path.basename(mod_file_path)} is up to date.")
                return False

        # Either the file does not exist, or the version does not match, requiring an update
        return True

    except Exception as e:
        error_msg(f"Error checking mod version: {str(e)}")
        return False

def download_and_save_mod(url, mod_file_path, version_file_path, mod_version, error_msg, source="GitHub"):
    """Download and save a mod from the specified source (GitHub or others), then validate the zip file."""
    try:
        response = requests.get(url)
        response.raise_for_status()

        with open(mod_file_path, 'wb') as file:
            file.write(response.content)

        # Validate the downloaded zip file
        if not validate_zip(mod_file_path, error_msg):
            error_msg(f"Validation failed for {mod_file_path}. File is not valid or is corrupted.")
            return

        with open(version_file_path, 'w') as version_file:
            version_file.write(mod_version)

        error_msg(f"Downloaded and saved {mod_file_path} from {source}.")
    except requests.exceptions.RequestException as e:
        error_msg(f"Failed to download {mod_file_path} from {source}: {str(e)}")

#====================================================================================================

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
    return settings.get("colors", {}).get("TextColor", "#B3FF00")  # Default to Lime green

def PressedTextColor():
    return settings.get("colors", {}).get("PressedTextColor", "#ffffff")  # Default to white

operation_in_progress = False # Track operation status to avoid multiple simultaneous actions

#====================================================================================================

#TODO
'''
User Interface Enhancements:
Fix Mod Pack data
Figgure out why the tooltips are not working
# Add tooltips to buttons
'''


def toggle_mods_panels(error_msg, parent_dir=".", TextColor=hover_fg(), hover_bg=hover_bg()):
    # Define the directory where Mod_config_data.json files are located
    mod_config_dir = os.path.join(parent_dir, "Mods", "EDF 6 MOD SETTINGS MAKER", "MOD CONFIG DATA PLACED HERE")
    dark_bg = "#000000"  # Set the dark background color
    profile_path = os.path.join(mod_config_dir, 'MML_Profiles.txt')
    scrollbar_color = TextColor
    operation_in_progress = False

    def add_tooltip(widget, text):
        """Add a tooltip to a widget."""
        tooltip = tk.Toplevel(widget)
        tooltip.withdraw()
        tooltip.wm_overrideredirect(True)
        tooltip.configure(bg="#333333")
        label = tk.Label(
            tooltip,
            text=text,
            bg=JustBackGround(),
            fg=TextColor(),
            font=("Arial", 10),
            bd=1,
            relief="solid",
            padx=4,
            pady=2
        )
        label.pack()
        def enter(event):
            x = event.x_root + 10
            y = event.y_root + 10
            tooltip.wm_geometry(f"+{x}+{y}")
            tooltip.deiconify()
        def leave(event):
            tooltip.withdraw()
        widget.bind("<Enter>", enter, add="+")
        widget.bind("<Leave>", leave, add="+")

    def apply_hover_effect(button, hover_bg=hover_bg, hover_fg=TextColor, normal_bg=None, normal_fg=None):
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

    # Function to retrieve categories from the mod's JSON data
    def get_mod_categories(file_name):
        try:
            file_path = os.path.join(mod_config_dir, file_name)
            with open(file_path, 'r', encoding='utf-8') as config_file:
                config_data = json.load(config_file)
                return config_data.get('CATEGORIES', ["Other"])
        except Exception as e:
            print(f"Failed to load categories for {file_name}: {e}")
            return ["Other"]

    # Aggregate all unique categories from mods
    def get_all_categories():
        categories = set()
        current_files = [f for f in os.listdir(mod_config_dir) if f.endswith('.json') or f.endswith('.disabled')]
        for file in current_files:
            mod_categories = get_mod_categories(file)
            categories.update(mod_categories)
        return ["All"] + sorted(list(categories))

    def update_files(filter_text="", selected_category="All"):
        for widget in scrollable_frame.winfo_children():
            widget.destroy()

        current_files = [f for f in os.listdir(mod_config_dir) if f.endswith('.json') or f.endswith('.disabled')]
        filtered_files = []
        for file in current_files:
            if filter_text.lower() in file.lower():
                if selected_category == "All" or selected_category in get_mod_categories(file):
                    filtered_files.append(file)

        for file in filtered_files:
            file_label = tk.Label(scrollable_frame, text=file, bg=dark_bg, fg="#FFFFFF", font=("AR UDJingXiHeiB5", 10))
            file_label.pack(anchor="w", pady=5)

            button_frame = tk.Frame(scrollable_frame, bg=dark_bg)
            button_frame.pack(anchor="w", pady=2)

            enable_btn = tk.Button(button_frame, text="Enable", bg=ButtonBackGround(), fg="#FFFFFF", activebackground="#010e70", activeforeground="#FFFFFF", command=lambda f=file: enable_file(f))
            apply_hover_effect(enable_btn)
            disable_btn = tk.Button(button_frame, text="Disable", bg=ButtonBackGround(), fg="#FFFFFF", activebackground="#010e70", activeforeground="#FFFFFF", command=lambda f=file: disable_file(f))
            apply_hover_effect(disable_btn)
            uninstall_btn = tk.Button(button_frame, text="Uninstall", bg=ButtonBackGround(), fg="#FFFFFF", activebackground="#010e70", activeforeground="#FFFFFF", command=lambda f=file: uninstall_a_mod(f))
            apply_hover_effect(uninstall_btn)
            info_btn = tk.Button(button_frame, text="INFO", bg=ButtonBackGround(), fg="#FFFFFF", activebackground="#010e70", activeforeground="#FFFFFF", command=lambda f=file: info_file(f))
            apply_hover_effect(info_btn)
            edit_btn = tk.Button(button_frame, text="EDIT", bg=ButtonBackGround(), fg="#FFFFFF", activebackground="#010e70", activeforeground="#FFFFFF", command=lambda f=file: edit_file(f))
            apply_hover_effect(edit_btn)

            enable_btn.pack(side="left", padx=10)
            disable_btn.pack(side="left", padx=10)
            uninstall_btn.pack(side="left", padx=10)
            info_btn.pack(side="left", padx=10)
            edit_btn.pack(side="left", padx=10)

    def enable_file(file):
        nonlocal operation_in_progress
        if operation_in_progress:
            error_msg("Operation already in progress. Please wait.")
            return
        
        file_path = os.path.join(mod_config_dir, file)
        new_path = file_path.replace('.disabled', '.json')
        try:
            operation_in_progress = True
            if not os.path.exists(file_path):
                error_msg(f"File not found: {file_path}")
                return

            os.rename(file_path, new_path)
            error_msg(f"Enabled: {file}")
            update_files(search_entry.get(), category_var.get())
        except Exception as e:
            error_msg(f"Failed to enable {file}: {e}")
        finally:
            operation_in_progress = False

    def disable_file(file):
        nonlocal operation_in_progress
        if operation_in_progress:
            error_msg("Operation already in progress. Please wait.")
            return

        file_path = os.path.join(mod_config_dir, file)
        new_path = file_path.replace('.json', '.disabled')
        try:
            operation_in_progress = True
            if not os.path.exists(file_path):
                error_msg(f"File not found for disabling: {file_path}")
                return

            os.rename(file_path, new_path)
            error_msg(f"Disabled: {file}")
            update_files(search_entry.get(), category_var.get())
        except Exception as e:
            error_msg(f"Failed to disable {file}: {e}")
        finally:
            operation_in_progress = False

    def uninstall_a_mod(file):
        try:
            file_path = os.path.join(mod_config_dir, file)
            if os.path.exists(file_path):
                base_dir = os.path.abspath(os.path.join(os.path.dirname(file_path), "..", ".."))
                # Assuming `uninstaller` is defined elsewhere
                uninstaller.load_manifest_and_uninstall(file_path, base_dir)
                error_msg("Mod uninstalled successfully.")
                os.remove(file_path)
                error_msg(f"Manifest file removed: {file_path}")
                update_files(search_entry.get(), category_var.get())
            else:
                error_msg(f"File not found: {file_path}")
        except Exception as e:
            error_msg(str(e))

    def info_file(file):
        file_path = os.path.join(mod_config_dir, file)
        try:
            with open(file_path, 'r', encoding='utf-8') as config_file:
                config_data = json.load(config_file)

            mod_name = config_data.get('MOD_INFO', [{}])[0].get('MOD NAME', 'Unknown Mod')
            changelog = config_data.get('CHANGELOG', ['CHANGELOG not found'])
            author = config_data.get('MOD_INFO', [{}])[0].get('AUTHOR', 'AUTHOR not found')

            changelog_label.config(text=f"CHANGELOG For {mod_name}     |")
            changelog_text.config(state=tk.NORMAL)
            changelog_text.delete(1.0, tk.END)
            changelog_text.insert(tk.END, "\n".join(changelog))
            changelog_text.config(state=tk.DISABLED)
            author_label.config(text=f"Made by {author}")
        except Exception as e:
            error_msg(f"Failed to read config variables from {file_path}: {e}")

    def edit_file(file):
            """Open the mod's JSON file in the default text editor."""
            try:
                file_path = os.path.join(mod_config_dir, file)
                if not os.path.exists(file_path):
                    error_msg(f"File not found: {file_path}")
                    return
                # Use os.startfile on Windows or subprocess for cross-platform compatibility
                if os.name == 'nt':  # Windows
                    os.startfile(file_path)
                else:  # Linux/Mac
                    subprocess.run(['xdg-open', file_path])
                error_msg(f"Opened {file} in default text editor.")
            except Exception as e:
                error_msg(f"Failed to open {file} for editing: {e}")

    def save_profile():
        profile_name = profile_entry.get().strip()
        if not profile_name or profile_name == "Profile Name?":
            error_msg("Profile name cannot be empty.")
            return
        if profile_name == "LOAD PROFILE":
            error_msg("Invalid profile name: 'LOAD PROFILE' is reserved.")
            return
        try:
            current_files = [f for f in os.listdir(mod_config_dir) if f.endswith('.json') or f.endswith('.disabled')]
            profile_data = {file.replace('.json', '').replace('.disabled', ''): '1' if file.endswith('.json') else '0' 
                           for file in current_files}
            profile_line = f"{profile_name}: {{{', '.join(f'{k}:{v}' for k, v in profile_data.items())}}}"
            profiles = []
            if os.path.exists(profile_path):
                with open(profile_path, 'r') as profile_file:
                    profiles = profile_file.readlines()
            with open(profile_path, 'w') as profile_file:
                profile_file.write(f"LOAD PROFILE = {profile_name}\n")
                written_profiles = set()
                for line in profiles:
                    if line.strip() and not line.startswith("LOAD PROFILE"):
                        name = line.split(":", 1)[0].strip()
                        if name not in written_profiles:
                            profile_file.write(line)
                            written_profiles.add(name)
                if profile_name not in written_profiles:
                    profile_file.write(profile_line + '\n')
            update_profiles_list()
            update_selected_mods_list(profile_name)
            error_msg(f"Profile '{profile_name}' saved and set as active.")
            profile_entry.delete(0, tk.END)
        except Exception as e:
            error_msg(f"Failed to save profile: {e}")

    def load_profile():
        try:
            # Use profile_listbox only, since quick_profile_listbox was removed
            selected_index = profile_listbox.curselection()
            if not selected_index:
                error_msg("No profile selected.")
                return
            selected_profile = profile_listbox.get(selected_index)[0].split(',')[0].strip()
            if not os.path.exists(profile_path):
                error_msg("No profiles file found.")
                return
            with open(profile_path, 'r') as profile_file:
                profiles = profile_file.readlines()
            profile_found = False
            for line in profiles:
                if line.startswith(f"{selected_profile}:"):
                    profile_found = True
                    mod_data = line.split(":", 1)[1].strip().strip("{}")
                    mod_entries = [entry.strip().split(":") for entry in mod_data.split(",") if ':' in entry]
                    for mod_name, status in mod_entries:
                        mod_name = mod_name.strip()
                        json_file = f"{mod_name}.json"
                        disabled_file = f"{mod_name}.disabled"
                        json_path = os.path.join(mod_config_dir, json_file)
                        disabled_path = os.path.join(mod_config_dir, disabled_file)
                        if status.strip() == '1':
                            if os.path.exists(disabled_path):
                                enable_file(disabled_file)
                            elif not os.path.exists(json_path):
                                error_msg(f"Mod {json_file} not found; skipping.")
                        elif status.strip() == '0':
                            if os.path.exists(json_path):
                                disable_file(json_file)
                            elif not os.path.exists(disabled_path):
                                error_msg(f"Mod {disabled_file} not found; skipping.")
                    break
            if not profile_found:
                error_msg(f"Profile '{selected_profile}' not found.")
                return
            with open(profile_path, 'w') as profile_file:
                profile_file.write(f"LOAD PROFILE = {selected_profile}\n")
                for line in profiles:
                    if not line.startswith("LOAD PROFILE ="):
                        profile_file.write(line)
            update_files(search_entry.get(), category_var.get())
            update_selected_mods_list(selected_profile)
            error_msg(f"Profile '{selected_profile}' loaded successfully.")
        except Exception as e:
            error_msg(f"Failed to load profile: {e}")

    def export_profile():
            """Export all .json files from the current profile as an .r2z zip file."""
            nonlocal operation_in_progress
            if operation_in_progress:
                error_msg("Operation already in progress. Please wait.")
                return
            try:
                operation_in_progress = True
                current_profile = current_profile_label.cget("text")
                if not current_profile or current_profile == "No Profile Selected":
                    error_msg("No profile is currently selected.")
                    return
                # Read the profile data
                if not os.path.exists(profile_path):
                    error_msg("No profiles file found.")
                    return
                profile_data = None
                with open(profile_path, 'r') as profile_file:
                    profiles = profile_file.readlines()
                    for line in profiles:
                        if line.startswith(f"{current_profile}:"):
                            profile_data = line.split(":", 1)[1].strip().strip("{}")
                            break
                if not profile_data:
                    error_msg(f"Profile '{current_profile}' not found.")
                    return
                # Get enabled mods (.json files)
                mod_entries = [entry.strip().split(":") for entry in profile_data.split(",") if ':' in entry]
                enabled_mods = [mod_name.strip() + ".json" for mod_name, status in mod_entries if status.strip() == '1']
                if not enabled_mods:
                    error_msg("No enabled mods in the current profile to export.")
                    return
                # Prompt user for save location
                zip_name = f"{current_profile}_mods.r2z"
                save_path = filedialog.asksaveasfilename(
                    defaultextension=".r2z",
                    initialfile=zip_name,
                    filetypes=[("R2Z files", "*.r2z"), ("All files", "*.*")],
                    title="Save Profile as R2Z"
                )
                if not save_path:
                    error_msg("Export cancelled by user.")
                    return
                # Create the .r2z zip file
                with zipfile.ZipFile(save_path, 'w', zipfile.ZIP_DEFLATED) as zip_ref:
                    for mod_file in enabled_mods:
                        mod_file_path = os.path.join(mod_config_dir, mod_file)
                        if os.path.exists(mod_file_path):
                            # Store in 'mods/' directory structure like r2modman
                            arcname = os.path.join("mods", mod_file)
                            zip_ref.write(mod_file_path, arcname)
                            error_msg(f"Added {mod_file} to {zip_name}")
                        else:
                            error_msg(f"Warning: {mod_file} not found, skipped.")
                # Calculate and log checksum
                hasher = hashlib.md5()
                with open(save_path, 'rb') as f:
                    for chunk in iter(lambda: f.read(4096), b''):
                        hasher.update(chunk)
                checksum = hasher.hexdigest()
                error_msg(f"Exported profile '{current_profile}' as {zip_name} (Checksum: {checksum})")
            except Exception as e:
                error_msg(f"Failed to export profile: {str(e)}")
            finally:
                operation_in_progress = False

    def remove_profile():
        try:
            # Use profile_listbox only, since quick_profile_listbox was removed
            selected_index = profile_listbox.curselection()
            if not selected_index:
                error_msg("No profile selected.")
                return
            selected_profile = profile_listbox.get(selected_index)[0].split(',')[0].strip()
            if selected_profile == current_profile_label.cget("text"):
                error_msg("Cannot remove the current profile!")
                return
            profiles = []
            active_profile_line = "LOAD PROFILE = Default\n"
            if os.path.exists(profile_path):
                with open(profile_path, 'r') as profile_file:
                    profiles = profile_file.readlines()
                    for line in profiles:
                        if line.strip().startswith("LOAD PROFILE ="):
                            active_profile_line = line
                            break
            with open(profile_path, 'w') as profile_file:
                profile_file.write(active_profile_line)
                for line in profiles:
                    if line.strip() and not line.startswith(selected_profile + ":") and not line.startswith("LOAD PROFILE ="):
                        profile_file.write(line)
            update_profiles_list()
            error_msg(f"Profile '{selected_profile}' removed.")
        except Exception as e:
            error_msg(f"Failed to remove profile: {e}")

    def update_profiles_list():
        profile_listbox.delete(0, tk.END)
        profiles = []
        if os.path.exists(profile_path):
            with open(profile_path, 'r') as profile_file:
                profiles = profile_file.readlines()
        for line in profiles:
            try:
                if line.strip() == "LOAD PROFILE" or line.startswith("LOAD PROFILE ="):
                    continue
                line = line.strip()
                if not line or ':' not in line:
                    continue
                profile_name, mod_data = line.split(":", 1)
                profile_name = profile_name.strip()
                mod_data = mod_data.strip().strip("{}")
                mod_entries = [entry.strip() for entry in mod_data.split(",") if entry.strip() and ':' in entry]
                total_count = 0
                for entry in mod_entries:
                    if ':' in entry:
                        mod_name, status = entry.split(":", 1)
                        status = status.strip()
                        if status in ['1', '0']:
                            total_count += 1
                profile_listbox.insert(tk.END, (profile_name, total_count))
            except Exception as e:
                error_msg(f"Failed to parse profile line: {line}, Error: {e}")

    def update_selected_mods_list(profile_name):
        selected_mods_listbox.delete(0, tk.END)
        current_profile_label.config(text=f"Loaded Profile: {profile_name}")
        if not os.path.exists(profile_path):
            return
        with open(profile_path, 'r') as profile_file:
            profiles = profile_file.readlines()
        for line in profiles:
            if line.startswith(f"{profile_name}:"):
                mod_data = line.split(":", 1)[1].strip().strip("{}")
                mod_entries = [entry.strip() for entry in mod_data.split(",") if entry.strip() and ':' in entry]
                for entry in mod_entries:
                    if ':' in entry:
                        mod_name, status = entry.split(":", 1)
                        mod_name = mod_name.strip()
                        status = status.strip()
                        if status == '1':
                            selected_mods_listbox.insert(tk.END, mod_name)
                break

    def load_active_profile_on_startup():
        if not os.path.exists(profile_path):
            with open(profile_path, 'w') as profile_file:
                profile_file.write("LOAD PROFILE = Default\n")
                profile_file.write("Default: {}\n")
            error_msg("No profile file found; created default.")
            update_selected_mods_list("Default")
            update_files(search_entry.get(), category_var.get())
            profile_listbox.select_set(0)
            return
        active_profile = None
        with open(profile_path, 'r') as profile_file:
            profiles = profile_file.readlines()
            for line in profiles:
                if line.startswith("LOAD PROFILE ="):
                    active_profile = line.split("=", 1)[1].strip()
                    break
        if not active_profile and profiles:
            active_profile = profiles[1].split(":", 1)[0].strip() if len(profiles) > 1 else "Default"
        if active_profile:
            profile_found = False
            for line in profiles:
                if line.startswith(f"{active_profile}:"):
                    profile_found = True
                    mod_data = line.split(":", 1)[1].strip().strip("{}")
                    mod_entries = [entry.strip().split(":") for entry in mod_data.split(",") if ':' in entry]
                    for mod_name, status in mod_entries:
                        mod_name = mod_name.strip()
                        json_file = f"{mod_name}.json"
                        disabled_file = f"{mod_name}.disabled"
                        json_path = os.path.join(mod_config_dir, json_file)
                        disabled_path = os.path.join(mod_config_dir, disabled_file)
                        if status.strip() == '1' and os.path.exists(disabled_path):
                            enable_file(disabled_file)
                        elif status.strip() == '0' and os.path.exists(json_path):
                            disable_file(json_file)
                    break
            if not profile_found:
                error_msg(f"Active profile '{active_profile}' not found; using default state.")
            update_selected_mods_list(active_profile)
            update_files(search_entry.get(), category_var.get())
            error_msg(f"Loaded active profile '{active_profile}' on startup.")
            for i in range(profile_listbox.size()):
                if profile_listbox.get(i)[0] == active_profile:
                    profile_listbox.select_set(i)
                    break

    def create_search_and_filter_controls(parent_frame):
        search_frame = tk.Frame(parent_frame, bg=ButtonBackGround())
        search_frame.pack(fill='x', pady=10)

        search_label = tk.Label(search_frame, text="Search Mods:", bg=ButtonBackGround(), fg="#FFFFFF")
        search_label.pack(side='left', padx=10)
        search_entry = tk.Entry(search_frame, bg=ButtonBackGround(), fg="#FFFFFF", width=30)
        search_entry.pack(side='left', padx=10)

        category_label = tk.Label(search_frame, text="Filter by Category:", bg=ButtonBackGround(), fg="#FFFFFF")
        category_label.pack(side='left', padx=10)
        category_var = tk.StringVar(value="All")
        category_menu = tk.OptionMenu(search_frame, category_var, *get_all_categories())
        category_menu.config(bg=ButtonBackGround(), fg="#FFFFFF", activebackground="#555555", activeforeground="#FFFFFF")
        category_menu["menu"].config(bg=ButtonBackGround(), fg="#FFFFFF", activebackground="#555555", activeforeground="#FFFFFF")
        category_menu.pack(side='left', padx=10)

        filter_btn = tk.Button(search_frame, text="Apply Filter", bg=ButtonBackGround(), fg="#FFFFFF", activebackground="#010e70", activeforeground="#FFFFFF", command=lambda: update_files(search_entry.get(), category_var.get()))
        apply_hover_effect(filter_btn) #, tooltip_text="Apply search and category filters")
        filter_btn.pack(side='left', padx=10)

        return search_entry, category_var

    # Create a new window
    window = tk.Toplevel()
    window.title("Mods Panel")
    window.geometry("1650x600")

    # Create frames
    left_frame = tk.Frame(window, bg=dark_bg)  # Changelog
    center_frame = tk.Frame(window, bg=dark_bg)  # Mod List
    right_frame = tk.Frame(window, bg=dark_bg)  # Profiles
    left_frame.pack(side="left", fill="both", expand=True, padx=(5, 0), pady=5)
    center_frame.pack(side="left", fill="both", expand=True, padx=5, pady=5)
    right_frame.pack(side="left", fill="both", expand=True, padx=(0, 5), pady=5)

    # Configure weights for width distribution (1:3:2 ratio)
    window.pack_propagate(False)  # Prevent window from resizing based on content
    window.update()  # Ensure geometry is applied
    window.pack_propagate(True)
    window.grid_columnconfigure(0, weight=2)  # Left frame
    window.grid_columnconfigure(1, weight=3)  # Center frame
    window.grid_columnconfigure(2, weight=1)  # Right frame

    # Left Frame: Changelog
    search_entry, category_var = create_search_and_filter_controls(left_frame)
    canvas = tk.Canvas(left_frame, bg=dark_bg)
    scrollbar = tk.Scrollbar(left_frame, troughcolor=scrollbar_color, orient="vertical", command=canvas.yview, bg=ButtonBackGround(), width=15)
    scrollable_frame = tk.Frame(canvas, bg=dark_bg)

    scrollable_frame.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
    canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
    canvas.configure(yscrollcommand=scrollbar.set)
    canvas.pack(side="left", fill="both", expand=True)
    scrollbar.pack(side="left", fill="y")

    # Center Frame: Mod List

    changelog_author_frame = tk.Frame(center_frame, bg=dark_bg)
    changelog_author_frame.pack(anchor="nw", padx=10, pady=(5, 5))  # Adjusted pady for consistency
    changelog_label = tk.Label(changelog_author_frame, text="CHANGELOG      |", bg=dark_bg, fg="#FFFFFF")
    changelog_label.pack(side="left", padx=5)
    author_label = tk.Label(changelog_author_frame, text="Made by MOD AUTHOR HERE (INFO)", bg=dark_bg, fg="#FFFFFF")
    author_label.pack(side="right", anchor="ne", padx=5)

    changelog_frame = tk.Frame(center_frame, bg=dark_bg)
    changelog_frame.pack(fill="both", expand=True, padx=10, pady=(0, 5))  # Adjusted pady for consistency
    changelog_scrollbar = tk.Scrollbar(changelog_frame, orient="vertical", troughcolor="#FFFFFF", command=lambda *args: changelog_text.yview(*args), bg=ButtonBackGround(), width=15)
    changelog_text = tk.Text(changelog_frame, wrap="word", bg=dark_bg, fg="#FFFFFF", state=tk.DISABLED)
    changelog_text.config(yscrollcommand=changelog_scrollbar.set)
    changelog_scrollbar.pack(side="right", fill="y")
    changelog_text.pack(side="left", fill="both", expand=True)

    # Right Frame: Profiles
    # Profile List (Mod Profiles List, At the Top, Non-Scalable, With Scrollbar)
    profile_frame = tk.Frame(right_frame, bg=dark_bg)
    profile_frame.pack(pady=5)

    # "Mod Profile List" label
    profile_list_label = tk.Label(profile_frame, text="Mod Profile List", bg=dark_bg, fg="#FFFFFF", font=("Arial", 12, "bold"))
    profile_list_label.pack(padx=10)

    # Add profile_listbox with ttk.Scrollbar
    profile_listbox = tk.Listbox(profile_frame, width=50, height=7, bg=dark_bg, fg="#FFFFFF", selectbackground="#4682B4", highlightthickness=0, selectmode=tk.SINGLE)
    profile_scrollbar = ttk.Scrollbar(profile_frame, orient="vertical", command=profile_listbox.yview)
    profile_listbox.configure(yscrollcommand=profile_scrollbar.set)

    profile_listbox.pack(side="left", padx=(10, 0), pady=0)
    profile_scrollbar.pack(side="right", fill="y", pady=0)

    # Profile Entry
    profile_entry = tk.Entry(right_frame, bg=ButtonBackGround(), fg="#FFFFFF", width=40)
    profile_entry.insert(0, "Profile Name?")
    profile_entry.config(fg="#B3B3B3")

    def clear_placeholder(event):
        if profile_entry.get() == "Profile Name?":
            profile_entry.delete(0, tk.END)
            profile_entry.config(fg="#FFFFFF")

    def restore_placeholder(event):
        if not profile_entry.get().strip():
            profile_entry.insert(0, "Profile Name?")
            profile_entry.config(fg="#B3B3B3")

    profile_entry.bind("<FocusIn>", clear_placeholder)
    profile_entry.bind("<FocusOut>", restore_placeholder)
    profile_entry.pack(pady=10, padx=10)

    profile_btn_frame = tk.Frame(right_frame, bg=ButtonBackGround())
    profile_btn_frame.pack(pady=10)

    save_profile_btn = tk.Button(profile_btn_frame, text="Save Profile", bg=ButtonBackGround(), fg="#FFFFFF", activebackground="#010e70", activeforeground="#FFFFFF", command=save_profile)
    apply_hover_effect(save_profile_btn)
    save_profile_btn.pack(side="left", padx=5)

    remove_profile_btn = tk.Button(profile_btn_frame, text="Remove Profile", bg=ButtonBackGround(), fg="#FFFFFF", activebackground="#010e70", activeforeground="#FFFFFF", command=remove_profile)
    apply_hover_effect(remove_profile_btn)
    remove_profile_btn.pack(side="left", padx=5)

    load_profile_btn = tk.Button(profile_btn_frame, text="Load Profile", bg=ButtonBackGround(), fg="#FFFFFF", activebackground="#010e70", activeforeground="#FFFFFF", command=load_profile)
    apply_hover_effect(load_profile_btn)
    load_profile_btn.pack(side="left", padx=5)

    export_profile_btn = tk.Button(profile_btn_frame, text="Export Profile", bg=ButtonBackGround(), fg="#FFFFFF", activebackground="#010e70", activeforeground="#FFFFFF", command=export_profile)
    apply_hover_effect(export_profile_btn)
    export_profile_btn.pack(side="left", padx=5)

    # Current Profile Section (At the Bottom, Scalable, With Scrollbar)
    current_profile_frame = tk.Frame(right_frame, bg=dark_bg)
    current_profile_frame.pack(fill="both", expand=True, pady=5)

    current_profile_label = tk.Label(current_profile_frame, text="Loaded Profile: No Profile Selected", bg=dark_bg, fg="#FFFFFF", font=("Arial", 12, "bold"))
    current_profile_label.pack(padx=10)

    # Add selected_mods_listbox with ttk.Scrollbar
    selected_mods_frame = tk.Frame(current_profile_frame, bg=dark_bg)
    selected_mods_frame.pack(fill="both", expand=True, padx=0, pady=5)

    selected_mods_listbox = tk.Listbox(selected_mods_frame, width=50, height=15, bg=dark_bg, fg="#FFFFFF", selectbackground="#4682B4", highlightthickness=0)
    selected_mods_scrollbar = ttk.Scrollbar(selected_mods_frame, orient="vertical", command=selected_mods_listbox.yview)
    selected_mods_listbox.configure(yscrollcommand=selected_mods_scrollbar.set)

    selected_mods_listbox.pack(side="left", fill="both", expand=True, padx=(0, 0), pady=0)
    selected_mods_scrollbar.pack(side="right", fill="y", pady=0)

    # Load existing profiles and set up on startup
    if not os.path.exists(profile_path):
        with open(profile_path, 'w') as profile_file:
            profile_file.write("LOAD PROFILE = Default\n")
            profile_file.write("Default: {}\n")
        error_msg("Created default profile file.")
    load_active_profile_on_startup()
    update_profiles_list()
    update_files()

#====================================================================================================
# END OF THE MOD PANEL