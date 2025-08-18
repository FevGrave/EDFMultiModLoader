import json
import sys
import os
import logging

# Constants for weapon table values
WEAPON_STATE_DISABLED = 3
WEAPON_STATE_ENABLED = 1
WEAPON_STATE_DEFAULT = 2

def setup_logging():
    """Configure logging for the script."""
    logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")

def load_json_file(filepath):
    """Safely loads a JSON file and handles errors."""
    if not os.path.exists(filepath):
        logging.error(f"File not found: {filepath}")
        return None
    try:
        with open(filepath, "r", encoding="utf-8") as f:
            return json.load(f)
    except json.JSONDecodeError as e:
        logging.error(f"Failed to parse JSON in {filepath}: {e}")
        return None
    except Exception as e:
        logging.error(f"Unexpected error loading {filepath}: {e}")
        return None

def update_weapon_table(output_dir):
    """Updates the weapon table based on user selections."""
    user_selections_path = os.path.join(output_dir, "user_selections.json")
    weapon_table_path = os.path.join(output_dir, "WEAPONTABLE.json")
    
    # Load user selections
    user_selections = load_json_file(user_selections_path)
    if not user_selections:
        return
    
    # Determine mission pack states
    mission_pack_01 = user_selections.get("GameMode_Offline_MissionPack01", False) or user_selections.get("GameMode_Online_MissionPack01", False)
    mission_pack_02 = user_selections.get("GameMode_Offline_MissionPack02", False) or user_selections.get("GameMode_Online_MissionPack02", False)
    
    # Load weapon table
    weapon_table = load_json_file(weapon_table_path)
    if not weapon_table:
        return
    
    # Get the main weapon table entries
    variables = weapon_table.get("variables", [])
    if not variables:
        logging.error("No variables found in weapon table.")
        return
    
    main_table = variables[0].get("value", [])
    for weapon_entry in main_table:
        weapon_data = weapon_entry.get("value", [])
        if len(weapon_data) < 9:
            continue
        
        # Extract weapon identifier from index 0
        identifier_entry = weapon_data[0].get("value", "")
        if not isinstance(identifier_entry, str):
            continue
        
        # Update weapon state based on DLC
        if identifier_entry.startswith("MPACK_A_"):
            # Set to ENABLED if MP1 is enabled, else ENABLED
            new_state = WEAPON_STATE_ENABLED if mission_pack_01 else WEAPON_STATE_DISABLED
            weapon_data[8]["value"] = new_state
        elif identifier_entry.startswith("MPACK_B_"):
            if not mission_pack_02:
                weapon_data[8]["value"] = WEAPON_STATE_DISABLED
            else:
                # Set to ENABLED only if MP2 is enabled and MP1 is disabled
                new_state = WEAPON_STATE_ENABLED if not mission_pack_01 else WEAPON_STATE_DEFAULT
                weapon_data[8]["value"] = new_state
    
    # Save updated weapon table
    try:
        with open(weapon_table_path, "w", encoding="utf-8") as f:
            json.dump(weapon_table, f, indent=4)
        logging.info("Weapon table updated successfully.")
    except Exception as e:
        logging.error(f"Failed to save updated weapon table: {e}")

def main(output_directory, current_dir):
    """Main function to update the weapon table."""
    if not os.path.exists(output_directory):
        logging.error("Output directory not found.")
        sys.exit(1)
    
    update_weapon_table(output_directory)

if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Usage: python ConfigWeaponCuller.py <output_directory> <current_dir>")
        sys.exit(1)
    
    setup_logging()
    output_dir = sys.argv[1]
    current_dir = sys.argv[2]
    main(output_dir)