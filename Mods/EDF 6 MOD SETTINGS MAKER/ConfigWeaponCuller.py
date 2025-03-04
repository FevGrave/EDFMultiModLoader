import json
import os
import sys
import glob

def load_json(file_path):
    """Load JSON data from a given file path."""
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            return json.load(f)
    except FileNotFoundError:
        print(f"Error: File '{file_path}' not found.")
        sys.exit(1)
    except json.JSONDecodeError:
        print(f"Error: Failed to parse JSON from '{file_path}'.")
        sys.exit(1)

def save_json(file_path, data):
    """Save JSON data to a file with UTF-8 encoding."""
    with open(file_path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
    print(f"Updated weapon table saved to {file_path}")

def find_all_mod_config_files(directory):
    """Find all JSON files that end with Mod_config_data.json."""
    return glob.glob(os.path.join(directory, "*Mod_config_data.json"))

def extract_weapons_from_mod_config(config_file):
    """Extract weapon names from Mod_config_data.json."""
    data = load_json(config_file)
    mod_name = data["MOD_INFO"][0]["MOD NAME"]
    weapon_names = set()
    weapon_tables = data.get("NewToAddWeaponTables", {})

    for class_name, categories in weapon_tables.items():
        for category, weapons in categories.items():
            for weapon in weapons:
                weapon_name = weapon.get("Data", {}).get("value", [])[0]["value"]
                weapon_names.add(weapon_name)

    return mod_name, weapon_names

def process_mod_configs(config_files, user_selections):
    """Process multiple mod configuration files and determine rankings."""
    mod_configs = {}
    weapon_name_to_mod = {}
    enabled_mission_packs = []

    for file in config_files:
        data = load_json(file)
        mod_name, weapon_names = extract_weapons_from_mod_config(file)
        weapon_name_to_mod.update({name: mod_name for name in weapon_names})

        weapon_drop_status = data["MOD_INFO"][0].get("MY WEAPONS DROP WITH MY TWO MISSION PACKS", False)

        # Handle potential missing or empty NewToAddModeList safely
        offline_mission_pack = None
        new_mode_list = data.get("NewToAddModeList", [])
        if new_mode_list and isinstance(new_mode_list, list) and len(new_mode_list) > 0:
            first_mode = new_mode_list[0].get("value", [])
            if first_mode and isinstance(first_mode, list) and len(first_mode) > 0:
                offline_mission_pack = first_mode[0].get("value")

        if offline_mission_pack and user_selections.get(offline_mission_pack, False):
            enabled_mission_packs.append(mod_name)

        mod_configs[mod_name] = {"weapon_drop_status": weapon_drop_status}

    mission_pack_ranks = {}
    enabled_mission_packs.sort()

    if enabled_mission_packs:
        mission_pack_ranks[enabled_mission_packs[0]] = (1, mod_configs[enabled_mission_packs[0]]["weapon_drop_status"])
    if len(enabled_mission_packs) >= 2:
        mission_pack_ranks[enabled_mission_packs[1]] = (2, mod_configs[enabled_mission_packs[1]]["weapon_drop_status"])

    for mod_name in mod_configs:
        if mod_name not in mission_pack_ranks:
            mission_pack_ranks[mod_name] = (3 if mod_configs[mod_name]["weapon_drop_status"] else 0, False)

    print("\nDEBUG: Mission Pack Ranks:", mission_pack_ranks)
    return mission_pack_ranks, weapon_name_to_mod

def update_weapon_table(weapon_table, mission_pack_ranks, weapon_name_to_mod):
    """Update weapons' 8th index based on mission pack rankings, handling duplicates."""
    updated_count = 0

    for weapon_entry in weapon_table["variables"][0]["value"]:
        weapon_name = weapon_entry["value"][0]["value"]
        current_rank = weapon_entry["value"][8]["value"]
        
        if weapon_name in weapon_name_to_mod:
            mod_name = weapon_name_to_mod[weapon_name]
            new_rank, _ = mission_pack_ranks.get(mod_name, (3, False))
            
            if not isinstance(new_rank, int):
                print(f"WARNING: Incorrect rank format for {mod_name} -> {new_rank}")
                new_rank = 3
            
            if new_rank != current_rank:
                weapon_entry["value"][8]["value"] = new_rank
                updated_count += 1
                print(f"Updated: {weapon_name} -> Rank {new_rank}")

    print(f"\nTotal Weapons Updated: {updated_count}")
    return weapon_table

def main(output_directory, current_dir):
    """Main function to process multiple mod configuration JSON files."""
    mod_config_dir = os.path.join(current_dir, "MOD CONFIG DATA PLACED HERE")
    weapon_table_path = os.path.join(output_directory, "WEAPONTABLE.json")
    
    print(f"Searching for Mod_config_data.json files in: {mod_config_dir}")
    config_files = find_all_mod_config_files(mod_config_dir)

    if not config_files:
        print("Error: No Mod_config_data.json files found.")
        sys.exit(1)

    user_selections_path = os.path.join(output_directory, "user_selections.json")
    if not os.path.exists(user_selections_path):
        print(f"Error: File '{user_selections_path}' not found.")
        sys.exit(1)

    user_selections = load_json(user_selections_path)
    mission_pack_ranks, weapon_name_to_mod = process_mod_configs(config_files, user_selections)
    weapon_data = load_json(weapon_table_path)
    
    if weapon_data:
        updated_weapon_data = update_weapon_table(weapon_data, mission_pack_ranks, weapon_name_to_mod)
        save_json(weapon_table_path, updated_weapon_data)

if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Usage: python ConfigWeaponCuller.py <output_directory> <current_dir>")
        sys.exit(1)
    
    output_dir = sys.argv[1]
    current_dir = sys.argv[2]
    main(output_dir, current_dir)
