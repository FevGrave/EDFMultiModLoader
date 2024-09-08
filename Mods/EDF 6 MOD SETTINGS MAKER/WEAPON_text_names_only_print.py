import os, json

# Counts per category as provided
weapon_counts = {
    "RANGER": {
        "Assault Rifles": 45,
        "Shotguns": 28,
        "Snipers": 31,
        "Rocket Launchers": 34,
        "Missile Launchers": 20,
        "Grenades": 41,
        "Special": 58,
        "Support Equipment": 38,
        "Bikes": 9,
        "Tanks": 13,
        "Helicopters": 10
    },
    "WINGDIVER": {
        "Short-Range": 45,
        "Mid-Range Kinetic Weapons": 32,
        "Mid-Range Pulse Weapons": 23,
        "Mid-Range Energy Weapons": 25,
        "Long-Range": 22,
        "Ranged Weapons": 39,
        "Homing Weapons": 19,
        "Special": 21,
        "Plasma Cores": 35
    },
    "FENCER":{
        "CC Strikers": 25,
        "CC Piercers": 26,
        "Shields": 24,
        "Autocannons": 32,
        "Cannons": 33,
        "Missile Launchers": 24,
        "Enhanced Boosters": 18,
        "Enhanced Shields": 12,
        "Enhanced Cannons": 6,
        "Enhanced Exoskeletons": 11
    },
    "AIRRAIDER":{
        "Request Artillery Units": 17,
        "Request Gunships": 37,
        "Request Bombers": 33,
        "Request Missiles": 15,
        "Request Satellites": 20,
        "Limpet Guns": 23,
        "Stationary Weapons": 24,
        "Support Equipment": 35,
        "Special": 28,
        "Empty": 1,
        "Powered Exoskeletons": 21,
        "Special Weapons": 15,
        "Helicopters": 6,
        "Ground Vehicles": 20,
        "Tanks": 20
    },
    "DLC":{
        "DLC PACK 01": 34,
        "DLC PACK 02": 39
    }
}

def load_json_data(filepath):
    """Load and return the JSON data from the specified file."""
    with open(filepath, 'r', encoding='utf-8') as file:  # Specify UTF-8 encoding
        return json.load(file)


def debug_print_items(data, weapon_counts, output_file_path):
    """Prints items from the data structure based on the provided weapon counts to a specified text file."""
    items = data["variables"][0]["value"]  # Directly accessing the 'value' list of 'text_table'
    current_index = 0

    with open(output_file_path, 'w', encoding='utf-8') as file:
        for class_name, categories in weapon_counts.items():
            file.write(f"Class: {class_name}\n")
            for category_name, count in categories.items():
                file.write(f"  Category: {category_name}\n")
                for i in range(count):
                    if current_index < len(items):
                        item = items[current_index]
                        # Assuming each 'item' has a 'value' list, and the first item in this list has the name
                        file.write(f"    Item: {item['value'][0]['value']}\n")
                        current_index += 1
                    else:
                        file.write("    No more items available.\n")
                        break
                file.write("  End of Category\n\n")
            file.write("End of Class\n\n")

# Example of how to use the modified function
current_directory = os.path.dirname(os.path.abspath(__file__))
json_filepath = os.path.join(current_directory, "ImportWeaponTextTable-EN.json")
data = load_json_data(json_filepath)

# Assuming data and weapon_counts are defined as before
output_file_path = os.path.join(current_directory, "output_text_file.txt")
debug_print_items(data, weapon_counts, output_file_path)