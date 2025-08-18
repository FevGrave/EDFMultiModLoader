import os, sys, codecs, json, tkinter as tk
from tkinter import simpledialog
from tkinter import messagebox, ttk
sys.stdout = codecs.getwriter("utf-8")(sys.stdout.detach())

LIGHT_THEME = {
    'background': '#f0f0f0',
    'text': '#000000',
    'button': '#e0e0e0',
    'button_text': '#000000',
    'scrollbar': '#cccccc',
    'scrollbar_thumb': '#999999',
    'checkbutton': '#e0e0e0',
    'checkbutton_text': '#000000',
    'label': '#f0f0f0',
    'label_text': '#000000'
}

DARK_THEME = {
    'background': '#2b2b2b',
    'text': '#ffffff',
    'button': '#3b3b3b',
    'button_text': '#ffffff',
    'scrollbar': '#555555',
    'scrollbar_thumb': '#777777',
    'checkbutton': '#3b3b3b',
    'checkbutton_text': '#ffffff',
    'label': '#2b2b2b',
    'label_text': '#ffffff'
}

current_theme = LIGHT_THEME

def close_application(root):
    # Perform any cleanup tasks here if needed
    print("Application is closing...")
    root.destroy()

def check_arguments():
    if len(sys.argv) < 3:
        print("Usage: python GamemodeConfig.py <output_directory> <current_directory>")
        sys.exit(1)
    return sys.argv[1], sys.argv[2]

def show_mode_selection(output_directory, current_directory):
    def check_dlc_files(save_data_dir):
        save_slots = ["saveslot00", "saveslot01", "saveslot02", "saveslot03"]
        dlc1_exists = True
        dlc2_exists = True

        for slot in save_slots:
            dlc1_path = os.path.join(save_data_dir, slot, "DEFP_DLC1.MST")
            dlc2_path = os.path.join(save_data_dir, slot, "DEFP_DLC2.MST")

            # Check for DLC1
            if os.path.isfile(dlc1_path):
                print("Player has played the DLC 1 Mission Pack on Vanilla EDF")
                dlc1_exists = False
            elif not dlc1_exists:
                print("Player does not own or has yet to play DLC 1 Mission Pack")

            # Check for DLC2
            if os.path.isfile(dlc2_path):
                print("Player has played the DLC 2 Mission Pack on Vanilla EDF")
                dlc2_exists = False
            elif not dlc2_exists:
                print("Player does not own or has yet to play DLC 2 Mission Pack")

        return dlc1_exists, dlc2_exists

    def find_paired_packs(mission_packs):
        paired_packs = {}
        for i in range(0, len(mission_packs), 2):  # Iterate in steps of 2
            if i + 1 < len(mission_packs):  # Ensure a pair exists
                paired_packs[mission_packs[i]] = mission_packs[i + 1]
                paired_packs[mission_packs[i + 1]] = mission_packs[i]
            else:
                # If an unpaired item exists, pair it with itself
                paired_packs[mission_packs[i]] = mission_packs[i]
        return paired_packs

    def apply_theme(theme):
        root.config(bg=theme['background'])
        style = ttk.Style()

        # Configure Scrollbar style
        style.configure(
            "Custom.TScrollbar",
            troughcolor=theme['scrollbar'],        # Scrollbar track color
            background=theme['scrollbar_thumb'],  # Scrollbar thumb (handle) color
            arrowcolor=theme['button_text']       # Up/Down arrow colors
        )
        style.map("Custom.TScrollbar", background=[("active", theme['scrollbar_thumb'])])

        style.layout("Custom.TScrollbar", [
            ("Vertical.Scrollbar.trough", {
                "children": [
                    ("Vertical.Scrollbar.thumb", {"expand": "1", "sticky": "nswe"})
                ],
                "sticky": "ns"
            }),
            ("Vertical.Scrollbar.uparrow", {"sticky": "n"}),  # Optional: Remove this line
            ("Vertical.Scrollbar.downarrow", {"sticky": "s"})  # Optional: Remove this line
        ])

        # Update all widgets with the current theme
        for widget in root.winfo_children():
            if isinstance(widget, tk.Frame):
                widget.config(bg=theme['background'])
            elif isinstance(widget, tk.Button):
                widget.config(bg=theme['button'], fg=theme['button_text'])
            elif isinstance(widget, ttk.Scrollbar):
                widget.config(style="Custom.TScrollbar")
            elif isinstance(widget, tk.Label):
                widget.config(bg=theme['label'], fg=theme['label_text'])
            elif isinstance(widget, tk.Canvas):
                widget.config(bg=theme['background'], highlightbackground=theme['background'])

                # Update widgets inside canvas
                for child in widget.winfo_children():
                    if isinstance(child, tk.Checkbutton):
                        child.config(bg=theme['background'], fg=theme['text'], selectcolor=theme['checkbutton'])
                    elif isinstance(child, tk.Label):
                        child.config(bg=theme['background'], fg=theme['text'])
            for child in widget.winfo_children():
                if isinstance(child, tk.Frame):
                    child.config(bg=theme['background'])
                elif isinstance(child, tk.Button):
                    child.config(bg=theme['button'], fg=theme['button_text'])
                elif isinstance(child, ttk.Scrollbar):
                    child.config(style="Custom.TScrollbar")
                elif isinstance(child, tk.Checkbutton):
                    child.config(bg=theme['background'], fg=theme['text'], selectcolor=theme['checkbutton'])
                elif isinstance(child, tk.Label):
                    child.config(bg=theme['label'], fg=theme['label_text'])
                elif isinstance(child, tk.Canvas):
                    child.config(bg=theme['background'], highlightbackground=theme['background'])

                    # Update widgets inside nested canvas
                    for sub_child in child.winfo_children():
                        if isinstance(sub_child, tk.Checkbutton):
                            sub_child.config(bg=theme['background'], fg=theme['text'], selectcolor=theme['checkbutton'])
                        elif isinstance(sub_child, tk.Label):
                            sub_child.config(bg=theme['background'], fg=theme['text'])

    def configure_mission_packs(save_data_dir):
        global pack_vars  # Make pack_vars accessible globally
        pack_vars = {}
        selected_count = tk.IntVar(value=0)  # Track the number of selected packs
        max_selections = 3

        # Check DLC files and build the mission pack list
        dlc1_exists, dlc2_exists = check_dlc_files(save_data_dir)
        mission_packs = [
            "GameMode_Scenario", "GameMode_OnlineScenario",
            "GameMode_Offline_MissionPack01", "GameMode_Online_MissionPack01",
            "GameMode_Offline_MissionPack02", "GameMode_Online_MissionPack02"
        ]

        # Add non-hardcoded mission packs dynamically
        extra_non_hard_coded_mission_packs = []
        config_path = os.path.join(output_directory, "CONFIG.json")
        try:
            with open(config_path, "r") as config_file:
                config_data = json.load(config_file)
                variables = config_data.get("variables", [])
                if variables:
                    for entry in variables[0].get("value", []):
                        mission_name = entry["value"][0].get("value", "")
                        if mission_name and mission_name not in mission_packs:
                            extra_non_hard_coded_mission_packs.append(mission_name)
        except (FileNotFoundError, json.JSONDecodeError) as e:
            messagebox.showerror(
                "Error",
                f"Failed to load CONFIG.json: {e}\nPlease ensure the file exists and is formatted correctly."
            )
            return

        # Combine all mission packs
        mission_packs.extend(extra_non_hard_coded_mission_packs)

        # Define paired mission packs
        paired_packs = find_paired_packs(mission_packs)

        # Create Checkbuttons for each mission pack
        for pack, paired_pack in paired_packs.items():
            if pack not in pack_vars:
                var = tk.BooleanVar(value=False)
                pack_vars[pack] = var
                pack_vars[paired_pack] = var  # Share the same BooleanVar

                state = "normal"
                if pack in ["GameMode_Scenario", "GameMode_OnlineScenario"]:
                    var.set(True)  # Default as selected
                    state = "disabled"  # Gray out permanently
                    selected_count.set(selected_count.get() + 1)
                elif "Offline_MissionPack01" in pack or "Online_MissionPack01" in pack:
                    state = "normal" if dlc1_exists else "disabled"
                elif "Offline_MissionPack02" in pack or "Online_MissionPack02" in pack:
                    state = "normal" if dlc2_exists else "disabled"

                tk.Checkbutton(
                    scrollable_frame, text=pack, variable=var, state=state,
                    command=lambda v=var, p=pack, pp=paired_pack: update_selection(v, p, pp)
                ).pack(anchor='w')

        def update_selection(var, pack, paired_pack):
            if var.get():
                if selected_count.get() < max_selections:
                    selected_count.set(selected_count.get() + 1)
                    pack_vars[paired_pack].set(True)  # Toggle the paired pack
                else:
                    var.set(False)  # Undo the selection if max is reached
                    messagebox.showwarning(
                        "Selection Limit",
                        f"You can only select up to {max_selections} mission packs."
                    )
            else:
                selected_count.set(selected_count.get() - 1)
                pack_vars[paired_pack].set(False)  # Deselect the paired pack

        # Create Checkbuttons for each mission pack
        for pack, paired_pack in paired_packs.items():
            if pack not in pack_vars:
                var = tk.BooleanVar(value=False)
                pack_vars[pack] = var
                pack_vars[paired_pack] = var  # Share the same BooleanVar

                state = "normal"
                if pack in ["GameMode_Scenario", "GameMode_OnlineScenario"]:
                    var.set(True)  # Default as selected
                    state = "disabled"  # Gray out permanently
                    selected_count.set(selected_count.get() + 1)
                elif "Offline_MissionPack01" in pack or "Online_MissionPack01" in pack:
                    state = "normal" if dlc1_exists else "disabled"
                elif "Offline_MissionPack02" in pack or "Online_MissionPack02" in pack:
                    state = "normal" if dlc2_exists else "disabled"

                tk.Checkbutton(
                    scrollable_frame, text=pack, variable=var, state=state,
                    command=lambda v=var, p=pack, pp=paired_pack: update_selection(v, p, pp)
                ).pack(anchor='w')

        def save_user_selections(output_directory, pack_vars):
            """Save selected mission packs to user_selections.json file."""
            user_selections = {pack: var.get() for pack, var in pack_vars.items()}
            user_selections_path = os.path.join(output_directory, "user_selections.json")
    
            try:
                with open(user_selections_path, "w", encoding="utf-8") as f:
                    json.dump(user_selections, f, indent=4)
                print(f"User selections saved to {user_selections_path}")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to save user selections: {e}")

        def confirm_selections():
            selected_packs = [k for k, v in pack_vars.items() if v.get()]
            if selected_count.get() > max_selections:
                messagebox.showerror(
                    "Too Many Selections",
                    f"You can only select up to {max_selections} mission packs."
                )
            else:
                try:
                    # Ensure config_path points to a valid file
                    if os.path.isdir(config_path):
                        raise IsADirectoryError(f"{config_path} is a directory, not a file.")

                    if not os.access(config_path, os.R_OK):
                        raise PermissionError(f"Cannot read {config_path}. Check file permissions.")

                    with open(config_path, "r", encoding="utf-8") as file:
                        config_data = json.load(file)

                    # Process the CONFIG.json file
                    process_config(config_path, selected_packs)

                    # Save the user selections to a JSON file
                    save_user_selections(output_directory, pack_vars)

                    messagebox.showinfo(
                        "Selections Saved",
                        f"Selected Mission Packs:\n{', '.join(selected_packs)}"
                    )
                except Exception as e:
                    print(f"Unexpected error: {e}")
                    messagebox.showerror("Error", f"An error occurred: {e}")

                close_application(root)

        tk.Button(left_frame, text="Confirm Mission Packs", command=confirm_selections).pack(pady=10)

    def clean_and_set_ninth_index_values(config_data):
        """
        Cleans and updates the 9th index values (mode["value"][9]["value"]) in config_data["variables"][0]["value"].
        Values are updated in sequential pairs: 0, 0, 1, 1, 2, 2, REST WILL BE DELETED OR IS DELETED
        """
        try:
            # Access the ModeList from the config data
            mode_list = config_data.get("variables", [])[0].get("value", [])

            # Initialize the sequence counter
            sequence_value = 0

            for idx, mode in enumerate(mode_list):
                # Ensure the mode structure is valid
                if "value" in mode and len(mode["value"]) > 9 and isinstance(mode["value"][9], dict):
                    # Set the value at index 9 to the current sequence value
                    mode["value"][9]["value"] = sequence_value

                    # Increment the sequence value every two modes
                    if idx % 2 == 1:
                        sequence_value += 1
                else:
                    print(f"Skipping invalid mode at index {idx}: {mode}")

            print(f"Successfully updated 9th index values in mode list.")
        except (KeyError, IndexError, TypeError) as e:
            print(f"Error while cleaning and setting 9th index values: {e}")

    def process_config(config_path, selected_mission_packs):
        try:
            with open(config_path, 'r', encoding='utf-8') as file:
                config_data = json.load(file)
            
            # Modify the configuration as needed
            filtered_mode_list = [
                mode for mode in config_data["variables"][0]["value"] if mode["value"][0]["value"] in selected_mission_packs
            ]
            config_data["variables"][0]["value"] = filtered_mode_list

            clean_and_set_ninth_index_values(config_data)

            # Ensure the file is writable before saving
            if os.path.exists(config_path):
                os.chmod(config_path, 0o666)  # Set file to be writable

            with open(config_path, 'w', encoding='utf-8') as file:
                json.dump(config_data, file, indent=4)

            print(f"Updated CONFIG.json saved. Retained {len(filtered_mode_list)} mission packs.")
        except PermissionError as e:
            print(f"PermissionError: {e}")
            messagebox.showerror("Error", f"Permission denied. Ensure you have write access to: {config_path}")
        except Exception as e:
            print(f"Error processing CONFIG.json: {e}")
            messagebox.showerror("Error", f"An error occurred while processing CONFIG.json:\n{e}")


            # Load the CONFIG.json file
            with open(config_path, 'r', encoding='utf-8') as file:
                config_data = json.load(file)

            # Ensure 'variables' exists and is properly structured
            variables = config_data.get("variables", [])
            if not variables or "value" not in variables[0]:
                raise KeyError("Invalid CONFIG.json structure: 'variables[0][value]' missing.")

            # Get the ModeList from the config
            all_mission_packs = [
                mode["value"][0]["value"] for mode in variables[0]["value"]
            ]

            # Filter out non-selected mission packs
            filtered_mode_list = [
                mode for mode in variables[0]["value"] if mode["value"][0]["value"] in selected_mission_packs
            ]

            # Update the config with filtered ModeList
            config_data["variables"][0]["value"] = filtered_mode_list

            # Update the 9th index values
            clean_and_set_ninth_index_values(config_data)

            # Save the updated CONFIG.json
            with open(config_path, 'w', encoding='utf-8') as file:
                json.dump(config_data, file, indent=4)

            print(f"Updated CONFIG.json saved. Retained {len(filtered_mode_list)} mission packs.")

        except PermissionError as e:
            print(f"PermissionError: {e}")
            messagebox.showerror("Error", f"Permission denied. Ensure you have write access to: {config_path}")
        except Exception as e:
            print(f"Error processing CONFIG.json: {e}")
            messagebox.showerror("Error", f"An error occurred while processing CONFIG.json:\n{e}")

    root = tk.Tk()
    root.title("EDF Mission Pack Configuration Tool")
    root.geometry("850x400")

    # Apply initial theme
    apply_theme(LIGHT_THEME)
    left_frame = tk.Frame(root)
    left_frame.pack(side="left", padx=20, pady=20)

    tk.Label(left_frame, text="Toggle between light and dark themes for better visibility.").pack(pady=5)

    right_frame = tk.Frame(root)
    right_frame.pack(side="right", padx=20, pady=20) 

    # Add a toggle theme button to the left frame
    def toggle_theme():
        global current_theme
        if current_theme == LIGHT_THEME:
            current_theme = DARK_THEME
        else:
            current_theme = LIGHT_THEME
        apply_theme(current_theme)

    theme_button = tk.Button(left_frame, text="Toggle Theme", command=toggle_theme)
    theme_button.pack(pady=5)

    # Scrollable area for mission packs in the right frame
    canvas = tk.Canvas(right_frame)
    scroll_y = ttk.Scrollbar(right_frame, orient="vertical", command=canvas.yview)
    scrollable_frame = ttk.Frame(canvas)

    scrollable_frame.bind(
        "<Configure>",
        lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
    )
    canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
    canvas.configure(yscrollcommand=scroll_y.set)

    canvas.pack(side="left", fill="both", expand=True)
    scroll_y.pack(side="right", fill="y")

    tk.Label(left_frame, text="Base EDF 6 mission packs are pre-selected and cannot be deselected.").pack(pady=5)
    tk.Label(left_frame, text="You can select up to 2 additional mission packs,").pack(pady=5)
    tk.Label(left_frame, text="Offline and Online packs count as 1 selection for syncing.").pack(pady=5)

    # Call function to configure mission packs
    save_data_dir = os.path.join(os.getenv("LOCALAPPDATA"), "EarthDefenceForce6", "SAVE_DATA")
    configure_mission_packs(save_data_dir)

    # Start the Tkinter main loop
    root.mainloop()

def main(output_directory, current_directory):
    show_mode_selection(output_directory, current_directory)

if __name__ == "__main__":
    output_directory, current_directory = check_arguments()
    main(output_directory, current_directory)