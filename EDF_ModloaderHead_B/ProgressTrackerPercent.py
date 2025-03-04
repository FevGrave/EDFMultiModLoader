#ProgressTrackerPercent.py
import os, json, tkinter as tk
from tkinter import ttk

'''
NOTE THE HEAD USES THE THIS AS EXE NOT THE PY
'''

def get_version():
    return "0.0.2"

# Initialize as None to be set by an external function
settings = {}

def set_working_directory():
    """Sets the working directory to the current file's location."""
    os.chdir(os.path.dirname(os.path.abspath(__file__)))

def initialize_settings(current_dir):
    """Initializes settings with a specified directory."""
    global current_directory, settings
    current_directory = current_dir
    settings = load_settings(current_directory)
    

def load_settings(current_directory):
    """Load settings from a JSON file, with default fallback and validation."""
    settings_file = "MMLsettings.json"
    default_settings = {
        "edf6_platform": "steam",
        "platform_can_be": "steam|epic",
        "base_dir": current_directory,
        "modloader_HAKKEN_style": "NI",
        "colors": {
            "JustBackGround": "#484848",
            "ButtonBackGround": "#000000",
            "ButtonPressedBackGround": "#010e70",
            "TextColor": "#B3FF00",
            "PressedTextColor": "#ffffff",
            "Helpful Color Blind Site": "https://davidmathlogic.com/colorblind/#%23484848-%23000000-%23010E70-%23FFFFFF"
        },
        "modloader_status": "Enabled",
        "modloader_status_can_be": "Enabled|Disabled, DONT EDIT AS THIS IS VISUAL TEXT",
        "progress": {
            "Last Game": "EDF 6",
            "EDF 6": 0.0,
            "( 6 ) DLC Lost Days": 0.0,
            "( 6 ) DLC Visions of Malice": 0.0,
            "EDF 5": 0.0,
            "( 5 ) DLC Mission Pack 1": 0.0,
            "( 5 ) DLC Mission Pack 2": 0.0,
            "EDF 4.1": 0.0,
            "(4.1) DLC Mission Pack 1": 0.0,
            "(4.1) DLC Mission Pack 2": 0.0,
            "EDF World Brothers": 0.0,
            "(WB ) Additional Mission Pack: Another ResCUBE": 0.0,
            "EDF World Brothers 2": 0.0,
            "(WB2) Extra Mission Pack: Robo Saurous vs the Mecharmy": 0.0,
            "Custom Mod Pack": 0.0
        },
        "Custom Mod Pack": {
            "ClassCount": 4,
            "Difficulties": 5,
            "Missions": 100,
            "NoLimits": 0.7
        }
    }

    try:
        if os.path.exists(settings_file):
            with open(settings_file, 'r') as file:
                settings = json.load(file)
                for key, value in default_settings.items():
                    if key not in settings:
                        settings[key] = value
                return settings
    except json.JSONDecodeError:
        print("Error loading settings, reverting to defaults.")

    save_settings(default_settings)
    return default_settings

def save_settings(settings):
    """Save settings to a JSON file."""
    settings_file = "MMLsettings.json"
    try:
        with open(settings_file, 'w') as file:
            json.dump(settings, file, indent=4)
    except Exception as e:
        print(f"Error saving settings: {e}")

def get_settings():
    """Getter for settings."""
    return settings

def debug_tk_instances():
    if tk._default_root:
        print("Root Tk instance found")
    else:
        print("No Root Tk instance")

# Tuple of games with parameters, notes and mod pack support
games = {
    #"Game": (ClassCount, Difficulties, Missions, NoLimits, Notes)
    "EDF 6": (4, 5, 147, 0.70, "`Hard` diff can give you `Normal` & `Easy` Medals, Online & Offline share progress"),
    "( 6 ) DLC Lost Days": (4, 5, 19, 0.70, "`Hard` diff can give you `Normal` & `Easy` Medals, Online & Offline share progress"),
    "( 6 ) DLC Visions of Malice": (4, 5, 40, 0.70, "`Hard` diff can give you `Normal` & `Easy` Medals, Online & Offline share progress"),
    "EDF 5": (4, 5, 111, 0.70, "`Hard` diff can give you `Normal` & `Easy` Medals, Online & Offline can't share progress"),
    "( 5 ) DLC Mission Pack 1": (4, 5, 15, 0.70, "`Hard` diff can give you `Normal` & `Easy` Medals, Online & Offline can't share progress"),
    "( 5 ) DLC Mission Pack 2": (4, 5, 14, 0.70, "`Hard` diff can give you `Normal` & `Easy` Medals, Online & Offline can't share progress"),
    "EDF 4.1": (4, 5, 98, 0.70, "You have to play each diff per class, Online & Offline can't share progress"),
    "(4.1) DLC Mission Pack 1": (4, 5, 26, 0.70, "You have to play each diff per class, Online & Offline can't share progress"),
    "(4.1) DLC Mission Pack 2": (4, 5, 20, 0.70, "You have to play each diff per class, Online & Offline can't share progress"),
    "EDF World Brothers": (1, 5, 60, 0.80, "Voxel EDF"),
    "(WB ) Additional Mission Pack: Another ResCUBE": (1, 6, 11, 0.80, "Voxel EDF"),
    "EDF World Brothers 2": (1, 5, 104, 0.80, "Voxel EDF The sequel"),
    "(WB2) Extra Mission Pack: Robo Saurous vs the Mecharmy": (1, 6, 16, 0.80, "Voxel EDF The sequel"),
    "Custom Mod Pack": (None, None, None, None, "Custom mod pack: Edit: Class Count, Difficulties, Missions, No Limits Percentage.")
}

# Custom values for the mod pack (initialized to default)
custom_mod_values = {
    "ClassCount": 4,
    "Difficulties": 5,
    "Missions": 100,
    "NoLimits": 0.70
}

def load_progress_for_game(game_name):
    saved_progress = load_settings().get("progress", {})

    game_names = list(games.keys())[:9]  # First 9 games

    # Set the completion values for each game individually
    for i, game_name in enumerate(game_names):
        if game_name in saved_progress:
            completion_value = saved_progress[game_name]
            completion_entry.delete(0, tk.END)
            completion_entry.insert(0, f"{completion_value:.2f}")  # Insert saved value
            completion_slider.set(completion_value)  # Set the slider as well
        else:
            completion_entry.delete(0, tk.END)
            completion_entry.insert(0, "0.00")  # Default to 0.00
            completion_slider.set(0.00)
            
    return saved_progress.get(game_name, 0.00)  # Default to 0.00 if no saved progress is found

def load_last_game():
    saved_progress = settings.get("progress", {})
    return saved_progress.get("Last Game", "EDF 6")  # Default to "EDF 6" if no last game found

def save_progress_on_close():
    current_game = game_combobox.get()
    completion_value = float(completion_entry.get())
    
    # Ensure the 'progress' key exists in settings
    if "progress" not in settings:
        settings["progress"] = {}
    settings["progress"][current_game] = completion_value
    settings["progress"]["Last Game"] = current_game

    # Save Custom Mod Pack settings
    if current_game == "Custom Mod Pack":
        settings["Custom Mod Pack"] = {
            "ClassCount": custom_mod_values["ClassCount"],
            "Difficulties": custom_mod_values["Difficulties"],
            "Missions": custom_mod_values["Missions"],
            "NoLimits": custom_mod_values["NoLimits"]
        }
    
    save_settings(settings)

# Function to load progress for each individual game
def load_individual_game_progress(game_name):
    # Load the saved settings, including progress data
    saved_progress = settings.get("progress", {})
    
    # Load the custom mod settings if the game is "Custom Mod Pack"
    if game_name == "Custom Mod Pack" and "Custom Mod Pack" in settings:
        custom_settings = settings["Custom Mod Pack"]
        custom_mod_values["ClassCount"] = custom_settings.get("ClassCount", 4)
        custom_mod_values["Difficulties"] = custom_settings.get("Difficulties", 5)
        custom_mod_values["Missions"] = custom_settings.get("Missions", 100)
        custom_mod_values["NoLimits"] = custom_settings.get("NoLimits", 0.70)

        # Update the GUI entries with the saved custom values
        class_count_entry.delete(0, tk.END)
        class_count_entry.insert(0, custom_mod_values["ClassCount"])

        difficulties_entry.delete(0, tk.END)
        difficulties_entry.insert(0, custom_mod_values["Difficulties"])

        missions_entry.delete(0, tk.END)
        missions_entry.insert(0, custom_mod_values["Missions"])

        no_limits_entry.delete(0, tk.END)
        no_limits_entry.insert(0, custom_mod_values["NoLimits"])
    
    # Load the completion percentage if saved in progress
    if game_name in saved_progress:
        completion_value = saved_progress[game_name]
        completion_entry.delete(0, tk.END)
        completion_entry.insert(0, f"{completion_value:.2f}")  # Insert saved value into the entry
        completion_slider.set(completion_value)  # Update the slider with the saved value
    else:
        # Default to 0.00 if no saved progress is found
        completion_entry.delete(0, tk.END)
        completion_entry.insert(0, "0.00")
        completion_slider.set(0.00)

def save_individual_game_progress(game_name):
    # Load the current settings, which include progress data
    saved_progress = load_settings(current_directory).get("progress", {})
    
    # Save the completion value for the specific game
    completion_value = float(completion_entry.get())
    saved_progress[game_name] = completion_value
    
    # Update the settings dictionary with the new progress data
    settings["progress"] = saved_progress
    
    # Save the settings to the file, appending the new progress data
    save_settings(settings)

def on_game_selection(event):
    selected_game = game_combobox.get()

    # Only load progress for the first 6 games
    if selected_game in list(games.keys())[:6]:
        load_individual_game_progress(selected_game)

        completion_value = load_progress_for_game(selected_game)
        completion_entry.delete(0, tk.END)
        completion_entry.insert(0, f"{completion_value:.2f}")
        completion_slider.set(completion_value)  # Update the slider with the loaded value

def initialize_previous_game():
    global previous_game
    previous_game = game_combobox.get()

# Global variable to track the previous game
previous_game = load_last_game()  # Initialize with the last saved game on startup

def on_game_selection_change(event):
    global previous_game
    
    # Save progress for the previously selected game
    if previous_game:
        save_individual_game_progress(previous_game)
    
    # Load progress for the newly selected game
    selected_game = game_combobox.get()
    load_individual_game_progress(selected_game)
    
    # Update the previous game to the newly selected game
    previous_game = selected_game

    toggle_custom_settings()

# Function to hide or show custom mod pack settings based on game selection
def toggle_custom_settings():
    selected_game = game_combobox.get()
    if selected_game == "Custom Mod Pack":
        # Show custom mod settings
        class_count_label.grid()
        class_count_entry.grid()
        difficulties_label.grid()
        difficulties_entry.grid()
        missions_label.grid()
        missions_entry.grid()
        no_limits_label.grid()
        no_limits_entry.grid()
    else:
        # Hide custom mod settings
        class_count_label.grid_remove()
        class_count_entry.grid_remove()
        difficulties_label.grid_remove()
        difficulties_entry.grid_remove()
        missions_label.grid_remove()
        missions_entry.grid_remove()
        no_limits_label.grid_remove()
        no_limits_entry.grid_remove()

    # Automatically calculate results after game change
    calculate_results()

def update_completion_entry(val):
    # Snap the slider to the closest Medal value
    snap_to_closest_Medal(float(val))

def snap_to_closest_Medal(current_value):
    total_Medals = get_total_Medals()
    completion_per_Medal = 100 / total_Medals

    # Calculate the closest Medal count
    closest_Medal = round(current_value / completion_per_Medal)

    # Convert it back to the percentage value
    snapped_completion = closest_Medal * completion_per_Medal

    # Update both the entry and the slider to the snapped value
    completion_entry.delete(0, tk.END)
    completion_entry.insert(0, f"{snapped_completion:.2f}")
    completion_slider.set(snapped_completion)
    calculate_results()

def update_completion_slider(event):
    try:
        entry_value = float(completion_entry.get())
        completion_slider.set(entry_value)
    except ValueError:
        pass  # Ignore invalid entries

# Function to calculate the total number of Medals based on selected game
def get_total_Medals():
    selected_game = game_combobox.get()
    if selected_game == "Custom Mod Pack":
        ClassCount = custom_mod_values["ClassCount"]
        Difficulties = custom_mod_values["Difficulties"]
        Missions = custom_mod_values["Missions"]
    else:
        ClassCount, Difficulties, Missions, _, _ = games[selected_game]
    return ClassCount * Difficulties * Missions

# Function to adjust completion rate based on Medal count
def adjust_completion_by_Medals(Medal_count):
    total_Medals = get_total_Medals()
    current_completion = float(completion_entry.get())
    completion_per_Medal = 100 / total_Medals
    new_completion = max(0, min(100, current_completion + (Medal_count * completion_per_Medal)))
    snap_to_closest_Medal(new_completion)
    completion_entry.delete(0, tk.END)
    completion_entry.insert(0, f"{new_completion:.2f}")
    update_completion_slider(None)
    calculate_results()

# Function to handle slider clicks on the sides
def on_slider_click(event):
    # Get the width of the slider widget
    slider_width = completion_slider.winfo_width()

    # Get the current value of the slider
    current_value = float(completion_slider.get())

    # Calculate the position where the click occurred relative to the slider
    click_position = event.x / slider_width * 100  # Convert to a percentage-based click position

    # Check if the click was on the left or right side of the current slider value
    if click_position > current_value:
        adjust_completion_by_Medals(1)  # Simulate +1 Medal button
    elif click_position < current_value:
        adjust_completion_by_Medals(-1)  # Simulate -1 Medal button

# Define the switch dictionary for "Medal" and "Star"
terms_switch = {
    "Medal": "Medal",
    "Star": "Star"
}

# Store the current selection (start with "Medal" by default)
current_term = "Medal"

# Function to toggle between "Medal" and "Star" and update button labels
def toggle_term(selected_term):
    global current_term
    current_term = terms_switch[selected_term]  # Update the current term globally using the selected term
    update_button_labels()  # Update button text based on the selected term

    # Get the current game's notes and dynamically replace terms
    selected_game = game_combobox.get()
    if selected_game in games:
        _, _, _, _, notes = games[selected_game]
        notes = get_dynamic_notes(notes)  # Pass the current notes to get_dynamic_notes function
    calculate_results()  # Recalculate results to reflect the new term

def get_dynamic_notes(notes):
    # Replace "Medals" with the selected term dynamically in the notes
    return notes.replace("Medal", current_term)

# Function to update button labels dynamically based on the selected term
def update_button_labels():
    adjust_label.config(text=f"Adjust Completion by {current_term}:")
    add_1_button.config(text=f"+1 {current_term}")
    add_2_button.config(text=f"+2 {current_term}s")
    add_3_button.config(text=f"+3 {current_term}s")
    subtract_1_button.config(text=f"-3 {current_term}s")
    subtract_2_button.config(text=f"-2 {current_term}s")
    subtract_3_button.config(text=f"-1 {current_term}")

# Function to calculate the results based on the selected game and completion rate
def calculate_results():
    try:
        selected_game = game_combobox.get()
        completion_rate = float(completion_entry.get()) / 100  # Convert percentage to decimal
    except ValueError:
        results_label.config(text="Invalid completion rate")
        return

    # Handle the custom mod pack separately to allow edits
    if selected_game == "Custom Mod Pack":
        try:
            # Update custom mod values from user input
            custom_mod_values["ClassCount"] = int(class_count_entry.get())
            custom_mod_values["Difficulties"] = int(difficulties_entry.get())
            custom_mod_values["Missions"] = int(missions_entry.get())
            custom_mod_values["NoLimits"] = float(no_limits_entry.get())  # Use the updated NoLimits entry
        except ValueError:
            results_label.config(text="Invalid custom mod values")
            return

        # Use the custom mod values for calculation
        ClassCount = custom_mod_values["ClassCount"]
        Difficulties = custom_mod_values["Difficulties"]
        Missions = custom_mod_values["Missions"]
        NoLimits = custom_mod_values["NoLimits"]
        notes = "Custom mod pack: edit Class Count, Difficulties, Missions, NoLimits."
    else:
        if selected_game in games:
            ClassCount, Difficulties, Missions, NoLimits, notes = games[selected_game]
            notes = get_dynamic_notes(notes)
        else:
            results_label.config(text="Game not found")
            return

    # Step 1: Calculate TotalMedals
    TotalMedals = ClassCount * Difficulties * Missions

    # Step 2: Calculate Fraction
    Fraction = 100 / TotalMedals

    # Step 3: Calculate UserTermCount (based on Medal or Star)
    UserTermCount = round(completion_rate * TotalMedals)

    # Step 4: Adjusted NoLimits Calculation for Custom Mod Pack
    NoLimitsTermCount = round(NoLimits * TotalMedals)  # Custom-modified NoLimits count

    # Step 5: Calculate terms needed to reach NoLimits and Completion
    CountNoLimitsTermCount = max(0, NoLimitsTermCount - UserTermCount)  # Medals remaining to reach NoLimits
    CountCompleteTermCount = max(0, TotalMedals - UserTermCount)

    # Step 6: Calculate static values for terms left to NoLimits and Completion
    EasyToHardTotalTerms = round(0.60 * (ClassCount * Difficulties * Missions))

    staticTermsLefttoNoLimit = max(0, NoLimitsTermCount - EasyToHardTotalTerms)
    staticTermsLefttoCompletion = max(0, TotalMedals - NoLimitsTermCount)

    # Additional info for the next closest milestone in `Medals till x% achievement`
    target_percentages = [5, 10, 15, 20, 25, 30, 35, 40, 45, 50, 55, 60, 62, 64, 66, 68, 70, 72, 74, 76, 78, 80, 82, 84, 86, 88, 90, 92, 94, 96, 98, 100]
    closest_milestone = None

    for percent in target_percentages:
        medals_needed = round((percent / 100) * TotalMedals) - UserTermCount
        if medals_needed > 0:  # Find the first non-zero positive `Medals` needed
            closest_milestone = (percent, medals_needed)
            break

    # Format additional_info to show only the closest milestone
    if closest_milestone:
        additional_info = f"""
        Medals needed to reach {closest_milestone[0]}% achievement: {closest_milestone[1]} {current_term}s
        """
    else:
        additional_info = "You have achieved all listed milestones!"

    if "`Hard` diff can give you `Normal` & `Easy`" in notes or selected_game == "Custom Mod Pack":
        additional_info += f"""
        Easy to Hard Total {current_term}s for all classes: {EasyToHardTotalTerms}
        {current_term}s Left From {EasyToHardTotalTerms} To {int(NoLimits * 100)}%: {staticTermsLefttoNoLimit}
        {current_term}s Left From {int(NoLimits * 100)}% To 100%: {staticTermsLefttoCompletion}
        """

    # Display results in the label
    results = f"""
    Results for {selected_game}:
    Fraction Growth : {Fraction:.11f}
    User {current_term} Count: {UserTermCount}
    {additional_info}
    No Limits {current_term} Count: {NoLimitsTermCount}
    {current_term}s OR Hardest & Inferno Missions Left To {int(NoLimits * 100)}%: {CountNoLimitsTermCount}
    
    100% Total {current_term}s: {TotalMedals}
    {current_term}s OR Hardest & Inferno Missions Left To 100%: {CountCompleteTermCount}
    """
    results += f"\nNotes: {notes}"
    results_label.config(text=results)

def launch_progress_tracker():
    root.title(f"Progress Tracker " + get_version())

    def on_closing():
        save_progress_on_close()
        root.quit()  # Only destroy after the progress is saved

    # Create a dropdown to select between "Medal" and "Star"
    term_label = ttk.Label(root, text="Select Term:")
    term_label.grid(column=0, row=0, padx=10, pady=5, sticky="ew")

    term_combobox = ttk.Combobox(root, values=list(terms_switch.keys()), width=10)
    term_combobox.grid(column=1, row=0, padx=10, pady=5, sticky="ew")
    term_combobox.current(0)  # Default selection is "Medal"
    term_combobox.bind("<<ComboboxSelected>>", lambda event: toggle_term(term_combobox.get()))  # Update term based on user selection

    # Game selection with increased width and calculate on change
    game_label = ttk.Label(root, text="Select Game:")
    game_label.grid(column=0, row=1, padx=10, pady=5, sticky="ew")

    global game_combobox
    game_combobox = ttk.Combobox(root, values=list(games.keys()), width=30)
    game_combobox.grid(column=1, row=1, padx=10, pady=5, sticky="ew")
    game_combobox.current(0)  # Set the default selection to the first game
    game_combobox.bind("<<ComboboxSelected>>", on_game_selection_change)

    # Completion rate input
    completion_label = ttk.Label(root, text="Enter Online Completion Rate (%):")
    completion_label.grid(column=0, row=2, padx=10, pady=5, sticky="ew")

    global completion_entry
    completion_entry = ttk.Entry(root)
    completion_entry.grid(column=1, row=2, padx=10, pady=5, sticky="ew")
    completion_entry.insert(0, "0.00")  # Default value
    completion_entry.bind("<KeyRelease>", update_completion_slider)

    # Function to initialize the slider with the value from completion_entry
    def StartPercent():
        try:
            entry_value = float(completion_entry.get())  # Get the value from the entry field
            completion_slider.set(entry_value)  # Set the slider to match the entry field
        except ValueError:
            completion_slider.set(0)  # If there's an invalid entry, default to 0

    # Slider for completion rate with increased length
    global completion_slider
    completion_slider = tk.Scale(root, from_=0, to=100, orient="horizontal", resolution=0.01, tickinterval=5, command=update_completion_entry, length=400)
    completion_slider.grid(column=0, row=4, columnspan=2, padx=10, pady=5, sticky="ew")

    # Bind the mouse click event to the slider to simulate +1 or -1 Medal buttons
    completion_slider.bind("<Button-1>", on_slider_click)

    # Custom Mod Pack fields (hidden by default)
    global class_count_label, class_count_entry, difficulties_label, difficulties_entry, missions_label, missions_entry, no_limits_label, no_limits_entry
    class_count_label = ttk.Label(root, text="Class Count:")
    class_count_label.grid(column=0, row=5, padx=10, pady=5, sticky="w")
    class_count_entry = ttk.Entry(root)
    class_count_entry.grid(column=1, row=5, padx=10, pady=5, sticky="ew")
    class_count_entry.insert(0, "4")

    difficulties_label = ttk.Label(root, text="Difficulties:")
    difficulties_label.grid(column=0, row=6, padx=10, pady=5, sticky="w")
    difficulties_entry = ttk.Entry(root)
    difficulties_entry.grid(column=1, row=6, padx=10, pady=5, sticky="ew")
    difficulties_entry.insert(0, "5")

    missions_label = ttk.Label(root, text="Missions:")
    missions_label.grid(column=0, row=7, padx=10, pady=5, sticky="w")
    missions_entry = ttk.Entry(root)
    missions_entry.grid(column=1, row=7, padx=10, pady=5, sticky="ew")
    missions_entry.insert(0, "100")

    no_limits_label = ttk.Label(root, text="No Limits:")
    no_limits_label.grid(column=0, row=8, padx=10, pady=5, sticky="w")
    no_limits_entry = ttk.Entry(root)
    no_limits_entry.grid(column=1, row=8, padx=10, pady=5, sticky="ew")
    no_limits_entry.insert(0, "0.70")

    # Button to adjust completion by Medals
    adjust_frame = ttk.Frame(root)
    adjust_frame.grid(column=0, row=3, columnspan=2, padx=10, pady=5, sticky="ew")

    global adjust_label, add_1_button, add_2_button, add_3_button, subtract_1_button, subtract_2_button, subtract_3_button
    adjust_label = ttk.Label(adjust_frame, text=f"Adjust Completion by {current_term}:")
    adjust_label.grid(column=0, row=0, columnspan=6, padx=5, pady=5, sticky="w")

    # Add buttons
    add_1_button = ttk.Button(adjust_frame, text=f"+1 {current_term}", command=lambda: adjust_completion_by_Medals(1))
    add_1_button.grid(column=0, row=1, padx=5, pady=5, sticky="ew")
    add_2_button = ttk.Button(adjust_frame, text=f"+2 {current_term}s", command=lambda: adjust_completion_by_Medals(2))
    add_2_button.grid(column=1, row=1, padx=5, pady=5, sticky="ew")
    add_3_button = ttk.Button(adjust_frame, text=f"+3 {current_term}s", command=lambda: adjust_completion_by_Medals(3))
    add_3_button.grid(column=2, row=1, padx=5, pady=5, sticky="ew")

    # Subtract buttons
    subtract_1_button = ttk.Button(adjust_frame, text=f"-3 {current_term}s", command=lambda: adjust_completion_by_Medals(-3))
    subtract_1_button.grid(column=3, row=1, padx=5, pady=5, sticky="ew")
    subtract_2_button = ttk.Button(adjust_frame, text=f"-2 {current_term}s", command=lambda: adjust_completion_by_Medals(-2))
    subtract_2_button.grid(column=4, row=1, padx=5, pady=5, sticky="ew")
    subtract_3_button = ttk.Button(adjust_frame, text=f"-1 {current_term}", command=lambda: adjust_completion_by_Medals(-1))
    subtract_3_button.grid(column=5, row=1, padx=5, pady=5, sticky="ew")

    # Button to trigger calculation
    calculate_button = ttk.Button(root, text="Calculate", command=calculate_results)
    calculate_button.grid(column=0, row=9, columnspan=2, padx=10, pady=10, sticky="ew")

    # Update Results Label
    global results_label
    results_label = ttk.Label(root, text="", justify="center", anchor="center", wraplength=500, width=70)
    results_label.grid(column=0, row=10, columnspan=2, padx=10, pady=10, sticky="ew")

    # Initially set the button labels
    #debug_tk_instances()
    update_button_labels()
    toggle_custom_settings()
    StartPercent()

    # Call load_progress when the tracker is launched
    load_individual_game_progress(game_combobox.get())  # Load progress for the initially selected game

    # Load progress for the last game played
    last_game = load_last_game()
    game_combobox.set(last_game)
    load_individual_game_progress(last_game)
    toggle_custom_settings()

    root.protocol("WM_DELETE_WINDOW", on_closing)

# Main execution
if __name__ == "__main__":
    initialize_settings(os.getcwd())
    root = tk.Tk()  # Initialize the Tk instance
    launch_progress_tracker()  # Launch the Progress tracker GUI
    root.mainloop()  # Start the Tkinter main event loop
