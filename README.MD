# Hi Welcome To The EDF MML

[Quick Start Guide for EDF 6 Modding](#quick-start-guide-for-edf-6-modding)
[Overview on Mod_config_data.json](#overview-on-mod_config_data.json)
[Glossary](#glossary)
[Top Row Buttons](#top-row-buttons)
[Main Section](#main-section)
[Credits Section](#credits-section)
[Miscellaneous](#miscellaneous)
[GITHUB_INFO Block](#github_info-block)
[DataReplacementTable Block](#datareplacementtable-block)
[NewToAddTextTableEntries Block](#newtoaddtexttableentries-block)
[NewToAddModeList Block](#newtoaddmodelist-block)
[NewToAddSoldierWeaponCategory Block](#newtoaddsolderweaponcategory-block)
[NewToAddWeaponCatalog-(classes) Block](#newtoaddweaponcatalog-classes-block)
[NewToAddWeaponTables Block](#newtoaddweapontables-block)
[DirManifestToFilesUninstaller](#dirmanifesttofilesuninstaller)

## Quick Start Guide for EDF 6 Modding

Welcome to Earth Defense Force 6 modding! This guide will help you get started with creating your first mod configuration file.

1. **Set up your development environment**:
   - Install the latest version of the B.A Mod loader.
   - Familiarize yourself with JSON formatting.

2. **modifying your mod configuration file**:
   - Navigate to the mods folder: `EARTH DEFENSE FORCE 6\Mods\EDF 6 MOD SETTINGS MAKER\MOD CONFIG DATA PLACED HERE`
   - Use the file named `Mod_config_data.json` and rename it `<YourModName>Mod_config_data.json`
   - Start with editing the basic structure within:

## Overview on Mod_config_data.json
    {
        "GITHUB_INFO": [], // GITHUB LINK DOWNLOAD, CAN BE "NEXUS_INFO", Contains metadata about the mod, including author, name, download link, version, and notes. 
        "DataReplacementTable": [], // Used for finding and replacing specific strings in JSON files, typically for localization changes.
        OR patch existing content.
        "NewToAddTextTableEntries": {}, // Adds new text entries across all supported language files.
        "NewToAddModeList": [], // Defines new game modes or mission packs. NOT WORKING YET, MISSING Advanced Patch to bypass limitations
        "NewToAddSoldierWeaponCategory": [], // Defines new weapon categories for different soldier classes.
        "NewToAddWeaponCatalog-Ranger": [], // Specifies weapon slots available for each soldier class.
        "NewToAddWeaponCatalog-WingDiver": [], // ^^^^^^
        "NewToAddWeaponCatalog-AirRaider": [], // ^^^^^^
        "NewToAddWeaponCatalog-Fencer": [], // ^^^^^^
        "NewToAddWeaponTables": {}, // Organizes weapons for each soldier class.
        "DirManifestToFilesUninstaller": {}, // Made with a Tool `ManifestMAKER.exe` that is in the renamed `mymodfolder\Mods` when you package
        your mod to public you still need to double check the files
        "CHANGELOG": [] // Tracks changes between mod versions.
    }
    

## Glossary

- **Modder**: An individual who creates modifications (mods) for the Earth Defense Force games.
- **SGO File**: A proprietary file format used by the game for storing various types of data.
- **Weapon Category ID**: A unique integer identifier for weapon categories defined in the `NewToAddSoldierWeaponCategory` block.
- **PTR (Pointer)**: A type used in JSON structures to indicate a pointer to another structure or list.
- **Locale**: Refers to language-specific versions of text and assets in the game (e.g., CN for Chinese, EN for English).

## Top Row Buttons:
- ### Check for Update:
This button checks for any updates to the B.A Mod loader, ensuring you're always using the latest version.
- ### Update Mods:
This feature allows you to update the installed mods to their latest versions.
- ### Build Tables:
This button compiles the necessary tables for modding the gameplay, making sure everything is set up correctly.
- ### Repair Tables:
This option resets the tables to their default settings, useful if you need to revert any changes or fix issues.
- ### Uninstall a Mod:
This function uninstalls all files connected to the selected mod, keeping your game clean and organized.
- ### Get Into Modding:
Opens the modding wiki, providing valuable resources and guides for those looking to customize their gameplay experience.
## Main Section:
- ### EDF! Game to Launch:
This section allows you to launch different versions of the Earth Defense Force game directly from the mod loader.
  - EARTH DEFENSE FORCE 4.1
  - EARTH DEFENSE FORCE 5
  - EARTH DEFENSE FORCE 6
- ### Open Save Folders:
Quickly access the save folders for the different game versions, making it easy to manage your game data. Buttons below indicate the corresponding versions 
  - 4.1, 5, 6.
- ### Modloader Status:
Enabled: Indicates that the winmm.dll mod loader is currently active.
Toggle Modloader Status: A button to easily enable or disable the winmm.dll mod loader as needed.
- ### Error Section:
Error Block: Displays any errors or logs that occur during the modding process.
Clear Error Block: Clears the displayed text or errors, allowing you to manage the logs effectively.
- ### Mod, Patch, and Plugin Details:
#### These indicators show how many mods, patches, and plugins are currently active.
Mods: as *Mod_confog_data.json at

    EARTH DEFENSE FORCE 6\Mods\EDF 6 MOD SETTINGS MAKER\MOD CONFIG DATA PLACED HERE\*YourModName*Mod_config_data.json
Patches: as .txt 

    EARTH DEFENSE FORCE 6\Mods\Patches\(PatchName).txt
Plugins: as .dll advanced external funtions 

    EARTH DEFENSE FORCE 6\Mods\Plugins\
# Credits Section:
## Credits to the Developers: Acknowledges the creators behind the mod loader, GUI, special game patching.
### - BlueAmulet (Modloader)
### - FevGrave (GUI + Table Generator, Background images)
### - MoistGoat(Advanced MissionPack Settings)
## Miscellaneous:
Toggle Disabled Games Mode: Toggles a mode that likely disables certain game features.
FevGrave, X, Reddit: Direct links to specific user profiles or communities (X refers to the social media platform previously known as Twitter).
and one button to open the github source code
Official EDF Channels:
EDF Official EN on X
EDF Official JP on X
EDF on Reddit
EDF Discord
These buttons provide easy access to official Earth Defense Force channels on social media and community platforms.

# What's in the Mod_config_data.json

## GITHUB_INFO Block

The `GITHUB_INFO` block is used to store metadata about the mod, including the mod name, download link, version, and any additional notes.

### Fields:
- **AUTHOR:** Your Username

- **MOD NAME:** The name of the mod.

- **LINK:** The direct download link for the mod. This link should always point to the latest version.

- **VERSION:** The current version of the mod. **Important:** Ensure that this version number is always updated to reflect the latest release. This is crucial for the auto-download function, as it may soft lock if it attempts to download an outdated version.

- **Notes:** Any additional notes related to the mod. dont use as a `CHANGELOG` there is a block for that at the very bottom

### Example:
    {
        "AUTHOR": "FevGrave",
        "MOD NAME": "EDF_6-1",
        "LINK": "https://github.com/FevGrave/EDF_6-1/archive/refs/heads/main.zip",
        "VERSION": "0.0.1", // Update this field with the latest version to avoid download issues
        "Notes": "TODO / Conflicts"
    }

### Important Note:

Always update the VERSION field whenever a new version of the mod is released. Failure to do so may cause the auto-download function to soft lock if it tries to download an current "outdated" version.

## DataReplacementTable Block

The `DataReplacementTable` block is used to find and replace specific strings in the specified JSON files. This section is essential for modifying text within the game's localization files and other related configurations.

### Applicable Files:

Modders should focus on editing the following files:

- `ImportDefaultData.json`

- `ImportTextTable-CN.json`

- `ImportTextTable-EN.json`

- `ImportTextTable-JA.json`

- `ImportTextTable-KR.json`

- `ImportTextTable-SC.json`

- `ImportWeaponTable.json`

- `ImportWeaponTextTable-CN.json`

- `ImportWeaponTextTable-EN.json`

- `ImportWeaponTextTable-JA.json`

- `ImportWeaponTextTable-KR.json`

### Fields:

- **File:** Specifies which file the replacement should occur in. Must be one of the files listed above.

- **Find:** The exact string value to search for in the specified file.

- **Replace:** The new string that will replace the found text.

### Example:

    {
      "File": "ImportTextTable-EN.json",
      "Find": {
      "value": "A standard room.\nStandard rooms are displayed in the lobby for everyone to join."
      },
        "Replace": {
        "value": "Modded hosting in public lobbies is not recommended due to the potential for instability and unexpected behavior..."
        }
      },
      {
        "File": "ImportTextTable-EN.json",
        "Find": {
        "value": "Passcode Only"
      },
        "Replace": {
        "value": "Change Me"
      }
    }

### Important Considerations:

Only the files listed under "Applicable Files" should be edited.

Ensure that the Find value matches exactly, including any special characters like newline characters (\n), to avoid unintended changes.

This block is mainly used for patching localization and small text updates, making it a powerful tool for maintaining consistency across different language versions.

### Use Cases:

This section is ideal for modifying in-game text across different languages for making specific text-based updates without altering the core functionality of the game.

   

## NewToAddTextTableEntries Block


The `NewToAddTextTableEntries` block is used to add new text entries into all specified localization files. Due to current limitations, entries are added to all supported language files regardless of the specific content or language.


### Applicable Files:
The entries in this block are added into the following five files:
- | `File Format Installed And Used` | `Starting File To Use` |
- | `TEXTTABLE_STEAM.CN.TXT_SGO` | `ImportTextTable-CN.json` (Traditional Chinese) |
- | `TEXTTABLE_STEAM.EN.TXT_SGO` | `ImportTextTable-EN.json` (English) |
- | `TEXTTABLE_STEAM.KR.TXT_SGO` | `ImportTextTable-KR.json` (Korean) |
- | `TEXTTABLE_STEAM.JA.TXT_SGO` | `ImportTextTable-JA.json` (Japanese) |
- | `TEXTTABLE_STEAM.SC.TXT_SGO` | `ImportTextTable-CS.json` (Simplified Chinese) |

### Fields:

    "NewToAddTextTableEntries": {
        "CN": [
            {"name":"Test_Scenario_F", "type":"string", "value":"离线改装任务模式"},
        ],
        "EN": [
            {"name":"Test_Scenario_F", "type":"string", "value":"Offline MODDED Mission Mode"},
        ],
        "JA": [
            {"name":"Test_Scenario_F", "type":"string", "value":"オフライン改造ミッションモード"},
        ],
        "KR": [
            {"name":"Test_Scenario_F", "type":"string", "value":"오프라인 모드 미션 모드"},
        ],
        "SC": [
            {"name":"Test_Scenario_F", "type":"string", "value":"离线�����装任务模式"},
        ]
    },

- **2 Letter Lang**

    - **name:** The identifier for the new text entry. **Important:** Do not use `"GameMode"` or `"MissionPack##"` (# as numbers)for your 2 or more Missionpack Labels as the `name` value, as these are reserved for special UI setups and could cause UI conflicts.

    - **type:** ALWAYS set to `"string"` for text entries.

    - **value:** The actual text string that will be added to the specified localization files.


### Connections to Other Blocks:
- The `name` and `value` fields in `NewToAddTextTableEntries` are also connected to:
  - **`NewToAddModeList`:** The first two strings in both nodes are directly linked to the entries in [NewToAddTextTableEntries](#newtoaddtexttableentries-block).
  - **[NewToAddSoldierWeaponCategory Block](#newtoaddsolderweaponcategory-block):** The `String` value in this block is tied to the `name` values defined here.



### Important Considerations:

- Ensure that each `name` is unique across the [NewToAddTextTableEntries](#newtoaddtexttableentries-block) to prevent conflicts.

- **Do not** use `"GameMode"` or `"MissionPack##"` as `name` values. These fields are reserved for specific UI configurations and using them can disrupt the game's user interface.

- The `value` should be appropriate for all language files listed above, or modders should be prepared to manually adjust the entries in each file post-import.

### Use Cases:

This block is used to introduce new text elements that are necessary for the mod's functionality. Examples might include new menu options, game modes, or item descriptions that weren't present in the original game.

Below is an example of adding multiple new text entries:

    {
        "name": "WingDiver_Weapon_Slot",
        "type": "string",
        "value": "New Wingdiver Weapon Slot"
    },
    {
        "name": "WingDiver_Weapon_Slot_Support_Slot",
        "type": "string",
        "value": "New Wingdiver Support Slot"
    }

## NewToAddModeList Block

The `NewToAddModeList` block is used to define new game modes or mission packs within the game. This block is particularly important for adding custom offline and online mission packs to the game.

### Structure:

The `NewToAddModeList` block typically contains two main nodes:

1. **Offline Mode:** Defines settings and configurations for offline mission packs.

2. **Online Mode:** Defines settings and configurations for online mission packs.

### Fields:

- **type:** Generally set to `"ptr"` to indicate a pointer to another structure or list.

- **value:** This is an array that contains various pointers and configurations, including references to text entries, background music, game settings, and mission lists.

### Offline Mode (First Block) Online Mode (Second Block):

These blocks define the settings for an offline and online mission pack.

### Example of one block:
    {
        "type": "ptr",
        "value": [
            {"type": "string", "value": "Test_Scenario_F"},
            {"type": "string", "value": "Test_Scenario_Desc_F"},
            {"type": "string", "value": "off_scenario.%LOCALE%.dds"},
            {"type": "string", "value": "BGM_E5S02_EDFHonbu"},
            {"type": "string", "value": "MAIN.GST"},
            {"type": "string", "value": "MODTEST.MST"},
            {
                "type": "ptr",
                "value": [
                    {"type": "string", "value": "app:/Mission/YOUR_MissionList.offline.list.sgo"},
                    {"type": "string", "value": "app:/Mission/YOUR_MissionList.offline.txt.%LOCALE%.sgo"},
                    {"type": "string", "value": "app:/Mission/YOUR_MissionList.offline.image.rab"}
                ]
            },
            {
                "type": "ptr",
                "value": [
                    {
                        "type": "ptr",
                        "value": [
                            {
                                "type": "ptr",
                                "value": [
                                    {{{missionDifficultyScale}}}
                                ]
                            },
                            {
                                "type": "ptr",
                                "value": [
                                    {{{PlayerCountDiffScale}}}
                                ]
                            },
                            {
                                "type": "ptr",
                                "value": [
                                    {{{WeaponDrops}}}
                                ]
                            },
                            {
                                "type": "ptr",
                                "value": [
                                    {{{OnlineCorrection}}}
                                ]
                            },
                            {
                                "type": "ptr",
                                "value": [
                                    {{{InfantryCorrection}}}
                                ]
                            },
                            {
                                "type": "ptr",
                                "value": [
                                    {{{VehicleCorrection}}}
                                ]
                            },
                            {
                                "type": "ptr",
                                "value": [
                                    {{{Weapon Limit}}}
                                ]
                            },
                            {
                                "type": "ptr",
                                "value": [
                                    {{{Online Armor Limit}}}
                                ]
                            }
                        ]
                    },
                    {
                        Repeat the block above 4 more times to set Normal, Hard, Hardest, Inferno difficulties
                    }
                ]
            },
            {{{Miscellaneous}}}
            {
                "type": "ptr",
                "value": [
                    {{{LocalPlayerCount}}}
                ]
            }
        ]
    }

### Connections to Other Blocks:
- This block is connected to `NewToAddTextTableEntries`, which provides the text entries for the mode names and descriptions.
- See [NewToAddTextTableEntries](#newtoaddtexttableentries-block) for details on adding new text entries.
- The `missionDifficultyScale`, `PlayerCountDiffScale`, and other variables used in this block are typically defined in the game's core files. Modders should be cautious when modifying these values.

  

## NewToAddSoldierWeaponCategory Block


The `NewToAddSoldierWeaponCategory` block is used to define new weapon categories for different soldier classes in the game. This block is essential for expanding the range of weapons available to different classes, allowing for greater customization and variety in gameplay.

### Structure:

Each entry in this block typically contains two main components:

1. **Weapon Category ID:** A unique integer that identifies the weapon category.

2. **Weapon Slot Name:** A string that represents the name of the weapon slot associated with that category.

### Fields:

- **type:** Generally set to `"ptr"` to indicate a pointer to another structure.

- **value:** This is an array containing the following:

- **Weapon Category ID:** An integer value that uniquely identifies the weapon category. that corresponds to the `NewToAddWeaponTables` when making a new gun or item to use

- **Weapon Slot Name:** A string value that corresponds to the name of the weapon slot. This value will need to match the "name" entry in the `NewToAddTextTableEntries` block.

### Example:

    {
        "type": "ptr",
        "value": [
            {"type": "int", "value": 10000},
            {"type": "string", "value": "Ranger_Weapon_Slot"}
        ]
    },
    {
        "type": "ptr",
        "value": [
            {"type": "int", "value": 15001},
            {"type": "string", "value": "Ranger_Weapon_Slot_Support_Slot"}
        ]
    },
    {
        "type": "ptr",
        "value": [
            {"type": "int", "value": 20000},
            {"type": "string", "value": "WingDiver_Weapon_Slot"}
        ]
    }

### Connections to Other Blocks:
- This block is directly linked to `NewToAddTextTableEntries`, where you define the names of the weapon slots.
- See [NewToAddTextTableEntries](#newtoaddtexttableentries-block) for instructions on adding new text entries for weapon slot names.
- The Weapon Category IDs defined here correspond to the categories in `NewToAddWeaponTables`.


### Important Considerations:

Ensure that each Weapon Category ID is unique across the `NewToAddSoldierWeaponCategory` block to prevent conflicts.

The Weapon Slot Name should be appropriately defined in the `NewToAddTextTableEntries` block to ensure proper UI representation.

Proper linkage with the `NewToAddWeaponCatalog-(classes)` block is crucial to ensure the new weapon categories are accessible in the appropriate menus.

### Use Cases:

This block is used to introduce new weapon categories for different soldier classes, such as the Ranger, Wing Diver, Air Raider, and Fencer. By defining new categories, modders can add custom weapons to the game that fit into these new slots and appear correctly in the soldier classes' weapon selection menus.

  

## NewToAddWeaponCatalog-(classes) Block

The `NewToAddWeaponCatalog-(classes)` block is used to specify the weapon slots available for each soldier class in the game. This block directly connects the weapon categories defined in the `NewToAddSoldierWeaponCategory` block to the specific slots that will appear in the game’s weapon selection menu for each class.

### Connections to Other Blocks:
- This block is directly linked to `NewToAddSoldierWeaponCategory`, where you define the weapon categories.
- See [NewToAddSoldierWeaponCategory](#newtoaddsoldierweaponcategory-block) for details on defining new weapon categories.
- The Weapon Category IDs used here should match those defined in `NewToAddSoldierWeaponCategory`.

- The filler information in this block helps organize weapons according to the categories defined in `NewToAddSoldierWeaponCategory`.
### Structure:

Each soldier class has its own block, where the weapon slots are defined:

- **Ranger**

- **WingDiver**

- **AirRaider**

- **Fencer**

Each entry within these blocks defines the weapon slot and the corresponding category ID or IDs.

### Fields:

- **Weapon Slot:** The name of the slot as it appears in the game menu.

- **value:** An array containing one or more `Weapon Category ID` values that link to the weapon categories defined in the `NewToAddSoldierWeaponCategory` block.

### Adding Multiple Categories to a Slot:

You can add multiple weapon categories to a single slot by including more than one `Weapon Category ID` in the `value` array. This allows a single slot to support multiple weapon categories, providing greater flexibility and customization.

### Example for Ranger:

    "NewToAddWeaponCatalog-Ranger": [
        {"Weapon_Slot1": {"value": [{"type": "int", "value": 10000}, {"type": "int", "value": 10001}]}},
        {"Weapon_Slot2": {"value": [{"type": "int", "value": 10000}]}},
        {"Weapon_SlotSupport2": {"value": [{"type": "int", "value": 15001}]}},
        {"Weapon_SlotSupport1": {"value": [{"type": "int", "value": 15001}]}}
    ]

### Explanation:

Weapon_Slot1: This slot now supports two weapon categories, 10000 and 10001. This means that both categories will be available for selection in this slot.

Weapon_Slot2: This slot supports only one category, 10000.

Weapon_SlotSupport1 & Weapon_SlotSupport2: These slots each support the category 15001.


### Soldier Classes:

Ranger:

Weapon_Slot1: Supports multiple categories (10000, 10001), allowing greater flexibility in weapon selection.

Weapon_Slot2: Supports a single category (10000).

Weapon_SlotSupport1 & Weapon_SlotSupport2: Support a single category (15001).

WingDiver, AirRaider, and Fencer: Follow a similar structure where multiple categories can be added to each slot by including additional Weapon Category ID values in the value array.

### Connections to Other Blocks:
- This block is connected to `NewToAddSoldierWeaponCategory`, which defines the weapon categories.
- See [NewToAddSoldierWeaponCategory](#newtoaddsolderweaponcategory-block) for instructions on adding new weapon categories.
- The filler information in this block helps organize weapons according to the categories defined in [NewToAddSoldierWeaponCategory Block](#newtoaddsolderweaponcategory-block).

Proper configuration of this block ensures that the new weapon slots show up correctly in the game menus, allowing players to access and equip the new weapons added by the mod.

### Important Considerations:

Ensure that the Weapon Slot names are correctly defined and linked to the appropriate category IDs.

The Weapon Category ID should match the ID used in the NewToAddSoldierWeaponCategory block to prevent any issues with weapon selection in the game.

When adding multiple categories to a single slot, ensure that the slot is capable of supporting all intended categories to avoid potential conflicts or UI issues.

### Use Cases:

This block is used to organize and display the new weapon categories within the soldier classes' weapon selection menus. By correctly configuring this block, modders can control where and how new weapons appear in the game, ensuring that the player has easy access to the new content.

  

### NewToAddWeaponTables Block

### Purpose of Filler Information:
The empty arrays within each category (e.g., "Assault Rifles": []) are placeholders intended to help modders organize weapons. These placeholders allow modders to categorize and structure the weapons they're adding, ensuring what they have made will be appended to the end of the game's Weapon Tables.

### Structure:

The block is divided by soldier classes, with each class having its own set of weapon categories:

- **RANGER**

- **WINGDIVER**

- **FENCER**

- **AIRRAIDER**

### Fields:

Each soldier class contains a list of weapon categories. These categories are initially filled with placeholders (filler info) to help modders like you to organize the weapons. These categories will be appended at the end of the existing lists.

### Example Structure:
    "NewToAddWeaponTables": {
        "RANGER": {
            "Assault Rifles": [],
            "Shotguns": [],
            "Snipers": [],
            "Rocket Launchers": [],
            "Missile Launchers": [],
            "Grenades": [],
            "Special": [],
            "Support Equipment": [],
            "Bikes": [],
            "Tanks": [],
            "Helicopters": [],
            "New Ranger Weapon Slot": [],
            "New Ranger Support Slot": []
        },
        "WINGDIVER": {
            "Short-Range": [],
            "Mid-Range Kinetic Weapons": [],
            "Mid-Range Pulse Weapons": [],
            "Mid-Range Energy Weapons": [],
            "Long-Range": [],
            "Ranged Weapons": [],
            "Homing Weapons": [],
            "Special": [],
            "Plasma Cores": [],
            "New Wingdiver Weapon Slot": [],
            "New Wingdiver Support Slot": []
        },
        "FENCER": {
            "CC Strikers": [],
            "CC Piercers": [],
            "Shields": [],
            "Autocannons": [],
            "Cannons": [],
            "Missile Launchers": [],
            "Enhanced Boosters": [],
            "Enhanced Shields": [],
            "Enhanced Cannons": [],
            "Enhanced Exoskeletons": [],
            "New Fencer Weapon Slot": [],
            "New Fencer Support Slot": []
        },
        "AIRRAIDER": {
            "Request Artillery Units": [],
            "Request Gunships": [],
            "Request Bombers": [],
            "Request Missiles": [],
            "Request Satellites": [],
            "Limpet Guns": [],
            "Stationary Weapons": [],
            "Support Equipment": [],
            "Special": [],
            "Powered Exoskeletons": [],
            "Special Weapons": [],
            "Helicopters": [],
            "Ground Vehicles": [],
            "Tanks": [],
            "New AirRaider Weapon Slot": [],
            "New AirRaider Support Slot": []
        }
    }

### Purpose of Filler Information:

The empty arrays within each category (e.g., "Assault Rifles": []) are placeholders intended to help YOU the modder(s) organize the weapons. These placeholders allow you to categorize and structure the weapons you’re adding, ensuring what you have made, They will be appended to the end of the games Weapon Tables

### Required Structure:

In addition to the filler information, each entry must include the following required skeleton structure:

    {
        "Name": "",
        "Data": {},
        "Text": {}
    }

### Explanation:

Name: This field is not used by the game but serves as a marker to help modders understand what the blocks represent.

Data: This block should contain the actual weapon data to be added, Will be appended to the WEAPONTABLE.SGO

Text: This block should contain any text related to the weapon, such as descriptions, though it may also start as an empty object. It will display the stats of the item within the game's menu

### Important Notes:

Organization: The filler information should be used to help structure the weapon categories. As weapons are added, these placeholders will be replaced or appended with actual data.

Appending: When modders add new weapons, these entries will be appended to the end of the existing lists within the game.

### Use Cases:
This block is essential for categorizing and organizing the various weapons available to each soldier class. By using the filler information and required structure, modders can ensure that new weapons are correctly integrated and displayed within the game.

Below is an example of how a complete entry might look after adding 2 or more new weapons (Second weapon is just a skeleton template):

    {
        "RANGER": {
            "Assault Rifles": [
                {
                    "Name": "Broken PA-11",
                    "Data": {
                        "value": [
                            {"value": "AssultRifle01", "type": "str"},
                            {"value": "app:/weapon/AssultRifle01.sgo", "type": "str"},
                            {"value": 10000, "type": "double"},
                            {"value": 1, "type": "double"},
                            {"value": 0, "type": "double"},
                            {"value": 1, "type": "double"},
                            {"value": 1, "type": "double"},
                            {"value": 1, "type": "double"},
                            {"value": 0, "type": "double"}
                        ],
                        "type": "ptr"
                    },
                    "Text": {
                        "value": [
                            {"value": "Broken PA-11", "type": "str"},
                            {
                                "value": "A broken high-performance assault rifle.\nPerformance of the rifle is greatly reduced due to it having been repaired with spare parts.\n\nHolding the trigger (pressing and holding the attack button) will continually fire shots.\nFired bullets are susceptible to air resistance and decrease in power depending on distance.\n\nAt the moment being fire, the bullet's power is the maximum of the spec (Damage  value shown on the right). \nIts power will gradually decrease and become the minimum of the spec (Damage value shown on the right) when reaching its limit of the range.",
                                "type": "str"
                            },
                            {
                                "value": [
                                    {
                                        "value": [
                                            {"value": "Capacity", "type": "str"},
                                            {"value": "$0", "type": "str"},
                                            {
                                                "value": [
                                                    {"value": 120, "type": "double"},
                                                    {"value": 0, "type": "double"},
                                                    {"value": 0, "type": "double"},
                                                    {"value": 7, "type": "double"},
                                                    {"value": 0.5, "type": "double"},
                                                    {"value": 0.5, "type": "double"},
                                                    {"value": 0, "type": "double"}
                                                ],
                                                "type": "ptr"
                                            }
                                        ],
                                        "type": "ptr"
                                    },
                                    {
                                        "value": [
                                            {"value": "ROF", "type": "str"},
                                            {"value": "$0/sec", "type": "str"},
                                            {
                                                "value": [
                                                    {"value": 5, "type": "double"},
                                                    {"value": 25, "type": "double"},
                                                    {"value": 5, "type": "double"},
                                                    {"value": 4, "type": "double"},
                                                    {"value": 0.5, "type": "double"},
                                                    {"value": 0.5, "type": "double"},
                                                    {"value": 0, "type": "double"}
                                                ],
                                                "type": "ptr"
                                            }
                                        ],
                                        "type": "ptr"
                                    },
                                    {
                                        "value": [
                                            {"value": "Damage", "type": "str"},
                                            {"value": "$0～$1", "type": "str"},
                                            {
                                                "value": [
                                                    {"value": 11, "type": "double"},
                                                    {"value": 8, "type": "double"},
                                                    {"value": 1, "type": "double"},
                                                    {"value": 8, "type": "double"},
                                                    {"value": 0.5, "type": "double"},
                                                    {"value": 0.5, "type": "double"},
                                                    {"value": 1, "type": "double"}
                                                ],
                                                "type": "ptr"
                                            },
                                            {
                                                "value": [
                                                    {"value": 5.5, "type": "double"},
                                                    {"value": 8, "type": "double"},
                                                    {"value": 1, "type": "double"},
                                                    {"value": 8, "type": "double"},
                                                    {"value": 0.5, "type": "double"},
                                                    {"value": 0.5, "type": "double"},
                                                    {"value": 1, "type": "double"}
                                                ],
                                                "type": "ptr"
                                            }
                                        ],
                                        "type": "ptr"
                                    },
                                    {
                                        "value": [
                                        {"value": "Reload Time", "type": "str"},
                                        {"value": "$0 sec", "type": "str"},
                                        {
                                            "value": [
                                                {"value": 1.5, "type": "double"},
                                                {"value": 21, "type": "double"},
                                                {"value": 4, "type": "double"},
                                                {"value": 8, "type": "double"},
                                                {"value": 1, "type": "double"},
                                                {"value": 0.5, "type": "double"},
                                                {"value": 1, "type": "double"}
                                            ],
                                            "type": "ptr"
                                            }
                                        ],
                                        "type": "ptr"
                                    },
                                    {
                                        "value": [
                                            {"value": "Range", "type": "str"},
                                            {"value": "$0m", "type": "str"},
                                            {
                                                "value": [
                                                    {"value": 208, "type": "double"},
                                                    {"value": 16, "type": "double"},
                                                    {"value": 3, "type": "double"},
                                                    {"value": 8, "type": "double"},
                                                    {"value": 0.5, "type": "double"},
                                                    {"value": 0.5, "type": "double"},
                                                    {"value": 1, "type": "double"}
                                                ],
                                                "type": "ptr"
                                            }
                                        ],
                                        "type": "ptr"
                                    },
                                    {
                                        "value": [
                                            {"value": "Shot Speed", "type": "str"},
                                            {"value": "$0m/s", "type": "str"},
                                            {
                                                "value": [
                                                    {"value": 240, "type": "double"},
                                                    {"value": 16, "type": "double"},
                                                    {"value": 3, "type": "double"},
                                                    {"value": 8, "type": "double"},
                                                    {"value": 0.5, "type": "double"},
                                                    {"value": 0.5, "type": "double"},
                                                    {"value": 1, "type": "double"}
                                                ],
                                                "type": "ptr"
                                            }
                                        ],
                                        "type": "ptr"
                                    },
                                    {
                                        "value": [
                                            {"value": "Accuracy", "type": "str"},
                                            {"value": "$0", "type": "str"},
                                            {
                                                "value": [
                                                    {"value": 0.05000000074505806, "type": "double"},
                                                    {"value": 13, "type": "double"},
                                                    {"value": 2, "type": "double"},
                                                    {"value": 6, "type": "double"},
                                                    {"value": 2, "type": "double"},
                                                    {"value": 0.5, "type": "double"},
                                                    {"value": 1, "type": "double"}
                                                ],
                                            "type": "ptr"
                                            }
                                        ],
                                        "type": "ptr"
                                    },
                                    {
                                        "value": [
                                            {"value": "Zoom", "type": "str"},
                                            {"value": "----", "type": "str"}
                                        ],
                                        "type": "ptr"
                                    },
                                    {
                                        "value": [
                                            {"value": "Laser Sight", "type": "str"},
                                            {"value": "----", "type": "str"}
                                        ],
                                        "type": "ptr"
                                    }
                                ],
                                "type": "ptr"
                            }
                        ],
                        "type": "ptr"
                    }
                },
                {
                    "Name": "Custom Assault Rifle",
                    "Data": {
                        "// Weapon data goes here"
                    },
                    "Text": {
                        "// Weapon text and descriptions go here"
                    }
                }
            ]
        }
    }

  

## DirManifestToFilesUninstaller

Included in the ~~~mymodfolder\Mods~~~ folder is a ManifestMAKER.exe will write out the dir tree and can write to the *YourModName*Mod_config_data.json
