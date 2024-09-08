import os
import json
# pyinstaller --onefile .\ManifestMAKER.py


def scan_directory(directory_path):
    print("Building Folders Files Directory Tree from current host folder...")
    manifest = {"DirManifestToFilesUninstaller": {}}

    for root, dirs, files in os.walk(directory_path):
        # Remove the base directory path to get the relative path
        relative_path = os.path.relpath(root, directory_path)
        if relative_path == ".":
            relative_path = ""

        if dirs:
            # If there are directories, make sure the key is a dictionary with a 'Folders' entry
            manifest["DirManifestToFilesUninstaller"].setdefault(relative_path, {"Folders": dirs})
        
        if files:
            # If there are files, ensure we append them to the correct key
            if relative_path in manifest["DirManifestToFilesUninstaller"]:
                if isinstance(manifest["DirManifestToFilesUninstaller"][relative_path], dict):
                    manifest["DirManifestToFilesUninstaller"][relative_path].update({"Files": files})
                else:
                    manifest["DirManifestToFilesUninstaller"][relative_path].extend(files)
            else:
                manifest["DirManifestToFilesUninstaller"][relative_path] = files

    return manifest

def update_existing_manifest(new_manifest):
    # Define the path to the existing manifest file to be updated
    current_dir = os.getcwd()
    existing_manifest_path = os.path.join(current_dir, "EDF 6 MOD SETTINGS MAKER", "MOD CONFIG DATA PLACED HERE")
    
    # Locate the *Mod_config_data.json file
    for filename in os.listdir(existing_manifest_path):
        if filename.endswith("Mod_config_data.json"):
            manifest_file_path = os.path.join(existing_manifest_path, filename)
            break
    else:
        print("No suitable *Mod_config_data.json file found in the specified directory.")
        return

    print(f"Updating the manifest file: {manifest_file_path}")

    # Load the existing manifest
    with open(manifest_file_path, 'r', encoding='utf-8') as file:
        existing_manifest = json.load(file)

    # Replace the DirManifestToFilesUninstaller section
    existing_manifest["DirManifestToFilesUninstaller"] = new_manifest["DirManifestToFilesUninstaller"]

    # Save the updated manifest back to the file
    with open(manifest_file_path, 'w', encoding='utf-8') as file:
        json.dump(existing_manifest, file, ensure_ascii=False, indent=2)
    
    print(f"Manifest updated successfully at: {manifest_file_path}")
    print("PLEASE REVIEW THE `DirManifestToFilesUninstaller` within the *Mod_config_data.json")

def save_manifest(manifest, output_file):
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(manifest, f, ensure_ascii=False, indent=2)
    print(f"Manifest file created: {output_file}")

def pause():
    input("\nPress Enter to exit...")

if __name__ == "__main__":
    directory_to_scan = os.getcwd()  # Use the current directory
    output_file = "manifest.json"
    
    # Scan the directory and save the manifest
    manifest_data = scan_directory(directory_to_scan)

    # Update the existing manifest with the new data
    update_existing_manifest(manifest_data)

    save_manifest(manifest_data, output_file)

    # Pause the execution before exit
    pause()