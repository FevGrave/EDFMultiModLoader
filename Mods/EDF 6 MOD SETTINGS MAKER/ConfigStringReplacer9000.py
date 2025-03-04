import os
import sys
import glob
import json

def check_arguments():
    if len(sys.argv) < 3:
        print("Usage: python script.py <output_directory> <current_directory>")
        sys.exit(1)
    return sys.argv[1], sys.argv[2]

def match_value(value, find_value):
    if isinstance(find_value, dict):
        return all(find_value.get(k) == value.get(k) for k in ["type", "value"])
    return value == find_value

def process_import_subtitle_voice_table(filepath, find_value, replace_value):
    count = 0
    try:
        with open(filepath, 'r+', encoding='utf-8') as file:
            data = json.load(file)
            if "variables" in data and isinstance(data["variables"], list):
                for variable in data["variables"]:
                    if isinstance(variable.get("value"), list):
                        for entry in variable["value"]:
                            if isinstance(entry.get("value"), list):
                                for text_entry in entry["value"]:
                                    if (
                                        text_entry.get("name") == find_value.get("name") and
                                        text_entry.get("type") == find_value.get("type") and
                                        text_entry.get("value") == find_value.get("value")
                                    ):
                                        text_entry["value"] = replace_value["value"]
                                        count += 1
            file.seek(0)
            json.dump(data, file, ensure_ascii=False, indent=4)
            file.truncate()
        print(f"{count} replacement(s) applied in {os.path.basename(filepath)}.")
    except Exception as e:
        print(f"Error processing {filepath} with ISVT method: {e}")

def process_import_text_table(filepath, find_value, replace_value):
    count = 0
    try:
        with open(filepath, 'r+', encoding='utf-8') as file:
            data = json.load(file)
            count = replace_nested_value(data, find_value, replace_value)
            file.seek(0)
            json.dump(data, file, ensure_ascii=False, indent=4)
            file.truncate()
        print(f"{count} replacement(s) applied in {os.path.basename(filepath)}.")
    except Exception as e:
        print(f"Error processing {filepath} with ITT method: {e}")

def replace_nested_value(obj, find_value, replace_value):
    count = 0
    if isinstance(obj, dict):
        for key, value in obj.items():
            if isinstance(value, dict) and match_value(value, find_value):
                obj[key] = replace_value
                count += 1
                print(f"Replaced in dict at key: {key}")
            elif value == find_value:
                obj[key] = replace_value
                count += 1
                print(f"Replaced exact match at key: {key}")
            elif isinstance(value, (dict, list)):
                count += replace_nested_value(value, find_value, replace_value)
    elif isinstance(obj, list):
        for i, item in enumerate(obj):
            if isinstance(item, dict) and match_value(item, find_value):
                obj[i] = replace_value
                count += 1
                print(f"Replaced in list at index: {i}")
            elif item == find_value:
                obj[i] = replace_value
                count += 1
                print(f"Replaced exact match in list at index: {i}")
            elif isinstance(item, (dict, list)):
                count += replace_nested_value(item, find_value, replace_value)
    return count

def process_import_weapon_text_table(filepath, find_value, replace_value):
    count = 0
    try:
        with open(filepath, 'r+', encoding='utf-8') as file:
            data = json.load(file)
            if "variables" in data and isinstance(data["variables"], list):
                for variable in data["variables"]:
                    if variable.get("name") == "text_table" and isinstance(variable.get("value"), list):
                        count = replace_nested_value(variable["value"], find_value, replace_value)
            file.seek(0)
            json.dump(data, file, ensure_ascii=False, indent=4)
            file.truncate()
        print(f"{count} replacement(s) applied in {os.path.basename(filepath)}.")
    except Exception as e:
        print(f"Error processing {filepath} with IWTT method: {e}")

def process_import_default_data(filepath, find_value, replace_value):
    count = 0

    def recursive_replace(obj):
        nonlocal count
        if isinstance(obj, dict):
            for key, value in obj.items():
                if match_value(value, find_value):
                    obj[key] = replace_value
                    count += 1
                elif isinstance(value, (dict, list)):
                    recursive_replace(value)
        elif isinstance(obj, list):
            for i, item in enumerate(obj):
                if match_value(item, find_value):
                    obj[i] = replace_value
                    count += 1
                elif isinstance(item, (dict, list)):
                    recursive_replace(item)

    try:
        with open(filepath, 'r+', encoding='utf-8') as file:
            data = json.load(file)
            recursive_replace(data)
            file.seek(0)
            json.dump(data, file, ensure_ascii=False, indent=4)
            file.truncate()
        print(f"{count} replacement(s) applied in {os.path.basename(filepath)}.")
    except Exception as e:
        print(f"Error processing {filepath} with CONFIG method: {e}")

def process_player_object_file(filepath, find_value, replace_value):
    count = 0
    try:
        with open(filepath, 'r+', encoding='utf-8') as file:
            data = json.load(file)

            # Traverse and replace values within "variables"
            for variable in data.get("variables", []):
                if "name" in variable and "value" in variable:
                    if variable["name"] == find_value.get("name"):
                        # Handle the replacement of the full structure if it matches
                        if match_value(variable, find_value):
                            variable["value"] = replace_value["value"]
                            count += 1
                        elif isinstance(variable["value"], list):
                            # Handle nested replacements within the list
                            count += replace_nested_value(variable["value"], find_value, replace_value)

            file.seek(0)
            json.dump(data, file, ensure_ascii=False, indent=4)
            file.truncate()
        
        print(f"{count} replacement(s) applied in {os.path.basename(filepath)}.")
    except Exception as e:
        print(f"Error processing {filepath} with player object method: {e}")

def process_file(filepath, find_value, replace_value):
    file_methods = {
        'ImportDefaultData.json': process_import_default_data,
        'ImportSubtitleVoiceTable.CN.json': process_import_subtitle_voice_table,
        'ImportSubtitleVoiceTable.EN.json': process_import_subtitle_voice_table,
        'ImportSubtitleVoiceTable.JA.json': process_import_subtitle_voice_table,
        'ImportSubtitleVoiceTable.KR.json': process_import_subtitle_voice_table,
        'ImportSubtitleVoiceTable.SC.json': process_import_subtitle_voice_table,
        'ImportTextTable-CN.json': process_import_text_table,
        'ImportTextTable-EN.json': process_import_text_table,
        'ImportTextTable-JA.json': process_import_text_table,
        'ImportTextTable-KR.json': process_import_text_table,
        'ImportTextTable-SC.json': process_import_text_table,
        'ImportWeaponTable.json': process_import_weapon_text_table,
        'ImportWeaponTextTable-CN.json': process_import_weapon_text_table,
        'ImportWeaponTextTable-EN.json': process_import_weapon_text_table,
        'ImportWeaponTextTable-JA.json': process_import_weapon_text_table,
        'ImportWeaponTextTable-KR.json': process_import_weapon_text_table,
        'P501_PROTO_RANGER.json': process_player_object_file,
        'P502_PROTO_WINGDIVER.json': process_player_object_file,
        'P503_PROTO_FENCER.json': process_player_object_file,
        'P504_PROTO_AIRRADER.json': process_player_object_file,
        'P505_RANGER.json': process_player_object_file,
        'P506_WINGDIVER.json': process_player_object_file,
        'P507_FENCER.json': process_player_object_file,
        'P508_AIRRADER.json': process_player_object_file,
        'P601_PROTO_RANGER.json': process_player_object_file,
        'P602_PROTO_WINGDIVER.json': process_player_object_file,
        'P603_PROTO_FENCER.json': process_player_object_file,
        'P604_PROTO_AIRRADER.json': process_player_object_file,
        'P605_RANGER.json': process_player_object_file,
        'P606_WINGDIVER.json': process_player_object_file,
        'P607_FENCER.json': process_player_object_file,
        'P608_AIRRADER.json': process_player_object_file
    }
    filename = os.path.basename(filepath)
    if filename in file_methods:
        print(f"Processing file: {filename}")
        file_methods[filename](filepath, find_value, replace_value)
    else:
        print(f"No custom logic defined for {filename}")

def main(output_directory, current_directory):
    directory_path = os.path.join(current_directory, 'MOD CONFIG DATA PLACED HERE')
    file_pattern = '*Mod_config_data.json'
    config_files = glob.glob(os.path.join(directory_path, file_pattern))

    patch_summary = {}

    if config_files:
        for file_path in config_files:
            try:
                with open(file_path, 'r', encoding='utf-8') as file:
                    data = json.load(file)
                print(f"Loaded config file: {os.path.basename(file_path)}")

                for replacement_block in data.get('DataReplacementTable', []):
                    file_to_modify = replacement_block.get('File')
                    find_string = replacement_block.get('Find')
                    replace_string = replacement_block.get('Replace')

                    if file_to_modify and find_string and replace_string:
                        file_to_modify_path = os.path.join(current_directory, file_to_modify)
                        if os.path.exists(file_to_modify_path):
                            print(f"Applying replacement in {file_to_modify}")
                            process_file(file_to_modify_path, find_string, replace_string)
                            patch_summary[file_to_modify] = patch_summary.get(file_to_modify, 0) + 1
                        else:
                            print(f"File to modify not found: {file_to_modify}")
            except Exception as e:
                print(f"Error reading config file {file_path}: {e}")

        print("\nSummary of replacements:")
        for file, count in patch_summary.items():
            print(f"{count} replacement(s) applied to {file}")
    else:
        print("No mod config data files found.")

if __name__ == "__main__":
    output_directory, current_directory = check_arguments()
    main(output_directory, current_directory)
