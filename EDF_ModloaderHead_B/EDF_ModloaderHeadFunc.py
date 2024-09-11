# EDF_ModloaderHeadFunc.py

import os
import sys
import shutil
import requests
import subprocess
import json
from tkinter import messagebox
import webbrowser
import zipfile

settings_file = "settings.json"

def load_settings():
    """Load settings from a JSON file."""
    if os.path.exists(settings_file):
        with open(settings_file, 'r') as file:
            return json.load(file)
    # Default settings if the file doesn't exist
    return {"edf6_platform": "steam"}  # Default to Steam

def save_settings(settings):
    """Save settings to a JSON file."""
    with open(settings_file, 'w') as file:
        json.dump(settings, file, indent=4)

settings = load_settings()

# Set the global variable for the script directory
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__ if '__file__' in globals() else sys.executable))

# Go back one directory and then navigate to the desired script path
parent_dir = os.path.dirname(SCRIPT_DIR)
modloader_status_file = "winmm.dll"

# Define the directory for saving and unpacking updates
UPDATE_DIR = os.path.dirname(SCRIPT_DIR)
PLUGIN_DIRS = {
    "EARTH DEFENSE FORCE 4.1": "Plugins41",
    "EARTH DEFENSE FORCE 5": "Plugins5",
    "EARTH DEFENSE FORCE 6": "Plugins6",
}

#====================================================================================================
#TABLES

# Runs ConfigBuildAll.py Murges all the mods for EDF 6 so far
def build_tables(error_msg):
    try:
        script_path = os.path.join(parent_dir, "Mods", "EDF 6 MOD SETTINGS MAKER", "ConfigBuildAll.py")
        
        result = subprocess.run(["python", script_path], capture_output=True, text=True, shell=True)
        error_msg(result.stdout)
        if result.stderr:
            error_msg("Error: " + result.stderr)
    except Exception as e:
        error_msg(str(e))

# Repair Tables: Copy files from a directory and paste them at the parent directory
def repair_tables(error_msg):
    try:
        # Ensure the source directory path uses the executable's directory
        source_dir = os.path.join(parent_dir, "Mods", "EDF 6 MOD SETTINGS MAKER", "DO NOT TOUCH ORIGINAL CONFIG DATA")
        dest_dir = os.path.join(parent_dir, "Mods", "EDF 6 MOD SETTINGS MAKER")
        
        if not os.path.exists(source_dir):
            error_msg(f"Source directory does not exist: {source_dir}")
            return

        if not os.path.exists(dest_dir):
            error_msg(f"Destination directory does not exist: {dest_dir}")
            return

        for filename in os.listdir(source_dir):
            full_file_path = os.path.join(source_dir, filename)
            if os.path.isfile(full_file_path):
                shutil.copy(full_file_path, dest_dir)
        error_msg("Tables repaired successfully.")
    except Exception as e:
        error_msg(f"Failed to repair tables: {str(e)}")

#====================================================================================================

def open_save_folder(error_msg, game_key=None):
    try:
        # Updated save paths based on your input
        game_save_paths = {
            "EARTH DEFENSE FORCE 4.1": os.path.join(os.getenv('USERPROFILE'), "Documents", "My Games", "EDF4.1", "SAVE_DATA"),
            "EARTH DEFENSE FORCE 5": os.path.join(os.getenv('USERPROFILE'), "Documents", "My Games", "EDF5", "SAVE_DATA"),
            "EARTH DEFENSE FORCE 6": os.path.join(os.getenv('LOCALAPPDATA'), "EarthDefenceForce6")
        }

        if game_key and game_key in game_save_paths:
            save_folder_path = game_save_paths[game_key]
            if os.path.exists(save_folder_path):
                subprocess.Popen(f'explorer {save_folder_path}')
            else:
                error_msg(f"Save folder does not exist: {save_folder_path}")
        else:
            error_msg("Could not determine the game folder. Please check the folder structure.")
    except Exception as e:
        error_msg(f"Failed to open save folder: {str(e)}")

def launch_game(app_ids, error_msg):
    try:
        # Reload settings to ensure the latest platform choice is used
        current_settings = load_settings()  # Reload settings from the file
        current_platform = current_settings.get("edf6_platform", "steam")  # Get the current platform choice
        
        if current_platform == "steam" and app_ids[0].isdigit():  # Launch via Steam
            steam_command = f"steam://run/{app_ids[0]}"
            subprocess.run(["start", steam_command], shell=True)
            error_msg(f"Launching EDF game with Steam App ID: {app_ids[0]}")
        elif current_platform == "epic" and len(app_ids) > 1:  # Launch via Epic Games Store
            epic_command = f"com.epicgames.launcher://apps/{app_ids[1]}?action=launch&silent=true"
            subprocess.run(["start", epic_command], shell=True)
            error_msg(f"Launching EDF game with Epic Games Store App ID: {app_ids[1]}")
        else:
            error_msg("Failed to determine the platform or App ID.")
    except Exception as e:
        error_msg(f"Failed to launch EDF game with App IDs {app_ids}: {str(e)}")

def toggle_modloader_status(error_msg):
    try:
        # Logic to toggle the modloader status (e.g., renaming a file)
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
        return "Missing"  # Modloader file is not found

def show_error(error_msg):
    # Logic to display an error message
    messagebox.showerror("Error", error_msg)

#====================================================================================================

def get_mod_count(error_msg):
    try:
        mod_info_path = "Mods\EDF 6 MOD SETTINGS MAKER\MOD CONFIG DATA PLACED HERE"
        mod_files = [f for f in os.listdir(mod_info_path) if f.endswith(".json")]

        return str(len(mod_files))
    except Exception as e:
        error_msg(f"Failed to count mods: {str(e)}")
        return "0"

def get_patch_count(error_msg):
    try:
        # Logic to count the number of .txt patch files
        count = str(len([file for file in os.listdir("Mods/Patches") if file.endswith(".txt")]))
        return count
    except Exception as e:
        error_msg(f"Failed to count patches: {str(e)}")
        return "0"

def get_plugin_count(error_msg):
    try:
        # Define the patch directory
        Plugins_dir = os.path.join("Mods", "Plugins")

        # Check if Patcher.dll exists
        Plugins_dll_path = os.path.join(Plugins_dir, "Patcher.dll")
        if not os.path.exists(Plugins_dll_path):
            error_msg(f"'Patcher.dll' not found at {Plugins_dll_path}")
            return "0"
        
        # Logic to count the number of patch files
        count = str(len(os.listdir(Plugins_dir)))
        return count
    except Exception as e:
        error_msg(f"Failed to count Plugins: {str(e)}")
        return "0"

#===================================================================================================

def show_help(error_msg):
    try:
        # Logic to show help documentation by launching a web link
        help_url = "https://github.com/KCreator/Earth-Defence-Force-Documentation/wiki"
        webbrowser.open(help_url)
        error_msg(f"Launching mod documentation: {help_url}")
    except Exception as e:
        error_msg(f"Failed to launch help documentation: {str(e)}")

#====================================================================================================
#MODLOADER

def download_and_extract_zip(zip_url, zip_name, extract_to, error_msg):
    """Download a ZIP file from the given URL and extract it, then check for specific .exe files."""
    try:
        # Download the ZIP file
        response = requests.get(zip_url)
        response.raise_for_status()
        zip_path = os.path.join(extract_to, zip_name)
        with open(zip_path, 'wb') as file:
            file.write(response.content)

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
# MODS

def update_mods(error_msg):
    try:
        mod_info_path = os.path.join(parent_dir, "Mods", "EDF 6 MOD SETTINGS MAKER", "MOD CONFIG DATA PLACED HERE")
        mods_dir = "Ziped_Mods"
        # Load all mod files
        mod_files = [f for f in os.listdir(mod_info_path) if f.endswith(".json")]
        for mod_file in mod_files:
            mod_data = load_mod_data(mod_info_path, mod_file, error_msg)
            if mod_data:
                process_mods(mod_data, mods_dir, error_msg)
                
        error_msg("Mods updated successfully")
    except Exception as e:
        error_msg(f"Failed to update mods: {str(e)}")

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
    for mod in mod_data.get("GITHUB_INFO", []):
        mod_name = mod.get("MOD NAME")
        mod_url = mod.get("LINK")
        mod_version = mod.get("VERSION")

        if not mod_name or not mod_url or not mod_version:
            error_msg(f"Mod data is incomplete for one of the mods. Skipping...")
            continue

        mod_file_path = os.path.join(mods_dir, f"{mod_name}.zip")
        version_file_path = os.path.join(mods_dir, f"{mod_name}_version.txt")

        if mod_needs_update(mod_file_path, version_file_path, mod_version, error_msg):
            download_and_save_mod(mod_url, mod_file_path, version_file_path, mod_version, error_msg)

            # Create a temporary folder for extracted mod contents
            extract_dir = os.path.splitext(mod_file_path)[0]
            install_dir = os.path.join(os.path.dirname(mods_dir), "Mods")
            if not os.path.exists(install_dir):
                os.makedirs(install_dir)

            if os.path.exists(extract_dir):
                # Check for nested unnecessary directories
                extracted_items = os.listdir(extract_dir)
                while len(extracted_items) == 1 and os.path.isdir(os.path.join(extract_dir, extracted_items[0])):
                    # Navigate deeper into the single folder to reach actual content
                    extract_dir = os.path.join(extract_dir, extracted_items[0])
                    extracted_items = os.listdir(extract_dir)

                # If a "Mods" folder is found, pull everything out of it
                mods_subfolder_path = os.path.join(extract_dir, "Mods")
                if os.path.exists(mods_subfolder_path) and os.path.isdir(mods_subfolder_path):
                    extracted_items = os.listdir(mods_subfolder_path)
                    extract_dir = mods_subfolder_path

                # Move files from the correct extraction layer, excluding .md files
                for item in extracted_items:
                    source = os.path.join(extract_dir, item)
                    destination = os.path.join(install_dir, item)
                    
                    # Skip .md files
                    if item.lower().endswith('.md'):
                        error_msg(f"Skipping Markdown files are excluded.")
                        continue

                    try:
                        if os.path.isdir(source):
                            shutil.move(source, destination)
                        else:
                            shutil.move(source, install_dir)
                        error_msg(f"Temporarily installed {item} to {install_dir}")
                    except Exception as e:
                        error_msg(f"Failed to temporarily install {item}: {str(e)}")

            # Clean up the extracted directory and remove the ModName folder in Ziped_Mods
            shutil.rmtree(extract_dir, ignore_errors=True)
            if os.path.exists(extract_dir):
                shutil.rmtree(extract_dir, ignore_errors=True)

            # Clean up the ModName folder in Ziped_Mods
            mod_folder_path = os.path.join(mods_dir, mod_name)
            if os.path.exists(mod_folder_path):
                shutil.rmtree(mod_folder_path, ignore_errors=True)

def mod_needs_update(mod_file_path, version_file_path, mod_version, error_msg):
    """Check if the mod needs to be updated."""
    try:
        if os.path.exists(version_file_path):
            with open(version_file_path, 'r') as version_file:
                current_version = version_file.read().strip()
            if current_version == mod_version:
                error_msg(f"{os.path.basename(mod_file_path)} is already up to date.")
                return False
        return True
    except Exception as e:
        error_msg(f"Failed to check mod version: {str(e)}")
        return False

def download_and_save_mod(mod_url, mod_file_path, version_file_path, mod_version, error_msg):
    """Download the mod, save it, and unpack it along with its version."""
    try:
        # Download the mod file
        response = requests.get(mod_url)
        response.raise_for_status()  # Raise an HTTPError for bad responses
        with open(mod_file_path, 'wb') as file:
            file.write(response.content)
        
        # Save the version information
        with open(version_file_path, 'w') as version_file:
            version_file.write(mod_version)
        
        # Unpack the mod file if it is a ZIP archive
        if zipfile.is_zipfile(mod_file_path):
            with zipfile.ZipFile(mod_file_path, 'r') as zip_ref:
                extract_dir = os.path.splitext(mod_file_path)[0]  # Extract to a directory with the same name as the mod file
                os.makedirs(extract_dir, exist_ok=True)  # Create the extract directory if it doesn't exist
                zip_ref.extractall(extract_dir)
            error_msg(f"Downloaded, unpacked, and updated {os.path.basename(mod_file_path)} to version {mod_version}.")
        else:
            error_msg(f"Downloaded {os.path.basename(mod_file_path)} (not a ZIP file) to version {mod_version}.")
    
    except requests.exceptions.RequestException as e:
        error_msg(f"Failed to download {os.path.basename(mod_file_path)}: {str(e)}")
    except zipfile.BadZipFile:
        error_msg(f"Failed to unpack {os.path.basename(mod_file_path)}: Not a valid ZIP file.")
    except Exception as e:
        error_msg(f"Failed to save mod {os.path.basename(mod_file_path)}: {str(e)}")
