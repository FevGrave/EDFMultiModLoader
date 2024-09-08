import os, sys, json

def check_arguments():
    if len(sys.argv) < 2:
        print("Usage: python script.py <output_directory>")
        sys.exit(1)
    return sys.argv[1]

def load_json_file(file_path):
    """Utility function to load a JSON file with UTF-8 encoding."""
    with open(file_path, "r", encoding='utf-8') as file:
        return json.load(file)

def add_new_modes_to_mode_list(mode_list, new_modes):
    """Adds new modes to the ModeList with an incremented Mission_Pack_Num value after every 2 additions."""
    Mission_Pack_Num = 3  # Starting value for Mission_Pack_Num
    usage_count = 0  # Counter for how many times the current Mission_Pack_Num value has been used
    for mode in new_modes:
        # Update the relevant dictionary in `mode['value']` list where Mission_Pack_Num should be inserted
        y_position = 9  # This needs to be adjusted based on your structure
        if len(mode['value']) > y_position:
            mode['value'][y_position] = {"type": "int", "value": Mission_Pack_Num}
            usage_count += 1
            if usage_count == 2:
                Mission_Pack_Num += 1
                usage_count = 0
        mode_list.append(mode)

def process_weapon_catalog_updates(soldier_init, weapon_catalog_updates, class_name):
    """Dynamically appends new weapon catalog entries for a specified soldier class and sorts them.
    
    Args:
        soldier_init (list): List of soldier initialization data.
        weapon_catalog_updates (list): List of updates specifying weapon and slot enhancements.
        class_name (str): The class name to target for updates.
    """
    for soldier in soldier_init:
        if soldier['value'][1]['value'] == class_name:
            weapon_slots = soldier['value'][4]['value']
            for update in weapon_catalog_updates:
                for slot_key, slot_info in update.items():
                    target_slot = next((slot for slot in weapon_slots if slot['value'][0]['value'] == slot_key), None)
                    if target_slot:
                        # Assume the update is always to the first integer array within a nested pointer within each slot
                        target_values = target_slot['value'][2]['value']
                        # Extend the list with new values
                        target_values.extend(slot_info['value'])
                        # Sort the list in place by the 'value' key of each dictionary
                        target_values.sort(key=lambda x: x['value'])
                    else:
                        print(f"Warning: No slot named '{slot_key}' found for {class_name}")

def debug_log(data, message="Debug Log"):
    """Function to log data structure for debugging purposes."""
    print(f"{message}: {json.dumps(data, indent=4)}")

def append_to_soldier_weapon_category(soldier_weapon_category, new_categories):
    """Appends new entries to the SoldierWeaponCategory"""
    soldier_weapon_category.extend(new_categories)
    
    soldier_weapon_category.sort(key=lambda x: x[0]['value'] if isinstance(x, list) and x else x['value'][0]['value'] if 'value' in x and isinstance(x['value'], list) and x['value'] else None)

# Paths and directory setup
IDD = "ImportDefaultData.json"
mod_config_directory_relative = "MOD CONFIG DATA PLACED HERE"
current_directory = os.path.dirname(os.path.abspath(__file__))
default_data_path = os.path.join(current_directory, IDD)
mod_config_directory = os.path.join(current_directory, mod_config_directory_relative)

# Load data
IDdata = load_json_file(default_data_path)

# Iterate over each file in the directory that ends with 'Mod_config_data.json'
for filename in os.listdir(mod_config_directory):
    if filename.endswith('Mod_config_data.json'):
        file_path = os.path.join(mod_config_directory, filename)
        mod_config = load_json_file(file_path)

        # Apply additions to the ModeList from each mod configuration file
        add_new_modes_to_mode_list(IDdata["ModeList"], mod_config.get("NewToAddModeList", []))
        # Example call for each soldier type
        process_weapon_catalog_updates(IDdata["SoldierInit"], mod_config.get("NewToAddWeaponCatalog-Ranger", []), "SoldierType_Ranger")
        process_weapon_catalog_updates(IDdata["SoldierInit"], mod_config.get("NewToAddWeaponCatalog-WingDiver", []), "SoldierType_WingDiver")
        process_weapon_catalog_updates(IDdata["SoldierInit"], mod_config.get("NewToAddWeaponCatalog-AirRaider", []), "SoldierType_AirRaider")
        process_weapon_catalog_updates(IDdata["SoldierInit"], mod_config.get("NewToAddWeaponCatalog-Fencer", []), "SoldierType_Fencer")
        {"name": "SoldierWeaponCategory", "type": "ptr", "value": IDdata["SoldierWeaponCategory"]},
        append_to_soldier_weapon_category(IDdata["SoldierWeaponCategory"], mod_config["NewToAddSoldierWeaponCategory"])

# Define the data structure for the output CONFIG.JSON file
Head = {
    "format": "SGO",
    "endian": "BE",
    "version": 258,
    "variables": [
        {"name": "ModeList", "type": "ptr", "value": IDdata["ModeList"]},
        {"name": "PackageName", "type": "string", "value": "DEFP"},
        {"name": "SoldierInit", "type": "ptr", "value": IDdata["SoldierInit"]},
        {"name": "SoldierWeaponCategory", "type": "ptr", "value": IDdata["SoldierWeaponCategory"]},
        {"name": "WeaponTable", "type": "string", "value": "app:/Weapon/WeaponTable.sgo"},
        {"name": "WeaponText", "type": "string", "value": "app:/Weapon/WeaponText.%LOCALE%.sgo"}
    ]
}

# Right before exporting the Head dictionary to a JSON file, add:
print("Building Config . . . ", end="", flush=True)
print("DONE")

output_directory = check_arguments()
config_file = os.path.join(output_directory, "CONFIG.json")

# Export the Head dictionary to a JSON file
with open(config_file, "w") as file:
    json.dump(Head, file, indent=4)