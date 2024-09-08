import os
import json
import sys

def check_arguments():
    if len(sys.argv) < 2:
        print("Usage: python script.py <output_directory>")
        sys.exit(1)
    return sys.argv[1]

def load_json_file(file_path):
    """Utility function to load a JSON file with UTF-8 encoding."""
    if not os.path.exists(file_path):
        return {}
    with open(file_path, "r", encoding='utf-8') as file:
        try:
            data = json.load(file)
            return data
        except json.JSONDecodeError:
            print(f"Error: Failed to decode JSON from {file_path}.")
            return {}

def save_json_file(file_path, data):
    """Utility function to save a JSON file with UTF-8 encoding."""
    with open(file_path, "w", encoding='utf-8') as file:
        json.dump(data, file, ensure_ascii=False, indent=4)

def append_entries_to_variables(data, new_entries):
    """Appends new text table entries to the 'variables' list in the JSON data."""
    if 'variables' not in data or not isinstance(data['variables'], list):
        print(f"Warning: 'variables' not found or not a list. Initializing with an empty list.")
        data['variables'] = []
    data['variables'].extend(new_entries)
    # Sort safely, defaulting to an empty string if 'name' is missing
    data['variables'].sort(key=lambda entry: entry.get('name', ''))

# Paths and directory setup
current_directory = os.path.dirname(os.path.abspath(__file__))
mod_config_directory = os.path.join(current_directory, 'MOD CONFIG DATA PLACED HERE')

# Language codes and corresponding import file names
language_files = {
    "CN": "ImportTextTable-CN.json",
    "EN": "ImportTextTable-EN.json",
    "JA": "ImportTextTable-JA.json",
    "KR": "ImportTextTable-KR.json",
    "SC": "ImportTextTable-SC.json"
}

# Process each Mod_config_data.json file in the directory
for filename in os.listdir(mod_config_directory):
    if filename.endswith('Mod_config_data.json'):
        mod_config_file_path = os.path.join(mod_config_directory, filename)
        mod_config = load_json_file(mod_config_file_path)

        # Access the NewToAddTextTableEntries directly
        new_entries_by_language = mod_config.get('NewToAddTextTableEntries')
        if new_entries_by_language is None or not isinstance(new_entries_by_language, dict):
            print(f"Error: 'NewToAddTextTableEntries' not found or is not a dictionary in {mod_config_file_path}")
            continue

        # Save the updated data to the corresponding files for each language code
        output_directory = check_arguments()
        for lang_code, new_entries in new_entries_by_language.items():
            # Load the corresponding import file as the starting point
            import_file_path = os.path.join(current_directory, language_files[lang_code])
            data = load_json_file(import_file_path)

            # Append the new entries to the 'variables' list
            append_entries_to_variables(data, new_entries)

            # Save the final data back to the output directory
            output_file_path = os.path.join(output_directory, f"TEXTTABLE_STEAM.{lang_code}.TXT.json")
            save_json_file(output_file_path, data)
            print(f"Updating Text Table for {lang_code} from {filename} . DONE")
