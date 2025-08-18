import os, sys, json

def check_arguments():
    if len(sys.argv) < 3:
        print("Usage: python script.py <output_directory> <current_directory>")
        sys.exit(1)
    return sys.argv[1], sys.argv[2]

def load_json_file(file_name):
    # Check for external config directory first
    external_config_path = os.path.join(os.path.expanduser("~"), "EDF_Config", file_name)
    if os.path.exists(external_config_path):
        file_path = external_config_path
    else:
        # Fall back to internal file within the PyInstaller package
        base_path = getattr(sys, '_MEIPASS', os.path.dirname(os.path.abspath(__file__)))
        file_path = os.path.join(base_path, file_name)
    
    with open(file_path, "r", encoding="utf-8") as file:
        return json.load(file)

def add_new_modes_to_mode_list(mode_list, new_modes):
    Mission_Pack_Num_Start = max(
        [mode['value'][9]['value'] for mode in mode_list if 'value' in mode and len(mode['value']) > 9 and isinstance(mode['value'][9], dict)],
        default=3,
    ) + 1  # Start with the next available Mission_Pack_Num_Start
    usage_count = 0  # Initialize usage_count
    index = 9  # Adjust based on structure

    for mode in new_modes:
        # Ensure 'value' exists and has enough length
        if len(mode['value']) > index:
            # Assign Mission_Pack_Num_Start to the index
            mode['value'][index] = {"type": "int", "value": Mission_Pack_Num_Start}
            usage_count += 1

            # Update Mission_Pack_Num_Start every two modes
            if usage_count == 2:
                Mission_Pack_Num_Start += 1
                usage_count = 0
        else:
            print(f"Skipping mode: {mode}, 'value' length is less than index ({index})")

        # Append the updated mode to the mode_list
        mode_list.append(mode)

def process_weapon_catalog_updates(soldier_init, weapon_catalog):
    for class_name, weapon_slots in weapon_catalog.items():
        for soldier in soldier_init:
            if soldier['value'][1]['value'] == f"SoldierType_{class_name}":
                soldier_weapon_slots = soldier['value'][4]['value']
                for slot_key, slot_info in weapon_slots.items():
                    target_slot = next((slot for slot in soldier_weapon_slots if slot['value'][0]['value'] == slot_key), None)
                    if target_slot:
                        target_values = target_slot['value'][2]['value']
                        target_values.extend(slot_info['value'])
                        target_values.sort(key=lambda x: x['value'])
                    else:
                        print(f"Warning: No slot named '{slot_key}' found for {class_name}")

def transform_weapon_catalog(weapon_catalog):
    transformed_catalog = {class_name: weapons for class_name, weapons in weapon_catalog.items()}
    return transformed_catalog

def append_to_soldier_weapon_category(soldier_weapon_category, new_categories):
    soldier_weapon_category.extend(new_categories)
    soldier_weapon_category.sort(key=lambda x: x[0]['value'] if isinstance(x, list) else x['value'][0]['value'])

def main(output_directory, current_directory):
    default_data_path = os.path.join(current_directory, "ImportDefaultData.json")
    mod_config_directory = os.path.join(current_directory, "MOD CONFIG DATA PLACED HERE")

    IDdata = load_json_file(default_data_path)

    for filename in os.listdir(mod_config_directory):
        if filename.endswith('Mod_config_data.json'):
            file_path = os.path.join(mod_config_directory, filename)
            mod_config = load_json_file(file_path)

            add_new_modes_to_mode_list(IDdata["ModeList"], mod_config.get("NewToAddModeList", []))
            raw_catalog = mod_config.get("NewToAddWeaponCatalog", {})
            if isinstance(raw_catalog, dict):
                mod_config["NewToAddWeaponCatalog"] = transform_weapon_catalog(raw_catalog)
            else:
                print(f"Warning: NewToAddWeaponCatalog is not a dictionary (was {type(raw_catalog).__name__}). Initializing empty dict.")
                mod_config["NewToAddWeaponCatalog"] = {}

            process_weapon_catalog_updates(IDdata["SoldierInit"], mod_config["NewToAddWeaponCatalog"])
            append_to_soldier_weapon_category(IDdata["SoldierWeaponCategory"], mod_config.get("NewToAddSoldierWeaponCategory", []))

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

    config_file = os.path.join(output_directory, "CONFIG.json")
    with open(config_file, "w", encoding="utf-8") as file:
        json.dump(Head, file, indent=4)
    print("ConfigBuilder: CONFIG.json has been created successfully.")

if __name__ == "__main__":
    output_directory, current_directory = check_arguments()
    main(output_directory, current_directory)
