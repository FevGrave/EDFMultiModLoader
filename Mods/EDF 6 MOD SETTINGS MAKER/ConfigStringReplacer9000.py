import os, glob, json
import logging

# Set up logging with detailed information
logging.basicConfig(level=logging.INFO, format='%(message)s')

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
                            with open(file_to_modify_path, 'r+', encoding='utf-8') as mod_file:
                                file_data = json.load(mod_file)
                                patches = replace_nested_value(file_data, find_string, replace_string)
                                mod_file.seek(0)
                                json.dump(file_data, mod_file, ensure_ascii=False, indent=4)
                                mod_file.truncate()
                                # Include the "File" key in the output
                                file_name = os.path.basename(file_to_modify_path)
                                if file_to_modify_path in patch_summary:
                                    patch_summary[file_to_modify_path] += patches
                                else:
                                    patch_summary[file_to_modify_path] = patches
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
