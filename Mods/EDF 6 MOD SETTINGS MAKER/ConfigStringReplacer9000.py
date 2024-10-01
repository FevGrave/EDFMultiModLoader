#ConfigStringReplacer9000.py
import os, glob, json, logging

# Set up logging with detailed information
logging.basicConfig(level=logging.INFO, format='%(message)s')

def match_value(value, find_value):
    # Checks if value matches find_value, including type-specific checks
    if isinstance(find_value, dict):
        if "type" in find_value and "value" in find_value:
            if find_value["type"] == value.get("type") and find_value["value"] == value.get("value"):
                return True
    return value == find_value

def process_import_text_table(filepath, find_value, replace_value):
    """
    Custom logic for ImportTextTable-* files.
    Recursively searches for and replaces values in a nested JSON structure.
    """
    count = 0
    try:
        with open(filepath, 'r+', encoding='utf-8') as file:
            data = json.load(file)
            count = replace_nested_value(data, find_value, replace_value)
            file.seek(0)
            json.dump(data, file, ensure_ascii=False, indent=4)
            file.truncate()
        logging.info(f"{count} replacement(s) applied in {os.path.basename(filepath)}.")
    except Exception as e:
        logging.error(f"Error processing {filepath} with ITT method: {e}")

def replace_nested_value(obj, find_value, replace_value):
    """
    Recursively search for and replace values in a nested JSON structure.
    Supports replacing nested objects, not just simple values.
    """
    count = 0
    if isinstance(obj, dict):
        for key, value in obj.items():
            if isinstance(value, dict) and isinstance(find_value, dict):
                if all(item in value.items() for item in find_value.items()):
                    obj[key] = replace_value
                    count += 1
            elif value == find_value:
                obj[key] = replace_value
                count += 1
            elif isinstance(value, (dict, list)):
                count += replace_nested_value(value, find_value, replace_value)
    elif isinstance(obj, list):
        for i, item in enumerate(obj):
            if isinstance(item, dict) and isinstance(find_value, dict):
                if all(sub_item in item.items() for sub_item in find_value.items()):
                    obj[i] = replace_value
                    count += 1
            elif item == find_value:
                obj[i] = replace_value
                count += 1
            elif isinstance(item, (dict, list)):
                count += replace_nested_value(item, find_value, replace_value)
    return count

def process_import_weapon_text_table(filepath, find_value, replace_value):
    """
    Custom logic for ImportWeaponTextTable-* files.
    Searches and replaces matching index values within the 'value' array in the 'variables' section.
    """
    count = 0
    try:
        with open(filepath, 'r+', encoding='utf-8') as file:
            data = json.load(file)
            # Locate the 'value' array inside the 'variables' section
            if "variables" in data and isinstance(data["variables"], list):
                for variable in data["variables"]:
                    if variable.get("name") == "text_table" and isinstance(variable.get("value"), list):
                        # Perform the replacement inside the 'value' array
                        count = replace_nested_value(variable["value"], find_value, replace_value)
            file.seek(0)
            json.dump(data, file, ensure_ascii=False, indent=4)
            file.truncate()
        logging.info(f"{count} replacement(s) applied in {os.path.basename(filepath)}.")
    except Exception as e:
        logging.error(f"Error processing {filepath} with IWTT method: {e}")

def process_import_default_data(filepath, find_value, replace_value):
    """
    Custom logic for ImportDefaultData.json.
    Recursively searches through deeply nested structures and replaces matching values.
    """
    count = 0

    def recursive_replace(obj):
        nonlocal count
        # Recursively replace values in the nested JSON structure
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
        logging.info(f"{count} replacement(s) applied in {os.path.basename(filepath)}.")
    except Exception as e:
        logging.error(f"Error processing {filepath} with CONFIG method: {e}")

# Dispatcher function to call the correct method based on the file type
def process_file(filepath, find_value, replace_value):
    file_methods = {
        'ImportDefaultData.json': process_import_default_data,
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
    }

    # Extract the file name from the path
    filename = os.path.basename(filepath)
    
    # Call the corresponding method based on the file type
    if filename in file_methods:
        file_methods[filename](filepath, find_value, replace_value)
    else:
        logging.warning(f"No custom logic defined for {filename}")
    
    # Call the corresponding method based on the file type
    if filename in file_methods:
        if filename.startswith("ImportTextTable"):
            file_methods[filename](filepath, find_value, replace_value)
        elif filename.startswith("ImportWeaponTextTable"):
            file_methods[filename](filepath, find_value, replace_value)
        else:
            file_methods[filename](filepath)
    else:
        logging.warning(f"No custom logic defined for {filename}")

# Set the working directory to the script's directory
os.chdir(os.path.dirname(os.path.abspath(__file__)))
directory_path = os.path.join('MOD CONFIG DATA PLACED HERE')
file_pattern = '*Mod_config_data.json'
config_files = glob.glob(os.path.join(directory_path, file_pattern))

# Initialize patch_summary before it is used
patch_summary = {}

if config_files:
    for file_path in config_files:
        try:
            with open(file_path, 'r', encoding='utf-8') as file:
                data = json.load(file)
            logging.info(f"{os.path.basename(file_path)} loaded successfully.")
            for replacement_block in data.get('DataReplacementTable', []):
                file_to_modify = replacement_block.get('File')
                find_string = replacement_block.get('Find')
                replace_string = replacement_block.get('Replace')
                if file_to_modify and find_string is not None and replace_string is not None:
                    file_to_modify_path = os.path.join(file_to_modify)
                    if os.path.exists(file_to_modify_path):
                        try:
                            # Use the custom logic dispatcher to process each file type
                            process_file(file_to_modify_path, find_string, replace_string)

                            # Update patch summary
                            if file_to_modify_path in patch_summary:
                                patch_summary[file_to_modify_path] += 1
                            else:
                                patch_summary[file_to_modify_path] = 1
                        except Exception as e:
                            logging.error(f"Error modifying file {file_to_modify_path}: {e}")
                    else:
                        logging.warning(f"File to modify not found: {file_to_modify_path}")
        except Exception as e:
            logging.error(f"Error reading config file {file_path}: {e}")
    # Log the summary of patches
    for file_path, count in patch_summary.items():
        file_name = os.path.basename(file_path)
        logging.info(f"{count} patch(es) Modifications applied to {file_name}")
else:
    logging.warning("Mod config data file not found.")
