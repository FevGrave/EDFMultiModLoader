import os, json, sys, io

# Set stdout and stderr to use UTF-8 encoding
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8')

def check_arguments():
    if len(sys.argv) < 3:
        print("Usage: python script.py <output_directory>")
        sys.exit(1)
    #print(f"[DEBUG] Output directory: {sys.argv[1]}")
    return sys.argv[1], sys.argv[2]

def load_json_file(file_path):
    """Utility function to load a JSON file with UTF-8 encoding."""
    if not os.path.exists(file_path):
        print(f"Error: {file_path} not found.")
        return {}
    try:
        with open(file_path, "r", encoding='utf-8') as file:
            data = json.load(file)
            #print(f"[DEBUG] Successfully loaded JSON from {file_path}")
            return data
    except json.JSONDecodeError:
        print(f"Error: Failed to decode JSON from {file_path}.")
        return {}

def save_json_file(file_path, data):
    """Utility function to save a JSON file with UTF-8 encoding."""
    try:
        with open(file_path, "w", encoding='utf-8') as file:
            json.dump(data, file, ensure_ascii=False, indent=4)
        #print(f"[DEBUG] Successfully saved JSON to {file_path}")
    except Exception as e:
        print(f"Error: Failed to save JSON to {file_path}. Reason: {e}")

def append_entries_to_table(data, new_entries):
    """Appends new entries to the 'value' list inside the 'variables'."""
    if "variables" not in data or not isinstance(data["variables"], list):
        print(f"Error: 'variables' not found or is not a list in the file.")
        return
    
    if len(data["variables"]) == 0 or "value" not in data["variables"][0]:
        print(f"Error: No 'value' list found in 'variables'.")
        return
    
    value_list = data["variables"][0]["value"]
    if not isinstance(value_list, list):
        print(f"Error: 'value' is not a list. Cannot append entries.")
        return
    
    added_entries = 0
    for entry in new_entries:
        if isinstance(entry, dict):
            value_list.append(entry)
            added_entries += 1
            #print(f"[DEBUG] Appending new entry: {entry}")
        else:
            print(f"Warning: Malformed entry skipped: {entry}")

    #print(f"[DEBUG] Added {added_entries} new entries. Total count after appending: {len(value_list)}")

# Paths and directory setup
current_directory = sys.argv[2]
#print(f"[DEBUG] Current directory: {current_directory}")

mod_config_directory = os.path.join(current_directory, 'MOD CONFIG DATA PLACED HERE')
if not os.path.exists(mod_config_directory):
    print(f"Error: Mod config directory '{mod_config_directory}' does not exist.")
    sys.exit(1)

#print(f"[DEBUG] Mod config directory: {mod_config_directory}")

# Language codes and corresponding import file names
language_files = {
    "CN": "ImportSubtitleVoiceTable.CN.json",
    "EN": "ImportSubtitleVoiceTable.EN.json",
    "JA": "ImportSubtitleVoiceTable.JA.json",
    "KR": "ImportSubtitleVoiceTable.KR.json",
    "SC": "ImportSubtitleVoiceTable.SC.json"
}
mod_list_key = "NewToAddSubTitleList"

# Check output directory
output_directory = sys.argv[1]

# Dictionary to hold language data in memory
language_data = {}

# Step 1: Load all language files into memory once
for lang_code, voice_file_name in language_files.items():
    voice_file_path = os.path.join(current_directory, voice_file_name)
    language_data[lang_code] = load_json_file(voice_file_path)

def main(output_directory, current_directory):
    # Define paths and verify mod config directory
    mod_config_directory = os.path.join(current_directory, 'MOD CONFIG DATA PLACED HERE')
    if not os.path.exists(mod_config_directory):
        print(f"Error: Mod config directory '{mod_config_directory}' does not exist.")
        sys.exit(1)

    # Define language files and load data into memory
    language_files = {
        "CN": "ImportSubtitleVoiceTable.CN.json",
        "EN": "ImportSubtitleVoiceTable.EN.json",
        "JA": "ImportSubtitleVoiceTable.JA.json",
        "KR": "ImportSubtitleVoiceTable.KR.json",
        "SC": "ImportSubtitleVoiceTable.SC.json"
    }
    mod_list_key = "NewToAddSubTitleList"
    language_data = {lang_code: load_json_file(os.path.join(current_directory, file_name)) for lang_code, file_name in language_files.items()}

    # Process each Mod_config_data.json file in the mod config directory
    for filename in os.listdir(mod_config_directory):
        if filename.endswith('Mod_config_data.json'):
            mod_config_file_path = os.path.join(mod_config_directory, filename)
            mod_config = load_json_file(mod_config_file_path)

            # Skip files without the NewToAddSubTitleList key
            if mod_list_key not in mod_config:
                continue

            # Process entries for each language
            for lang_code, data in language_data.items():
                new_entries = mod_config.get(mod_list_key, {}).get(lang_code)
                if new_entries is None:
                    continue
                elif not isinstance(new_entries, list):
                    print(f"Error: '{mod_list_key}' for {lang_code} in {mod_config_file_path} is not a list. Skipping this language.")
                    continue

                append_entries_to_table(data, new_entries)

    # Save modified language files
    for lang_code, data in language_data.items():
        output_file_path = os.path.join(output_directory, f"EDF6_VOICETABLE.{lang_code}.json")
        save_json_file(output_file_path, data)
        print(f"Saved updated subtitle file: {output_file_path}")

# Allow the script to be called directly or from another script
if __name__ == "__main__":
    output_directory, current_directory = check_arguments()
    main(output_directory, current_directory)