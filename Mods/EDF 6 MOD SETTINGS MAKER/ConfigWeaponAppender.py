import os
import json
import sys

def check_arguments():
    if len(sys.argv) < 3:
        print("Usage: python script.py <output_directory> <current_directory>")
        sys.exit(1)
    return sys.argv[1], sys.argv[2]

# Utility function to load a JSON file with UTF-8 encoding
def load_json(filepath):
    try:
        with open(filepath, 'r', encoding='utf-8') as file:
            return json.load(file)
    except FileNotFoundError:
        print(f"Error: File {filepath} not found.")
        sys.exit(1)
    except json.JSONDecodeError as e:
        print(f"Error: Failed to parse JSON {filepath}. Reason: {e}")
        sys.exit(1)

# Utility function to save a JSON file with UTF-8 encoding
def save_json(filepath, data):
    try:
        with open(filepath, 'w', encoding='utf-8') as file:
            json.dump(data, file, ensure_ascii=False, indent=4)
    except Exception as e:
        print(f"Error: Failed to save JSON to {filepath}. Reason: {e}")

# Main processing function
def process_files(input_dir, import_data, import_text):
    # Loop through all Mod_config_data.json files in the input directory
    for filename in os.listdir(input_dir):
        if filename.endswith("Mod_config_data.json"):
            filepath = os.path.join(input_dir, filename)
            data = load_json(filepath)
            
            # Process NewToAddWeaponTables if present
            if "NewToAddWeaponTables" in data:
                for class_name, categories in data["NewToAddWeaponTables"].items():
                    for category, weapons in categories.items():
                        for weapon in weapons:
                            # Append Data node to ImportWeaponTable.json
                            import_data["variables"][0]["value"].append(weapon["Data"])
                            
                            # Append Text node to appropriate ImportWeaponTextTable-X.json files
                            en_text = weapon["Text"].get("EN", [])  # Use English as fallback
                            for lang in ["CN", "EN", "JA", "KR", "SC"]:
                                if lang in import_text:
                                    text_to_add = weapon["Text"].get(lang, en_text)  # Use EN if missing
                                    import_text[lang]["variables"][0]["value"].append(text_to_add)

def main(output_directory, current_directory):
    # Define paths based on provided directories
    input_dir = os.path.join(current_directory, "MOD CONFIG DATA PLACED HERE")
    import_data_file = os.path.join(current_directory, "ImportWeaponTable.json")
    import_text_files = {
        "CN": os.path.join(current_directory, "ImportWeaponTextTable-CN.json"),
        "EN": os.path.join(current_directory, "ImportWeaponTextTable-EN.json"),
        "JA": os.path.join(current_directory, "ImportWeaponTextTable-JA.json"),
        "KR": os.path.join(current_directory, "ImportWeaponTextTable-KR.json"),
        "SC": os.path.join(current_directory, "ImportWeaponTextTable-SC.json"),
    }

    # Define output paths for processed files
    os.makedirs(output_directory, exist_ok=True)
    output_data_file = os.path.join(output_directory, "WEAPONTABLE.json")
    output_text_files = {
        "CN": os.path.join(output_directory, "WEAPONTEXT.CN.json"),
        "EN": os.path.join(output_directory, "WEAPONTEXT.EN.json"),
        "JA": os.path.join(output_directory, "WEAPONTEXT.JA.json"),
        "KR": os.path.join(output_directory, "WEAPONTEXT.KR.json"),
        "SC": os.path.join(output_directory, "WEAPONTEXT.SC.json"),
    }

    # Load the main import files
    import_data = load_json(import_data_file)
    import_text = {lang: load_json(file) for lang, file in import_text_files.items()}

    # Process all Mod_config_data.json files
    process_files(input_dir, import_data, import_text)

    # Save the updated import files
    save_json(output_data_file, import_data)
    for lang, output_file in output_text_files.items():
        save_json(output_file, import_text[lang])

    print(f"Processing complete! Files saved to {output_directory}")

# Allow the script to be called directly or from another script
if __name__ == "__main__":
    output_directory, current_directory = check_arguments()
    main(output_directory, current_directory)
