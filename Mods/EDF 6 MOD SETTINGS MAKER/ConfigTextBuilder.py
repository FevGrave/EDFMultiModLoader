import os, json, sys

def check_arguments():
    if len(sys.argv) < 3:
        print("Usage: python script.py <output_directory>")
        sys.exit(1)
    return sys.argv[1], sys.argv[2]

def load_json_file(file_path):
    """Utility function to load a JSON file with UTF-8 encoding."""
    if not os.path.exists(file_path):
        print(f"Error: {file_path} not found.")
        return {}
    try:
        with open(file_path, "r", encoding='utf-8') as file:
            data = json.load(file)
            return data
    except json.JSONDecodeError:
        print(f"Error: Failed to decode JSON from {file_path}.")
        return {}

def save_json_file(file_path, data):
    """Utility function to save a JSON file with UTF-8 encoding."""
    try:
        with open(file_path, "w", encoding='utf-8') as file:
            json.dump(data, file, ensure_ascii=False, indent=4)
    except Exception as e:
        print(f"Error: Failed to save JSON to {file_path}. Reason: {e}")

def append_entries_to_variables(data, new_entries):
    """Appends new text table entries to the 'variables' list in the JSON data."""
    if 'variables' not in data or not isinstance(data['variables'], list):
        print(f"Warning: 'variables' not found or not a list. Initializing with an empty list.")
        data['variables'] = []

    # Append new entries to 'variables', checking for duplicates by name
    existing_names = {entry['name'] for entry in data['variables']}
    
    added_entries = 0
    for entry in new_entries:
        if isinstance(entry, dict) and 'name' in entry and 'type' in entry and 'value' in entry:
            if entry['name'] not in existing_names:
                data['variables'].append(entry)
                added_entries += 1
            else:
                print(f"Warning: Entry with name '{entry['name']}' already exists. Skipping.")
        else:
            print(f"Warning: Malformed entry skipped: {entry}")

    # Sort alphabetically by 'name'
    data['variables'].sort(key=lambda entry: entry.get('name', ''))

# Paths and directory setup
current_directory = sys.argv[2]

mod_config_directory = os.path.join(current_directory, 'MOD CONFIG DATA PLACED HERE')
if not os.path.exists(mod_config_directory):
    print(f"Error: Mod config directory '{mod_config_directory}' does not exist.")
    sys.exit(1)

# Language codes and corresponding import file names
language_files = {
    "CN": "ImportTextTable-CN.json",
    "EN": "ImportTextTable-EN.json",
    "JA": "ImportTextTable-JA.json",
    "KR": "ImportTextTable-KR.json",
    "SC": "ImportTextTable-SC.json"
}

# Load the language-specific files only once
output_directory = sys.argv[1]

# Dictionary to hold language files data in memory
language_data = {}

def main(output_directory, current_directory):
    # Set up paths for the mod config directory and language-specific files
    mod_config_directory = os.path.join(current_directory, 'MOD CONFIG DATA PLACED HERE')
    if not os.path.exists(mod_config_directory):
        print(f"Error: Mod config directory '{mod_config_directory}' does not exist.")
        sys.exit(1)

    # Define language files and initialize language data storage
    language_files = {
        "CN": "ImportTextTable-CN.json",
        "EN": "ImportTextTable-EN.json",
        "JA": "ImportTextTable-JA.json",
        "KR": "ImportTextTable-KR.json",
        "SC": "ImportTextTable-SC.json"
    }
    language_data = {}

    # Load all language files once
    for lang_code, file_name in language_files.items():
        import_file_path = os.path.join(current_directory, file_name)
        language_data[lang_code] = load_json_file(import_file_path)

    # Process each Mod_config_data.json file in the mod config directory
    for filename in os.listdir(mod_config_directory):
        if filename.endswith('Mod_config_data.json'):
            mod_config_file_path = os.path.join(mod_config_directory, filename)
            mod_config = load_json_file(mod_config_file_path)

            # Get NewToAddTextTableEntries and append entries for each language
            new_entries_by_language = mod_config.get('NewToAddTextTableEntries')
            if not isinstance(new_entries_by_language, dict):
                print(f"Error: 'NewToAddTextTableEntries' not found or is not a dictionary in {mod_config_file_path}")
                continue

            for lang_code, new_entries in new_entries_by_language.items():
                if lang_code in language_data:
                    append_entries_to_variables(language_data[lang_code], new_entries)
                else:
                    print(f"Warning: No language file loaded for {lang_code}")

    # Save the final results for each language file
    for lang_code, data in language_data.items():
        output_file_path = os.path.join(output_directory, f"TEXTTABLE_STEAM.{lang_code}.TXT.json")
        save_json_file(output_file_path, data)
        print(f"Saved updated language file: {output_file_path}")

# Allow the script to be called directly or from another script
if __name__ == "__main__":
    output_directory, current_directory = check_arguments()
    main(output_directory, current_directory)