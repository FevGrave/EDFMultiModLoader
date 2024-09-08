import json
import os
import sys

# Determine the directory where the script is located
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__ if '__file__' in globals() else sys.executable))

# Define paths
input_dir = os.path.join(SCRIPT_DIR, "MOD CONFIG DATA PLACED HERE")
import_data_file = os.path.join(SCRIPT_DIR, "ImportWeaponTable.json")
import_text_files = {
    "CN": os.path.join(SCRIPT_DIR, "ImportWeaponTextTable-CN.json"),
    "EN": os.path.join(SCRIPT_DIR, "ImportWeaponTextTable-EN.json"),
    "JA": os.path.join(SCRIPT_DIR, "ImportWeaponTextTable-JA.json"),
    "KR": os.path.join(SCRIPT_DIR, "ImportWeaponTextTable-KR.json"),
}

# Define paths to save the updated files in the "Common" folder two levels up
output_dir = os.path.abspath(os.path.join(SCRIPT_DIR, "../../"))
os.makedirs(output_dir, exist_ok=True)

output_data_file = os.path.join(output_dir, "WEAPONTABLE.json")
output_text_files = {
    "CN": os.path.join(output_dir, "WEAPONTEXT.CN.json"),
    "EN": os.path.join(output_dir, "WEAPONTEXT.EN.json"),
    "JA": os.path.join(output_dir, "WEAPONTEXT.JA.json"),
    "KR": os.path.join(output_dir, "WEAPONTEXT.KR.json"),
}

# Function to load a JSON file with UTF-8 encoding
def load_json(filepath):
    with open(filepath, 'r', encoding='utf-8') as file:
        return json.load(file)

# Function to save a JSON file with UTF-8 encoding
def save_json(filepath, data):
    with open(filepath, 'w', encoding='utf-8') as file:
        json.dump(data, file, ensure_ascii=False, indent=4)

# Main processing function
def process_files(input_dir, import_data_file, import_text_files):
    # Load the import files
    import_data = load_json(import_data_file)
    import_text = {lang: load_json(file) for lang, file in import_text_files.items()}

    # Loop through all Mod_config_data.json files in the input directory
    for filename in os.listdir(input_dir):
        if filename.endswith("Mod_config_data.json"):
            filepath = os.path.join(input_dir, filename)
            data = load_json(filepath)
            
            # Process NewToAddWeaponTables
            if "NewToAddWeaponTables" in data:
                for class_name, categories in data["NewToAddWeaponTables"].items():
                    for category, weapons in categories.items():
                        for weapon in weapons:
                            # Append Data node to ImportWeaponTable.json
                            import_data["variables"][0]["value"].append(weapon["Data"])
                            
                            # Append Text node to appropriate ImportWeaponTextTable-X.json files
                            for lang, text_file in import_text.items():
                                text_file["variables"][0]["value"].append(weapon["Text"])
    
    # Save the updated import files under new names in the Common folder
    save_json(output_data_file, import_data)
    for lang, output_file in output_text_files.items():
        save_json(output_file, import_text[lang])

# Run the processing function
process_files(input_dir, import_data_file, import_text_files)

print(f"Processing complete! Files saved to {output_dir}")
