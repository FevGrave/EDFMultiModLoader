import os
import shutil
import json
import glob
# List of folders that should never be removed
protected_folders = [
    "ADDONSTEAM", "BAT", "DEBUG", "DEFAULTPACKAGE", "DisabledPatches", "EDF 6 MOD SETTINGS MAKER", 
    "EFFECT", "ETC", "HUD", "MAP", "MENUOBJECT", "MISSION", "NETWORK", "OBJECT", 
    "Patches", "PC", "Plugins", "SHADER", "SOUND", "TOOLS", "UI", "WEAPON"
]

def remove_files_and_folders(manifest, base_path):
    for key, value in manifest.items():
        full_path = os.path.normpath(os.path.join(base_path, key))
        if isinstance(value, dict):
            # Handle folders
            if 'Folders' in value:
                for folder in value['Folders']:
                    folder_path = os.path.normpath(os.path.join(full_path, folder))
                    # Skip protected folders
                    if folder in protected_folders:
                        continue
                    # Attempt to remove non-protected folders
                    if os.path.isdir(folder_path):
                        try:
                            shutil.rmtree(folder_path)
                            print(f"Folder removed: {folder_path}")
                        except Exception as e:
                            print(f"Failed to remove folder: {folder_path}. Error: {e}")
                    else:
                        print(f"Folder does not exist: {folder_path}")

            # Handle files
            if 'Files' in value:
                for file in value['Files']:
                    file_path = os.path.normpath(os.path.join(full_path, file))
                    if os.path.isfile(file_path):
                        try:
                            os.remove(file_path)
                            print(f"File removed: {file_path}")
                        except Exception as e:
                            print(f"Failed to remove file: {file_path}. Error: {e}")
                    else:
                        print(f"File does not exist: {file_path}")

            # Recursively handle subfolders or sub-items
            for sub_key, sub_value in value.items():
                if sub_key not in ['Folders', 'Files']:
                    sub_full_path = os.path.normpath(os.path.join(full_path, sub_key))
                    remove_files_and_folders({sub_key: sub_value}, sub_full_path)

        elif isinstance(value, list):
            for item in value:
                item_path = os.path.normpath(os.path.join(full_path, item))
                if os.path.isfile(item_path):
                    try:
                        os.remove(item_path)
                        print(f"File removed: {item_path}")
                    except Exception as e:
                        print(f"Failed to remove file: {item_path}. Error: {e}")
                elif os.path.isdir(item_path):
                    try:
                        shutil.rmtree(item_path)
                        print(f"Folder removed: {item_path}")
                    except Exception as e:
                        print(f"Failed to remove folder: {item_path}. Error: {e}")
                else:
                    print(f"Path does not exist: {item_path}")

def load_manifest_and_uninstall(manifest_file, base_path):
    try:
        with open(manifest_file, 'r', encoding='utf-8') as file:
            manifest_data = json.load(file)
            if 'DirManifestToFilesUninstaller' in manifest_data:
                # Use the provided base path instead of deriving from manifest_file
                remove_files_and_folders(manifest_data['DirManifestToFilesUninstaller'], base_path)
            else:
                print("Manifest file does not contain 'DirManifestToFilesUninstaller'.")
    except json.JSONDecodeError as e:
        print(f"Error decoding JSON from manifest file: {e}")
    except Exception as e:
        print(f"An error occurred while loading the manifest: {e}")

if __name__ == "__main__":
    current_dir = os.path.dirname(os.path.abspath(__file__))
    manifest_dir = os.path.normpath(os.path.abspath(os.path.join(current_dir, "..", "..")))
    manifest_pattern = os.path.normpath(os.path.join(manifest_dir, "Mods", "EDF 6 MOD SETTINGS MAKER", "MOD CONFIG DATA PLACED HERE", "*Mod_config_data.json"))
    print(f"Looking for manifest files with the pattern: {manifest_pattern}")
    manifest_files = glob.glob(manifest_pattern)

    if manifest_files:
        manifest_file = manifest_files[0]
        print(f"Found manifest file: {manifest_file}")
        load_manifest_and_uninstall(manifest_file)
    else:
        print("No manifest file found matching the pattern.")
