#====================================================================================================
# EDF_ModloaderHeadFunc.py

import os, sys, shutil, requests, subprocess, json, webbrowser, zipfile, tkinter as tk, uuid, ConfigManifestUninstaller as uninstaller
from tkinter import messagebox

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
            "EDF 6": 0.0,
            "( 6 ) DLC Lost Days": 0.0,
            "( 6 ) DLC Visions of Malice": 0.0,
            "EDF 5": 0.0,
            "( 5 ) DLC Mission Pack 1": 0.0,
            "( 5 ) DLC Mission Pack 2": 0.0,
            "EDF 4.1": 0.0,
            "(4.1) DLC Mission Pack 1": 0.0,
            "(4.1) DLC Mission Pack 2": 0.0,
            "EDF World Brothers": 0.0,
            "(WB ) Additional Mission Pack: Another ResCUBE": 0.0,
            "EDF World Brothers 2": 0.0,
            "(WB2) Extra Mission Pack: Robo Saurous vs the Mecharmy": 0.0,
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
    use_exe = True #True  # Always use EXE unless specifically toggled
    output_directory = parent_dir
    current_directory = os.path.abspath(os.path.join(parent_dir, "Mods", "EDF 6 MOD SETTINGS MAKER"))

    try:
        if use_exe:
            exe_path = os.path.join(parent_dir, "Mods", "EDF 6 MOD SETTINGS MAKER", exe_name)
            #print(f"EXE Used: {exe_name}")
            result = subprocess.run([exe_path, output_directory, current_directory], capture_output=True, text=True, shell=True)
        else:
            script_path = os.path.join(parent_dir, "Mods", "EDF 6 MOD SETTINGS MAKER", "ConfigBuildAllNoInstaller.py")
            print("Python script used")  # ConfigBuildAll, ConfigBuildAllNoInstaller
            result = subprocess.run(["python", script_path, output_directory, current_directory], capture_output=True, text=True, shell=True)

        # Handle output and errors
        error_msg(result.stdout)
        if result.stderr:
            error_msg("Error: " + result.stderr)
    except Exception as e:
        error_msg(f"Exception occurred: {str(e)}")

# Repair Tables: Copy files from a directory and paste them at the parent directory
def repair_tables(error_msg, current_dir):
    try:
        source_dir = os.path.join(current_dir, "Mods", "EDF 6 MOD SETTINGS MAKER", "DO NOT TOUCH ORIGINAL CONFIG DATA")
        dest_dir = os.path.join(current_dir, "Mods", "EDF 6 MOD SETTINGS MAKER")

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
#Funtions

def open_save_folder(error_msg, game_key=None):
    try:
        # Define potential base paths for EDF 4.1 and EDF 5
        base_paths = [
            os.path.join(os.getenv('USERPROFILE', ''), "OneDrive", "Documents"),
            os.path.join(os.getenv('USERPROFILE', ''), "Documents")
        ]
        
        # Define specific save paths for each game
        game_save_paths = {
            "EARTH DEFENSE FORCE 4.1": ["My Games", "EDF4.1", "SAVE_DATA"],
            "EARTH DEFENSE FORCE 5": ["My Games", "EDF5", "SAVE_DATA"],
            "EARTH DEFENSE FORCE 6": [os.getenv('LOCALAPPDATA', ''), "EarthDefenceForce6", "SAVE_DATA"]
        }
        
        if game_key and game_key in game_save_paths:
            save_folder_path = None
            
            if game_key == "EARTH DEFENSE FORCE 6":
                base_save_path = os.path.join(*game_save_paths[game_key])
            else:
                # Check both potential base paths for EDF 4.1 and EDF 5
                for base_path in base_paths:
                    potential_path = os.path.join(base_path, *game_save_paths[game_key])
                    if os.path.exists(potential_path):
                        base_save_path = potential_path
                        break
            
            if base_save_path and os.path.exists(base_save_path):
                # Look for the first subfolder within the SAVE_DATA directory
                subfolders = [f.path for f in os.scandir(base_save_path) if f.is_dir()]
                if subfolders:
                    save_folder_path = subfolders[0]  # Open the first subfolder found
                else:
                    error_msg(f"No subfolder found in {base_save_path}")
                    return
            
            if save_folder_path and os.path.exists(save_folder_path):
                subprocess.Popen(['explorer', save_folder_path])
            else:
                error_msg(f"Save folder not found. Expected path: {save_folder_path}")
        else:
            error_msg("Invalid game key or game folder structure not recognized.")
    
    except Exception as e:
        error_msg(f"Failed to open save folder: {str(e)}")

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

def update_mods(error_msg):
    mod_info_path = os.path.join(parent_dir, "Mods", "EDF 6 MOD SETTINGS MAKER", "MOD CONFIG DATA PLACED HERE")
    
    try:
        # Load all mod files
        mod_files = [f for f in os.listdir(mod_info_path) if f.endswith(".json")]
        for mod_file in mod_files:
            mod_data = load_mod_data(mod_info_path, mod_file, error_msg)
            if mod_data:
                # Process each mod in the mod data
                for mod in mod_data.get("MOD_INFO", []):
                    download_mod(mod, error_msg)  # No need for additional messages here
                    
        error_msg("Mod update check completed.")  # Keep a general completion message
    except Exception as e:
        error_msg(f"Failed to update mods: {str(e)}")

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

# Track operation status to avoid multiple simultaneous actions
operation_in_progress = False

#====================================================================================================

#TODO
'''
User Interface Enhancements:
Fix Mod Pack data
'''


def toggle_mods_panels(error_msg):
    # Define the directory where Mod_config_data.json files are located
    mod_config_dir = os.path.join(parent_dir, "Mods", "EDF 6 MOD SETTINGS MAKER", "MOD CONFIG DATA PLACED HERE")
    dark_bg = "#000000"  # Set the dark background color
    profile_path = os.path.join(mod_config_dir, 'MML_Profiles.txt')
    scrollbar_color = TextColor()

    def apply_hover_effect(button, hover_bg=ButtonPressedBackGround(), hover_fg=TextColor(), normal_bg=None, normal_fg=None):
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

    # Function to refresh the file list and display current states
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

            enable_btn = tk.Button(button_frame, text="Enable", bg="#333333", fg="#FFFFFF", activebackground="#010e70", activeforeground="#FFFFFF", command=lambda f=file: enable_file(f))
            apply_hover_effect(enable_btn)
            disable_btn = tk.Button(button_frame, text="Disable", bg="#333333", fg="#FFFFFF", activebackground="#010e70", activeforeground="#FFFFFF", command=lambda f=file: disable_file(f))
            apply_hover_effect(disable_btn)
            uninstall_btn = tk.Button(button_frame, text="Uninstall", bg="#333333", fg="#FFFFFF", activebackground="#010e70", activeforeground="#FFFFFF", command=lambda f=file: uninstall_a_mod(f))
            apply_hover_effect(uninstall_btn)
            info_btn = tk.Button(button_frame, text="INFO", bg="#333333", fg="#FFFFFF", activebackground="#010e70", activeforeground="#FFFFFF", command=lambda f=file: info_file(f))
            apply_hover_effect(info_btn)

            enable_btn.pack(side="left", padx=10)
            disable_btn.pack(side="left", padx=10)
            uninstall_btn.pack(side="left", padx=10)
            info_btn.pack(side="left", padx=10)

    def enable_file(file):
        global operation_in_progress
        if operation_in_progress:
            error_msg("Operation already in progress. Please wait.")
            return
        
        file_path = os.path.join(mod_config_dir, file)
        new_path = file_path.replace('.disabled', '.json')
        try:
            operation_in_progress = True
            if not os.path.exists(file_path):
                error_msg(f"File not found: {file_path}")
                operation_in_progress = False
                return

            os.rename(file_path, new_path)
            error_msg(f"Enabled: {file}")
            update_files()
        except Exception as e:
            error_msg(f"Failed to enable {file}: {e}")
        finally:
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
            operation_in_progress = True
            if not os.path.exists(file_path):
                error_msg(f"File not found for disabling: {file_path}")
                operation_in_progress = False
                return

            os.rename(file_path, new_path)
            error_msg(f"Disabled: {file}")
            update_files()
        except Exception as e:
            error_msg(f"Failed to disable {file}: {e}")
        finally:
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

    def save_profile():
        profile_name = profile_entry.get().strip()
        if not profile_name:
            error_msg("Profile name cannot be empty.")
            return

        try:
            # Collect the state of all files to save with the profile
            current_files = [f for f in os.listdir(mod_config_dir) if f.endswith('.json') or f.endswith('.disabled')]
            unique_files = list(set(current_files))  # Ensure uniqueness

            # Generate profile data with correct format
            profile_data = {
                file.replace('.json', '').replace('.disabled', ''): '1' if file.endswith('.json') else '0'
                for file in unique_files
            }
            profile_line = f"{profile_name}: {{{', '.join(f'{k}:{v}' for k, v in profile_data.items())}}}"

            # Read existing profiles
            profiles = []
            if os.path.exists(profile_path):
                with open(profile_path, 'r') as profile_file:
                    profiles = profile_file.readlines()

            # Write the updated profiles while avoiding duplicates
            with open(profile_path, 'w') as profile_file:
                for line in profiles:
                    if not line.startswith(profile_name + ":"):
                        profile_file.write(line)
                profile_file.write(profile_line + '\n')

            # Update the profile listbox with current profiles
            profile_listbox.delete(0, tk.END)
            for line in profiles:
                try:
                    prof_name, mod_data = line.split(":", 1)
                    enabled_count = sum(1 for entry in mod_data.strip("{}\n").split(", ") if ":1" in entry)
                    profile_listbox.insert(tk.END, f"{prof_name.strip()}, {enabled_count} mods")
                except Exception as e:
                    error_msg(f"Failed to parse profile line: {line}, Error: {e}")

            # Add the newly saved profile to the listbox
            enabled_mods_count = len([v for v in profile_data.values() if v == '1'])
            profile_listbox.insert(tk.END, f"{profile_name}, {enabled_mods_count} mods")
            error_msg(f"Profile '{profile_name}' saved.")
            profile_entry.delete(0, tk.END)

        except Exception as e:
            error_msg(f"Failed to save profile: {e}")

    def load_profile():
        try:
            selected_index = profile_listbox.curselection()
            if not selected_index:
                error_msg("No profile selected.")
                return

            selected_profile = profile_listbox.get(selected_index).split(',')[0].strip()
            if not os.path.exists(profile_path):
                error_msg("No profiles file found.")
                return

            with open(profile_path, 'r') as profile_file:
                profiles = profile_file.readlines()

            for line in profiles:
                if line.startswith(f"{selected_profile}:"):
                    mod_data = line.split(":", 1)[1].strip("{}\n")
                    for entry in mod_data.split(", "):
                        if ':' in entry:
                            mod_name, status = entry.split(":")
                            mod_name = mod_name.strip('{} ')
                            status = status.strip()
                            json_file = f"{mod_name}.json"
                            disabled_file = f"{mod_name}.disabled"

                            if status == '1':
                                if os.path.exists(os.path.join(mod_config_dir, disabled_file)):
                                    enable_file(disabled_file)
                                elif os.path.exists(os.path.join(mod_config_dir, json_file)):
                                    error_msg(f"{json_file} is already enabled.")
                            elif status == '0':
                                if os.path.exists(os.path.join(mod_config_dir, json_file)):
                                    disable_file(json_file)
                                elif os.path.exists(os.path.join(mod_config_dir, disabled_file)):
                                    error_msg(f"{disabled_file} is already disabled.")
                            error_msg(f"Processed mod {mod_name} with status {status}")
                    break
            else:
                error_msg(f"Profile '{selected_profile}' not found in the profiles file.")
        except Exception as e:
            error_msg(f"Failed to load profile: {e}")

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

    # Function to display information (CHANGELOG and AUTHOR) from the file in the UI
    def info_file(file):
        file_path = os.path.join(mod_config_dir, file)
        try:
            with open(file_path, 'r', encoding='utf-8') as config_file:
                config_data = json.load(config_file)

            # Extract MOD NAME and CHANGELOG
            mod_name = config_data.get('MOD_INFO', [{}])[0].get('MOD NAME', 'Unknown Mod')
            changelog = config_data.get('CHANGELOG', ['CHANGELOG not found'])

            # Extract AUTHOR
            author = config_data.get('MOD_INFO', [{}])[0].get('AUTHOR', 'AUTHOR not found')

            # Update the changelog title with the mod name
            changelog_label.config(text=f"CHANGELOG For {mod_name}     |")

            # Update the CHANGELOG text widget
            changelog_text.config(state=tk.NORMAL)
            changelog_text.delete(1.0, tk.END)
            changelog_text.insert(tk.END, "\n".join(changelog))
            changelog_text.config(state=tk.DISABLED)

            # Update the AUTHOR label
            author_label.config(text=f"Made by {author}")

        except Exception as e:
            error_msg(f"Failed to read config variables from {file_path}: {e}")

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

    def create_search_and_filter_controls(parent_frame):
        search_frame = tk.Frame(parent_frame, bg="#333333")  # Light gray background for search area
        search_frame.pack(fill='x', pady=10)

        search_label = tk.Label(search_frame, text="Search Mods:", bg="#333333", fg="#FFFFFF")
        search_label.pack(side='left', padx=10)
        search_entry = tk.Entry(search_frame, bg="#333333", fg="#FFFFFF", width=30)
        search_entry.pack(side='left', padx=10)

        category_label = tk.Label(search_frame, text="Filter by Category:", bg="#333333", fg="#FFFFFF")
        category_label.pack(side='left', padx=10)
        category_var = tk.StringVar()
        category_var.set("All")
        category_menu = tk.OptionMenu(search_frame, category_var, *MOD_CATEGORIES)
        category_menu.config(
            bg="#333333",
            fg="#FFFFFF",
            activebackground="#555555",
            activeforeground="#FFFFFF",
            relief="solid",
            highlightthickness=0,
            cursor="hand2"
        )
        category_menu["menu"].config(
            bg="#333333",
            fg="#FFFFFF",
            activebackground="#555555",
            activeforeground="#FFFFFF"
        )
        category_menu.pack(side='left', padx=10)

        filter_btn = tk.Button(search_frame, text="Apply Filter", bg="#333333", fg="#FFFFFF", activebackground="#010e70",   activeforeground="#FFFFFF", command=lambda: update_files(search_entry.get(), category_var.get()))
        apply_hover_effect(filter_btn)
        filter_btn.pack(side='left', padx=10)

        return search_entry, category_var

    MOD_CATEGORIES = ["All", "Weapons", "Enemies", "Graphics", "UI", "Missions", "Gameplay", "Other", "Patch"]

    # Create a new window
    window = tk.Toplevel()
    window.title("Mods Panel")
    window.geometry("1500x400")  # Increased height for better layout

    # Create frames with increased padding and new background color
    left_frame = tk.Frame(window, padx=10, pady=10, bg=dark_bg)
    right_frame = tk.Frame(window, padx=10, pady=10, bg=dark_bg)

    left_frame.pack(side="left", fill="both", expand=True, padx=5)
    right_frame.pack(side="right", fill="both", expand=True, padx=5)

    # Add a vertical divider between frames
    divider = tk.Frame(window, bg="#333333", width=2)  # Light gray divider
    divider.pack(side="left", fill="y", padx=5)

    # Add search and filter controls to the left frame
    search_entry, category_var = create_search_and_filter_controls(left_frame)

    # Create a canvas and scrollbar for the left frame to handle many files
    canvas = tk.Canvas(left_frame, bg=dark_bg)
    scrollbar = tk.Scrollbar(left_frame, troughcolor=scrollbar_color, orient="vertical", command=canvas.yview)
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

    # Create a frame to hold changelog label and author label side by side
    changelog_author_frame = tk.Frame(left_frame, bg=dark_bg)
    changelog_author_frame.pack(anchor="nw", padx=10, pady=(10, 5))

    # Changelog label (left side)
    changelog_label = tk.Label(changelog_author_frame, text="CHANGELOG      |", bg=dark_bg, fg="#FFFFFF")
    changelog_label.pack(side="left", padx=5)

    # Author label (right side, anchored to northeast)
    author_label = tk.Label(changelog_author_frame, text="Made by MOD AUTHOR HERE (INFO)", bg=dark_bg, fg="#FFFFFF")
    author_label.pack(side="right", anchor="ne", padx=5)

    # Create a frame to hold the changelog text and scrollbar
    changelog_frame = tk.Frame(left_frame, bg=dark_bg)
    changelog_frame.pack(fill="both", padx=10, pady=(0, 10))

    # Create the scrollbar
    changelog_scrollbar = tk.Scrollbar(changelog_frame, orient="vertical", troughcolor="#FFFFFF", command=lambda *args: changelog_text.yview(*args))

    # Create the Text widget for the changelog display
    changelog_text = tk.Text(changelog_frame, wrap="word", bg=dark_bg, fg="#FFFFFF", height=15, state=tk.DISABLED)
    changelog_text.config(yscrollcommand=changelog_scrollbar.set)

    # Pack the scrollbar and text widget
    changelog_scrollbar.pack(side="right", fill="y")
    changelog_text.pack(side="left", fill="both", expand=True)

    # Create a frame for the profile buttons at the top
    profile_btn_frame = tk.Frame(right_frame, bg="#333333")
    profile_btn_frame.pack(pady=10, fill="x")

    # Profile buttons (at the top)
    save_profile_btn = tk.Button(profile_btn_frame, text="Save Profile", bg="#333333", fg="#FFFFFF", activebackground="#010e70", activeforeground="#FFFFFF", command=save_profile)
    apply_hover_effect(save_profile_btn)
    save_profile_btn.pack(side="left", padx=10)

    remove_profile_btn = tk.Button(profile_btn_frame, text="Remove Profile", bg="#333333", fg="#FFFFFF", activebackground="#010e70", activeforeground="#FFFFFF", command=remove_profile)
    apply_hover_effect(remove_profile_btn)
    remove_profile_btn.pack(side="left", padx=10)

    load_profile_btn = tk.Button(profile_btn_frame, text="Load Profile", bg="#333333", fg="#FFFFFF", activebackground="#010e70", activeforeground="#FFFFFF", command=load_profile)
    apply_hover_effect(load_profile_btn)
    load_profile_btn.pack(side="left", padx=10)

    # Text entry for adding new profiles (below buttons) with placeholder
    profile_entry = tk.Entry(right_frame, bg="#333333", fg="#FFFFFF", width=40)
    profile_entry.insert(0, "Profile Name?")  # Add placeholder text
    profile_entry.config(fg="#B3B3B3")  # Use a lighter gray for placeholder text to distinguish it from user input

    # Bind events to handle placeholder behavior
    def clear_placeholder(event):
        if profile_entry.get() == "Profile Name?":
            profile_entry.delete(0, tk.END)
            profile_entry.config(fg="#FFFFFF")  # Change text color to white for user input

    def restore_placeholder(event):
        if not profile_entry.get().strip():
            profile_entry.insert(0, "Profile Name?")
            profile_entry.config(fg="#B3B3B3")  # Restore placeholder color

    profile_entry.bind("<FocusIn>", clear_placeholder)
    profile_entry.bind("<FocusOut>", restore_placeholder)

    profile_entry.pack(pady=10, padx=10)

    # Create a listbox to show mod profiles (below entry)
    profile_listbox = tk.Listbox(right_frame, width=40, height=20, bg=dark_bg, fg="#FFFFFF", selectbackground="#4682B4")
    profile_listbox.pack(fill="both", expand=True, padx=10, pady=10)

    # Load profiles from a .txt file and display them in the listbox
    if os.path.exists(profile_path):
        with open(profile_path, 'r') as profile_file:
            profiles = profile_file.readlines()
            for profile in profiles:
                try:
                    profile_name, mod_data = profile.split(":", 1)
                    mod_entries = mod_data.strip().strip("{} ").split(",")
                    available_mods = set(os.listdir(mod_config_dir))
                    enabled_mod_count = 0

                    for entry in mod_entries:
                        entry = entry.strip()
                        if not entry:
                            continue
                        if ":" in entry:
                            parts = entry.split(":", 1)
                            if len(parts) == 2:
                                mod_name, status = parts
                                mod_name = mod_name.strip()
                                status = status.strip()
                                mod_file = f"{mod_name}.json"
                                if status == "1" and mod_file in available_mods:
                                    enabled_mod_count += 1
                                    enable_file(mod_file)
                                elif status == "0" and mod_file in available_mods:
                                    disable_file(mod_file)
                            else:
                                error_msg(f"Malformed entry with incorrect parts: {entry}")
                        else:
                            error_msg(f"Skipping malformed entry: {entry}")

                    profile_listbox.insert(tk.END, f"{profile_name.strip()}, {enabled_mod_count} mods")
                    error_msg(f"{profile_name.strip()}, {enabled_mod_count} mods")
                except Exception as e:
                    error_msg(f"Failed to parse profile line '{profile}': {e}")
    else:
        profile_listbox.insert(tk.END, "No profiles available.")
        error_msg("No MML_Profiles.txt found. The file will be created automatically when profiles are saved.")

    #
    # Initialize the display
    update_files()

#====================================================================================================