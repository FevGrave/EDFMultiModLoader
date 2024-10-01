# EDF_ModloaderHeadFunc.py

import os, sys, shutil, requests, subprocess, json, webbrowser, zipfile, tkinter as tk, ConfigManifestUninstaller as uninstaller
from tkinter import messagebox
import tkinter.filedialog as filedialog

settings_file = "MMLsettings.json"

def load_settings():
    """Load settings from a JSON file, with default fallback and validation."""
    # Define the default settings at the start to ensure it is available for any reference
    default_settings = {
        "edf6_platform": "steam",
        "platform_can_be": "steam|epic",
        "colors": {
            "JustBackGround": "#484848",
            "ButtonBackGround": "#000000",
            "ButtonPressedBackGround": "#010e70",
            "TextColor": "#B3FF00",
            "PressedTextColor": "#ffffff",
            "Helpful Color Blind Site": "https://davidmathlogic.com/colorblind/#%23484848-%23000000-%23010E70-%23B3FF00-%23FFFFFF"
        },
        "modloader_status": "Enabled",
        "modloader_status_can_be": "Enabled|Disabled, DONT EDIT AS THIS IS VISUAL TEXT",
    }

    if os.path.exists(settings_file):
        with open(settings_file, 'r') as file:
            try:
                settings = json.load(file)
                # Validate and fill missing keys with defaults if necessary
                for key, value in default_settings.items():
                    if key not in settings:
                        settings[key] = value
                return settings
            except json.JSONDecodeError:
                # Handle error if settings file is corrupted
                print("Error loading settings, reverting to defaults.")

    # Save default settings to file if the initial load fails
    save_settings(default_settings)
    return default_settings

def save_settings(settings):
    """Save settings to a JSON file."""
    try:
        with open(settings_file, 'w') as file:
            json.dump(settings, file, indent=4)
    except Exception as e:
        print(f"Error saving settings: {e}")

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
        # Logic to toggle the modloader status (Renaming winmm.dll)
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
                
        error_msg("ALL Mods Update Check Done.")
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

    # Handle GitHub mods
    for mod in mod_data.get("GITHUB_INFO", []):
        mod_name = mod.get("MOD NAME")
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
            download_nexus_mod(mod_name, mod_url, mod_file_path, version_file_path, mod_version, error_msg)
            error_msg(f"Downloaded and saved {mod_name} from Nexus Mods as {mod_file_path}.")
            install_mod(mod_file_path, mods_dir, error_msg)

    # Final success message
    error_msg("Mod updated successfully")

def install_mod(mod_file_path, mods_dir, error_msg):
    """Extract and install the mod from the downloaded file."""
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
    mod_name = os.path.basename(mod_file_path).replace('.zip', '')
    mod_folder_path = os.path.join(mods_dir, mod_name)
    if os.path.exists(mod_folder_path):
        shutil.rmtree(mod_folder_path, ignore_errors=True)

def download_nexus_mod(mod_name, url, mod_file_path, version_file_path, mod_version, error_msg):
    """Download a mod from Nexus Mods."""
    try:
        api_key = 'cKc9fBoPSz6hy0SKzuXQ/6nGzApqqLFuaFlEPcQ0qAOI0w==--ifjs30NvY1cduRns--dLgZDtE+L7zcaeSjNm4Eug=='
        api_headers = {
            'Authorization': api_key, # Nexus Mods API key
        }
        download_url = url
        # Make the request to the Nexus Mods API
        response = requests.get(download_url, headers=api_headers)
        response.raise_for_status()

        # Save the downloaded content
        with open(mod_file_path, 'wb') as file:
            file.write(response.content)

        # Save the version information
        with open(version_file_path, 'w') as version_file:
            version_file.write(mod_version)

        error_msg(f"Downloaded and saved {mod_name} from Nexus Mods.")
    except requests.exceptions.RequestException as e:
        error_msg(f"Failed to download {mod_name} from Nexus Mods: {str(e)}")

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

def TextColor():
    return settings.get("colors", {}).get("TextColor", "#B3FF00")  # Default to Lime green

def PressedTextColor():
    return settings.get("colors", {}).get("PressedTextColor", "#ffffff")  # Default to white

# Track operation status to avoid multiple simultaneous actions
operation_in_progress = False

def toggle_mods_panels(error_msg):
    # Define the directory where Mod_config_data.json files are located
    mod_config_dir = os.path.join(parent_dir, "Mods", "EDF 6 MOD SETTINGS MAKER", "MOD CONFIG DATA PLACED HERE")
    dark_bg = "#000000"  # Set the dark background color
    profile_path = os.path.join(mod_config_dir, 'MML_Profiles.txt')

    # Function to refresh the file list and display current states
    def update_files():
        # Clear the current frame contents
        for widget in scrollable_frame.winfo_children():
            widget.destroy()

        # Re-fetch the list of files from the directory
        current_files = [f for f in os.listdir(mod_config_dir) if f.endswith('.json') or f.endswith('.disabled')]

        # Display each file with enable, disable, uninstall, and info buttons
        for file in current_files:
            # Label to display the file name
            file_label = tk.Label(scrollable_frame, text=file, bg=dark_bg, fg=TextColor(), font=("AR UDJingXiHeiB5", 10))
            file_label.pack(anchor="w", pady=2)

            # Frame for the buttons
            button_frame = tk.Frame(scrollable_frame, bg=dark_bg)
            button_frame.pack(anchor="w")

            # Buttons to enable and disable the file
            enable_btn = tk.Button(button_frame, text="Enable", bg=JustBackGround(), fg=TextColor(), activebackground=ButtonPressedBackGround(), activeforeground=PressedTextColor(), command=lambda f=file: enable_file(f))
            disable_btn = tk.Button(button_frame, text="Disable", bg=JustBackGround(), fg=TextColor(), activebackground=ButtonPressedBackGround(), activeforeground=PressedTextColor(), command=lambda f=file: disable_file(f))
            uninstall_btn = tk.Button(button_frame, text="Uninstall", bg=JustBackGround(), fg=TextColor(), activebackground=ButtonPressedBackGround(), activeforeground=PressedTextColor(), command=lambda f=file: uninstall_a_mod(f))
            info_btn = tk.Button(button_frame, text="INFO", bg=JustBackGround(), fg=TextColor(), activebackground=ButtonPressedBackGround(), activeforeground=PressedTextColor(), command=lambda f=file: info_file(f))

            enable_btn.pack(side="left", padx=5)
            disable_btn.pack(side="left", padx=5)
            uninstall_btn.pack(side="left", padx=5)
            info_btn.pack(side="left", padx=5)

    # Function to enable the selected mod configuration file
    def enable_file(file):
        global operation_in_progress
        if operation_in_progress:
            error_msg("Operation already in progress. Please wait.")
            return
        
        file_path = os.path.join(mod_config_dir, file)
        new_path = file_path.replace('.disabled', '.json')
        try:
            # Start the operation and disable further actions
            operation_in_progress = True

            # Check if the file exists before renaming
            if not os.path.exists(file_path):
                error_msg(f"File not found: {file_path}")
                operation_in_progress = False
                return

            os.rename(file_path, new_path)
            error_msg(f"Enabled: {file}")

            # Refresh the file list to update the UI
            update_files()
        except Exception as e:
            error_msg(f"Failed to enable {file}: {e}")
        finally:
            # Reset the operation status to allow further actions
            operation_in_progress = False

    # Function to disable the selected mod configuration file
    def disable_file(file):
        global operation_in_progress
        if operation_in_progress:
            error_msg("Operation already in progress. Please wait.")
            return

        file_path = os.path.join(mod_config_dir, file)
        new_path = file_path.replace('.json', '.disabled')
        try:
            # Start the operation and disable further actions
            operation_in_progress = True

            # Check if the file exists before renaming
            if not os.path.exists(file_path):
                error_msg(f"File not found: {file_path}")
                operation_in_progress = False
                return

            os.rename(file_path, new_path)
            # Refresh the file list to update the UI
            update_files()
            error_msg(f"Disabled: {file}")

        except Exception as e:
            error_msg(f"Failed to disable {file}: {e}")
        finally:
            # Reset the operation status to allow further actions
            operation_in_progress = False

    def uninstall_a_mod(file):
        try:
            # Construct the full path of the selected file to uninstall
            file_path = os.path.join(mod_config_dir, file)

            if os.path.exists(file_path):
                # Set the base path to the directory containing the Mods folder
                base_dir = os.path.abspath(os.path.join(os.path.dirname(file_path), "..", ".."))

                # Use the uninstaller to handle the mod logic while targeting the specific file
                uninstaller.load_manifest_and_uninstall(file_path, base_dir)
                error_msg("Mod uninstalled successfully.")

                # Remove the manifest file after processing
                try:
                    os.remove(file_path)
                    error_msg(f"Manifest file removed: {file_path}")

                    # Refresh the displayed list of files after removal
                    update_files()
                except Exception as e:
                    error_msg(f"Failed to remove manifest file: {file_path}. Error:    {e}")
            else:
                error_msg(f"File not found: {file_path}")
        except Exception as e:
            error_msg(str(e))

    # Function to save a new profile to profiles.txt
    def save_profile():
        profile_name = profile_entry.get().strip()
        if profile_name:
            try:
                # Collect the state of all files to save with the profile
                current_files = [f for f in os.listdir(mod_config_dir) if f.endswith('.json') or f.endswith('.disabled')]
                unique_files = list(set(current_files))  # Ensure uniqueness
                profile_data = [f"({file}, {'1' if file.endswith('.json') else '0'})" for file in unique_files]
                profile_line = f"{profile_name}: {{{', '.join(profile_data)}}}"
                # Save the profile while ensuring no duplicates
                profiles = []
                if os.path.exists(profile_path):
                    with open(profile_path, 'r') as profile_file:
                        profiles = profile_file.readlines()
                # Update the profiles.txt without duplicates
                with open(profile_path, 'w') as profile_file:
                    for line in profiles:
                        if not line.startswith(profile_name + ":"):
                            profile_file.write(line)
                    profile_file.write(profile_line + '\n')
                # Clear the profile listbox to avoid reappending old data
                profile_listbox.delete(0, tk.END)
                # Reload profiles accurately
                for line in profiles:
                    profile_name, mod_data = line.split(":")
                    mod_count = mod_data.count('1') + mod_data.count('0')  # Count actual mod entries
                    profile_listbox.insert(tk.END, f"{profile_name.strip()}, {mod_count} mods")
                # Insert the newly saved profile
                profile_listbox.insert(tk.END, f"{profile_name}, {len(unique_files)} mods")
                error_msg(f"Profile '{profile_name}' saved.")
                profile_entry.delete(0, tk.END)
            except Exception as e:
                error_msg(f"Failed to save profile: {e}")
        else:
            error_msg("Profile name cannot be empty.")

    # Function to remove a selected profile from the list and file
    def remove_profile():
        try:
            selected_index = profile_listbox.curselection()
            if selected_index:
                selected_profile = profile_listbox.get(selected_index).split(',')[0]  # Extract profile name
                profile_listbox.delete(selected_index)

                # Update profiles.txt to remove the selected profile
                with open(profile_path, 'r') as profile_file:
                    profiles = profile_file.readlines()

                with open(profile_path, 'w') as profile_file:
                    for profile in profiles:
                        if not profile.startswith(selected_profile + ":"):
                            profile_file.write(profile)

                error_msg(f"Profile '{selected_profile}' removed.")
            else:
                error_msg("No profile selected.")
        except Exception as e:
            error_msg(f"Failed to remove profile: {e}")

    # Function to load the selected profile and enable/disable mods accordingly
    def load_profile():
        try:
            # Clear existing profile entries in the listbox
            profile_listbox.delete(0, tk.END)
            # Read the profiles from the file
            if os.path.exists(profile_path):
                with open(profile_path, 'r') as profile_file:
                    profiles = profile_file.readlines()
            # Reload the profiles and count mods accurately
            for profile in profiles:
                profile_name = profile.split(":")[0]
                mod_entries = profile.split(":")[1].strip().strip("{}").split(", ")
                unique_mod_files = list(set([entry.split(',')[0][1:] for entry in mod_entries]))  # Ensure uniqueness
                profile_listbox.insert(tk.END, f"{profile_name}, {len(unique_mod_files)} mods")  # Display the correct count
            error_msg("Profile loaded successfully.")
        except Exception as e:
            error_msg(f"Failed to load profile: {e}")

    # Function to enable or disable mods based on the loaded profile
    def enable_disable_mods(mod_files):
        current_files = [f for f in os.listdir(mod_config_dir) if f.endswith('.json') or f.endswith('.disabled')]
        for file in current_files:
            if file in mod_files:
                enable_file(file)
            else:
                disable_file(file)

    # Function to handle file actions (enable, disable, uninstall) and read variables
    def handle_file_action(file, action):
        # Determine file path
        file_path = os.path.join(mod_config_dir, file)

        # Perform the specified action
        if action == 'enable':
            enable_file(file)
        elif action == 'disable':
            disable_file(file)
        elif action == 'uninstall':
            uninstall_a_mod(file)

    # Function to display information (CHANGELOG and AUTHOR) from the file in the UI
    def info_file(file):
        file_path = os.path.join(mod_config_dir, file)
        try:
            # Open the file and load its contents
            with open(file_path, 'r', encoding='utf-8') as config_file:
                config_data = json.load(config_file)

            # Extract CHANGELOG
            changelog = config_data.get('CHANGELOG', ['CHANGELOG not found'])

            # Extract AUTHOR from either NEXUS_INFO or GITHUB_INFO
            author = 'AUTHOR not found'
            for key in ['NEXUS_INFO', 'GITHUB_INFO']:
                if key in config_data:
                    info_list = config_data[key]
                    if isinstance(info_list, list) and len(info_list) > 0:
                        author = info_list[0].get('AUTHOR', 'AUTHOR not found')
                        break

            # Update the CHANGELOG text widget
            changelog_text.config(state=tk.NORMAL)  # Enable editing to update content
            changelog_text.delete(1.0, tk.END)  # Clear existing content
            changelog_text.insert(tk.END, "\n".join(changelog))  # Insert new content
            changelog_text.config(state=tk.DISABLED)  # Disable editing to prevent user modifications

            # Update the AUTHOR label
            author_label.config(text=f"Made by {author}")

        except Exception as e:
            error_msg(f"Failed to read config variables from {file_path}: {e}")

    # Create a new window
    window = tk.Toplevel()
    window.title("Mods Panel")
    window.geometry("1500x500")

    # Create frames for file toggling and profiles
    left_frame = tk.Frame(window, padx=10, pady=10, bg=dark_bg)
    right_frame = tk.Frame(window, padx=10, pady=10, bg=dark_bg)

    left_frame.pack(side="left", fill="both", expand=True)
    right_frame.pack(side="right", fill="both", expand=True)

    # Create a canvas and scrollbar for the left frame to handle many files
    canvas = tk.Canvas(left_frame, bg=dark_bg)
    scrollbar = tk.Scrollbar(left_frame, orient="vertical", command=canvas.yview)
    scrollable_frame = tk.Frame(canvas, bg=dark_bg)

    scrollable_frame.bind(
        "<Configure>",
        lambda e: canvas.configure(
            scrollregion=canvas.bbox("all")
        )
    )

    canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
    canvas.configure(yscrollcommand=scrollbar.set)

    canvas.pack(side="left", fill="both", expand=True)
    scrollbar.pack(side="left", fill="y")
    # Create the CHANGELOG section below the scrollable file list
    changelog_label = tk.Label(left_frame, text="CHANGELOG", bg=dark_bg, fg=TextColor())
    changelog_label.pack(anchor="nw", padx=5, pady=(10, 2))

    # Create the Text widget for the changelog display
    changelog_text = tk.Text(left_frame, wrap="word", bg=dark_bg, fg=TextColor(), height=30, state=tk.DISABLED)
    changelog_text.pack(fill="y", padx=5, pady=(0, 10))

    # Create a listbox to show mod profiles on the right panel
    profile_listbox = tk.Listbox(right_frame, width=50, bg=dark_bg, fg=TextColor())
    profile_listbox.pack(fill="both", expand=True)

    # Load profiles from a .txt file and display them in the listbox
    if os.path.exists(profile_path):
        with open(profile_path, 'r') as profile_file:
            profiles = profile_file.readlines()
            for profile in profiles:
                profile_name = profile.split(":")[0]
                mods_count = profile.count(',') + 1  # Counting mods by the number of commas + 1
                profile_listbox.insert(tk.END, f"{profile_name}, {mods_count} mods")
    else:
        profile_listbox.insert(tk.END, "No profiles available.")
        error_msg("No MML_Profiles.txt found. The file will be created automatically when profiles are saved.")

    # Text entry for adding new profiles
    profile_entry = tk.Entry(
        right_frame,
        bg=JustBackGround(),  # Example color: Dark Slate Gray, you can adjust to any color you prefer
        fg=TextColor(),
        width=40,  # Adjust the width to make the input field longer
    )
    profile_entry.pack(pady=5)

    # Button to save the new profile
    save_profile_btn = tk.Button(right_frame, text="Save Profile", bg=JustBackGround(), fg=TextColor(), activebackground=ButtonPressedBackGround(), activeforeground=PressedTextColor(), command=save_profile)
    save_profile_btn.pack(pady=5)

    # Button to remove the selected profile
    remove_profile_btn = tk.Button(right_frame, text="Remove Profile", bg=JustBackGround(), fg=TextColor(), activebackground=ButtonPressedBackGround(), activeforeground=PressedTextColor(), command=remove_profile)
    remove_profile_btn.pack(pady=5)

    # Button to load the selected profile
    load_profile_btn = tk.Button(right_frame, text="Load Profile", bg=JustBackGround(), fg=TextColor(), activebackground=ButtonPressedBackGround(), activeforeground=PressedTextColor(), command=load_profile)
    load_profile_btn.pack(pady=5)

    # Add AUTHOR display on the right side under the profile buttons
    author_label = tk.Label(right_frame, text="Made by MOD AUTHOR HERE (INFO)", bg=dark_bg, fg=TextColor())
    author_label.pack(anchor="nw", pady=(10, 2))

    # Initialize the display
    update_files()
