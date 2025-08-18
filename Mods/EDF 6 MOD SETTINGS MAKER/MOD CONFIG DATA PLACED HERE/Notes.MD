# 📌 EDF MML Documentation: Introduction for Mod_config_data.json
## 🌟 Welcome to Earth Defense Force 6 Modding!
This documentation serves as a comprehensive guide to using EDF MML (Multi-Mod Loader) HAKKEN Core and the Mod_config_data.json (MCD) system for modding Earth Defense Force 6. Whether you are creating new missions, weapons, or localizations, this guide will help you understand the modding pipeline from setup to execution. Your Already [Ready to Get Started With Your MCD](#-ready-to-get-started-with-your-mcd)? WOW

### ❌Disclaimer 
#### 🔹 Intented for you the mod makers to make a "MCD" generating entertainment content for EDF, and not the END USER players who play the mods

#### 🔹 Important Modding Requirements
- This tool requires knowledge of EDF asset modding. This builds on it
- EDF MML merges multiple mods into a structured list, ensuring correct file placement.
- It uses SGOTT (Always Latest) to convert SGO ↔ JSON.

#### 🔹 Not used by these Tools to edit or convert SGO files:
- EDFTools (SGO ↔ XML) Allows MAB data to be read
- DSGO (SGO ↔ JSON) Slightly Different Format

#### 🔹 Need Help? Access the Modding Wiki & Guides!
- Click "Get Into Modding" in the EDF MML UI to access useful resources.

- Covers detailed EDF modding knowledge, including asset modifications, advanced techniques, and full integration methods. 

#### 🔹 Maybe Birb’s Guide to Mod EDF Assets (Beginner-Friendly)

- A starter-oriented guide for learning how to modify EDF assets, perfect for newcomers.
- This ensures both beginners and advanced users have access to the right tools and information for modding EDF 4.1, 5, 6.

### 📂 What’s in This Guide?
- Setup & Basics: The guide includes foundational steps for setting up EDF MML and understanding its integration with the HAKKEN core, specifically focusing on the Mod_config_data.json (MCD) file.

- Mod_config_data.json (MCD) Configuration: Detailed instructions on how to create, format, and use the MCD file, including:

- Naming conventions for Mod_config_data.json.
Placement of the MCD file in the appropriate directory.
Examples of properly formatted JSON structures for different blocks.
Core Modding Sections:

- Patching Content: Explains how to fix game data with DataReplacementTable.
- Text Modifications: How to modify in-game UI text, subtitles, and localizations using NewToAddTextTableEntries and NewToAddSubTitleList.
- Mission Pack Creation: Using NewToAddModeList to add custom mission sets.
- Weapon & Soldier Expansion: Details on creating new weapons and soldier categories through NewToAddSoldierWeaponCategory, NewToAddWeaponCatalog, and NewToAddWeaponTables.
- Mod Cleanup & Uninstallation: Proper use of DirManifestToFilesUninstaller to ensure clean removal of mods.
- New Quality of Life Features: The CATEGORIES block is a recent addition, offering better organization within the Mods Panel. The guide explains:

- How the Mods Panel integrates the categories into a search pool.
The effect on the user interface with category-based filtering.
Important Modding Practices: Best practices such as:

- Always testing mods in "No Installer" mode.
Backing up game files.
Using JSON validators to prevent formatting errors.
New Section Additions: The guide has evolved to include:

- "Connections to Other Blocks": Showing how configuration blocks interact.
- "Source File" and "End Product File" for each block section: Helping modders track data flow from input to final integration.

### 🔹 Core Modding Sections
- 🛠 Patching Content → That Is Deemed Incorrect And Must Be Fixed
- 🛠 Text Modifications → Modify in-game UI text & descriptions
- 🛠 Mission Pack Creation → Add custom mission sets
- 🛠 Weapon & Soldier Expansion → Define new weapons & categories
- 🛠 Mod Cleanup & Uninstallation → Ensure a clean Uninstallation mod process

### 📢 Important Notes for you Mod Makers
- ⚠ Repair Tables Before Modding!
- ⚠ Check JSON Formatting! Use a JSON validator to avoid syntax errors.
- ⚠ Use Unique Identifiers! Prevent text or weapon conflicts in other mods or within the game. If its adding content
- ⚠ Test in No Installer Mode! Use EDF HAKKEN NI.exe for testing before finalizing with EDF HAKKEN.exe.
- ⚠ This cannot combine missions as they are single file .AC with .RMPA AND OR .BVM files. USE .AC & RMPA for online play
- ⚠ This tool set is not for the faint of heart! It requires a good understanding of EDF modding and JSON formatting. If you are new to modding, consider starting with simpler tools or guides before diving into this advanced setup.

## 📌 EDF HAKKEN Core Executables (EDF HAKKEN.exe & EDF HAKKEN NI.exe)
### Double Meaning: Modding and Hardstyle/Gabber Dance (Hakken/Hakka) HUH?
#### Modding Aspect: 
- HAKKEN’s primary role as a highly adaptive, core modding tool for EDF 6 is clear, processing `Mod_config_data.json` to build and integrate modded content seamlessly across the MML ecosystem (e.g., patching content, creating mission packs, expanding weapons, as outlined in your updated sections).
#### Hardstyle/Gabber Dance Aspect: 
- The acronym of this HAKKEN tool ties into the Hakken/Hakka dance styles, known for their energetic, stomping, and rhythmic movements synced to the fast, pounding beats of Hardstyle and Gabber music genres (typically 140–150 BPM or WAYYY higher). "Highly Adaptive" mirrors a dancer’s ability to adapt to rapid tempo changes and intense rhythms, while "Kernel Kit" suggests the foundational beat and moves of the dance. "EDF Network" implies a network of ravers or EDF soldiers moving in unison, defending Earth with the same intensity as a Hardstyle/Gabber dance floor, adding a high-energy, cultural twist that resonates with EDF’s action-packed universe and modding’s dynamic creativity.

### WHAT IS HAKKEN: Highly Adaptive Kernel Kit for the EDF's Network
- **Highly**: Highlights HAKKEN’s exceptional capability and flexibility, emphasizing its ability to adapt to diverse modding needs in EDF 6—such as processing `Mod_config_data.json` for missions, weapons, and text.
- **Adaptive**: Reinforces HAKKEN’s versatility, adjusting seamlessly to mod configurations, game updates, and user inputs (e.g., switching between EDF HAKKEN.exe and EDF HAKKEN NI.exe modes).
- **Kernel**: Positions HAKKEN as the core engine or processing unit, central to building modded tables and generating files like `CONFIG.json` and `WEAPONTEXT.json`.
- **Kit for**: HAKKEN as a comprehensive toolkit for modders, aligning with its executable nature and the "Build Tables" functionality in the MML UI.
- **EDF's**: Maintains the direct link to Earth Defense Force, ensuring specificity to EDF 6 modding and its military/sci-fi theme. E! D! F!
- **Network**: Evokes a broader, interconnected system within EDF 6 modding, connecting modders, players, and game data.

#### 🛠 What Are These Files?
- The HAKKEN Core executables are responsible for building and processing modded tables in EDF MML. They handle mod integration in two different ways:

#### Executable Mode Purpose?
- EDF HAKKEN.exe Installer Mode	Fully integrates mod data into game files for public release.
- EDF HAKKEN NI.exe	No Installer Mode	Used for testing mods without installing the modified core game files, reducing crash risks.

### 🛠 How They Work in MML
- Use input with in the "Request Code: Air Force Drop-Off" felid in the GUI to Switch Modes OR
- User Clicks "Build Tables" in the EDF MML UI.
- Triggers EDF HAKKEN.exe or EDF HAKKEN NI.exe based on the mode.
- Processes Mod_config_data.json and builds the necessary game tables.
- Finalizes mod integration or prepares for testing.

### 🚀 When to Use Each Mode?
#### ✅ Use EDF HAKKEN NI.exe (No Installer Mode) For Testing And Verification Of Edits.

- Does not install the modified game data. and drop the data where the games exe is at.
- Useful for debugging modded content before release.
- Prevents game crashes due to faulty JSON configurations.

#### ✅ Use EDF HAKKEN.exe (Installer Mode) for Final Builds

- Applies changes and installs the modified data into the game’s structure.
- Required for public mod releases.
- Ensures all modded content is properly installed.

#### 🔹 HAKKEN Core (Generating Game Data Files)
- ##### 🔹 Limitations & Tips
    - ⚠ Ensure Mod_config_data.json is properly formatted before running HAKKEN.
    - ⚠ Use NI mode first to test how this add data to the files before using full install mode.
    - ⚠ Some generated files require manual review for accuracy.
    - ⚠ Make backups before running HAKKEN in install mode.

    | Languages             | Two letter lang |
    | :-------------------: | :-------------: |
    | (Traditional Chinese) | CN |
    | (English)             | EN |
    | (Japanese)            | JP |
    | (Korean)              | KR |
    | (Simplified Chinese)  | SC |

- ##### 🔹 Generated Files and EDF common conflict files MML can handel
|     SOURCE STARTING JSON FILE    | FINISHED PRODUCT WITH MODIFICATIONS |           WHAT ARE THEY ?           |
| :------------------------------: | :---------------------------------: | :---------------------------------: |
|==================================|=====================================|=====================================|
| ImportDefaultData.json           | CONFIG.SGO                          |📂 Mission Pack Data
|==================================|=====================================|=====================================|
| ImportSubtitleVoiceTable.CN.json | EDF6_VOICETABLE.CN.SGO              |📂 Subtitle Table Data
| ImportSubtitleVoiceTable.EN.json | EDF6_VOICETABLE.EN.SGO              |  Holds All Text In The Missions     |
| ImportSubtitleVoiceTable.JA.json | EDF6_VOICETABLE.JA.SGO              |                                     |
| ImportSubtitleVoiceTable.KR.json | EDF6_VOICETABLE.KR.SGO              |                                     |
| ImportSubtitleVoiceTable.SC.json | EDF6_VOICETABLE.SC.SGO              |                                     |
|==================================|=====================================|=====================================|
| ImportTextTable-CN.json          | TEXTTABLE_STEAM.CN.TXT_SGO          |📂 GUI Text Tables (Localization)
| ImportTextTable-EN.json          | TEXTTABLE_STEAM.EN.TXT_SGO          |  Holds All Text In The Games UI     |
| ImportTextTable-JA.json          | TEXTTABLE_STEAM.JA.TXT_SGO          |  Translators Of Other Languages     |
| ImportTextTable-KR.json          | TEXTTABLE_STEAM.KR.TXT_SGO          |  Use This File For Your Translation |
| ImportTextTable-SC.json          | TEXTTABLE_STEAM.SC.TXT_SGO          |     (ImportTextTable-EN.json)       |
|==================================|=====================================|=====================================|
| ImportWeaponTable.json           | WEAPONTABLE.SGO                     |📂 Weapon Level, Config Data, Setting to lock gun
|==================================|=====================================|=====================================|
| ImportWeaponTextTable-CN.json    | WEAPONTEXT.CN.SGO                   |📂 Weapon Text Stats (Localization)
| ImportWeaponTextTable-EN.json    | WEAPONTEXT.EN.SGO                   |  Visual Text To Display The Items Stats.
| ImportWeaponTextTable-JA.json    | WEAPONTEXT.JA.SGO                   |                                     |
| ImportWeaponTextTable-KR.json    | WEAPONTEXT.KR.SGO                   |                                     |
| ImportWeaponTextTable-SC.json    | WEAPONTEXT.SC.SGO                   |                                     |
|==================================|=====================================|=====================================|
| P501_PROTO_RANGER.json           | P501_PROTO_RANGER.SGO               | 📂 EDF 5 Civ Skin
| P502_PROTO_WINGDIVER.json        | P502_PROTO_WINGDIVER.SGO            |  Settings for Camera, Grip Offsets  |
| P503_PROTO_FENCER.json           | P503_PROTO_FENCER.SGO               |  "IK" lengths, Spotlight, Color,    |
| P504_PROTO_AIRRADER.json         | P504_PROTO_AIRRAIDER.SGO            |  And many more, Same Applies Bellow |
|==================================|=====================================|=====================================|
| P505_RANGER.json                 | P505_RANGER.SGO                     | 📂 EDF 5 Military Skin
| P506_WINGDIVER.json              | P506_WINGDIVER.SGO                  |                                     |
| P507_FENCER.json                 | P507_FENCER.SGO                     |                                     |
| P508_AIRRADER.json               | P508_AIRRAIDER.SGO                  |                                     |
|==================================|=====================================|=====================================|
| P601_PROTO_RANGER.json           | P601_PROTO_RANGER.SGO               | 📂 EDF 6 Tattered Military Skin
| P602_PROTO_WINGDIVER.json        | P602_PROTO_WINGDIVER.SGO            |                                     |
| P603_PROTO_FENCER.json           | P603_PROTO_FENCER.SGO               |                                     |
| P604_PROTO_AIRRADER.json         | P604_PROTO_AIRRAIDER.SGO            |                                     |
|==================================|=====================================|=====================================|
| P605_RANGER.json                 | P605_RANGER.SGO                     | 📂 EDF 6 Future Military Skin
| P606_WINGDIVER.json              | P606_WINGDIVER.SGO                  |                                     |
| P607_FENCER.json                 | P607_FENCER.SGO                     |                                     |
| P608_AIRRADER.json               | P608_AIRRAIDER.SGO                  |                                     |

### 🛠 How to Switch Modes
    - 1️⃣ In EDF MML, locate the "Request Code: Air Force Drop-Off" text box. 
    - 2️⃣ Type ni → Press Enter → Switches to No Installer Mode.
    - 3️⃣ Type i → Press Enter → Switches to Installer Mode.
    - 4️⃣ The selected mode will be applied when clicking "Build Tables".

### 🚀 Best Practices
    - ✅ Again use ni mode for safe mod testing before finalizing changes.
    - ✅ If everything works in ni, then use i mode to fully install the mod.
    - ✅ Avoid using i mode first unless confident in your mod’s stability.

## 🚀 What is Mod_config_data.json (MCD)?
    - 📌 Mod_config_data.json (MCD) is the configuration file that defines how mods interact with EDF 6. It controls:
    - ✔ Game modifications (text, mission packs, weapons, UI elements)
    - ✔ New content additions (custom missions, weapons, and soldier categories)
    - ✔ File cleanup & uninstall processes

### 🛠 How Does EDF MML Work With This?
    - 1️⃣ Load Mod_config_data.json → Defines the mod structure.
    - 2️⃣ Process with HAKKEN Core Exe's baked from Python Scripts → Reads mod data and builds the edits into the tables.
    - 3️⃣ The HAKKEN  Core installs the Modified Files → Your content is now integrated into EDF 6!
    - 4️⃣ Uninstall System → Mods can be safely removed using DirManifestToFilesUninstaller.

### 🛠 How to Name Your Mod_config_data.json File
- ##### MUST END WITH Mod_config_data.json
- To ensure your mod works correctly, you must rename the Mod_config_data.json file to match your mod's unique name. This helps the mod loader identify and process your mod properly. Use the following format:

#### ✅ Examples of naming your Mod_config_data.json File:
- BUNGUS_Mod_config_data.json
- STRONG_TEAMATES_Mod_config_data.json
- OP_ANIME_WIFUSMod_config_data.json
- Explosive_Human_MinesMod_config_data.json
- HighkrealMod_config_data.json
    ##### This naming convention avoids conflicts with other mods and keeps your files organized. Make sure not to confuse this with renaming a CONFIG.json file, as the Mod_config_data.json is a specific file used for defining mod interactions with EDF 6 with the HAKKEN.EXEs

### 📂 Where to Place Your Mod_config_data.json File

- To place your Mod_config_data.json file correctly, press the Mods button in the EDF MML GUI. This will open the correct folder automatically.

- The exact directory for Steam or Epic installs is:

        <Game Install Directory>\EARTH DEFENSE FORCE 6\Mods\EDF 6 MOD SETTINGS MAKER\MOD CONFIG DATA PLACED HERE

- This ensures that your mod is properly recognized and loaded by the EDF MML.

### 💡 Ready to Get Started With Your MCD?
- ##### [Step 1️⃣ MOD_INFO](#1️⃣-mod_info-metadata)
- ##### [Step 2️⃣ CATEGORIES](#2️⃣-categories-block-organizing-mods)
- ##### [Step 3️⃣ DataReplacementTable](#3️⃣-datareplacementtable-modifies-existing-data)
- ##### [Step 4️⃣ NewToAddTextTableEntries](#4️⃣-newtoaddtexttableentries-adds-new-text)
- ##### [Step 5️⃣ NewToAddSubTitleList](#5️⃣-newtoaddsubtitlelist-adding-new-subtitles)
- ##### [Step 6️⃣ NewToAddModeList](#6️⃣-newtoaddmodelist-adds-new-mission-packs)
- ##### [Step 7️⃣ NewToAddSoldierWeaponCategory](#7️⃣-newtoaddsoldierweaponcategory-adding-new-soldier-weapon-slots)
- ##### [Step 8️⃣ NewToAddWeaponCatalog ](#8️⃣-newtoaddweaponcatalog-assigning-weapons-to-soldier-slots)
- ##### [Step 9️⃣ NewToAddWeaponTables](#9️⃣-newtoaddweapontables-adding-new-weapons-to-the-game)
- ##### [Step 1️⃣0️⃣ DirManifestToFilesUninstaller](#1️⃣0️⃣-dirmanifesttofilesuninstaller-file-cleanup--uninstallation)
- ##### [Step 1️⃣1️⃣ CHANGELOG](#1️⃣1️⃣-changelog-tracking-mod-version-history)
- ##### [Troubleshooting: Common Issues and How to Resolve Them](#troubleshooting-common-issues-and-how-to-resolve-them)



### 1️⃣ MOD_INFO (Metadata)
- ##### 🔹 File from Source:
    📌 Used by scripts: ConfigWeaponCuller, MML GUI - Updating the mods, and weapons to drop with every mission or a few.

- ##### 🔹 Modifies Game?
    ❌ No

- ##### 🔹 Adds New Data?
    ❌ No

- ##### 🔹 Purpose
    Stores metadata about the mod.
    Helps mod managers identify, track, and update mods.

- ##### 🔹 Limitations & Tips
    ⚠ Must manually update VERSION when releasing updates to prevent conflicts.

- ##### 🛠 JSON Skeleton
```json
"MOD_INFO": {
    "AUTHOR": "",
    "MOD NAME": "",
    "LINK": "",
    "VERSION": "",
    "MY WEAPONS DROP WITH MY TWO MISSION PACKS": false,
    "NOTES": ""
}
```

- ##### ✅ JSON Example
```json
"MOD_INFO": {
    "AUTHOR": "FevGrave",
    "MOD NAME": "EDF_6-1",
    "LINK": "https://github.com/FevGrave/EDF_6-1/archive/main.zip",
    "VERSION": "1.0.0",
    "MY WEAPONS DROP WITH MY TWO MISSION PACKS": true,
    "NOTES": "Ensure compatibility with latest patch."
}
```

### 2️⃣ CATEGORIES Block (Organizing Mods)

- ##### 🔹 Purpose

    The CATEGORIES block is a quality-of-life feature that allows mods to be categorized for easier searching and organization within the Mods Panel of the EDF MML. The Mods Panel pulls the names from the CATEGORIES block and adds them to a search pool. This allows users to quickly find mods based on their category using the "Filter by Category" dropdown menu.

- ##### 🔹 Limitations & Tips

    ⚠ Use capitalized first letters for each category name.
    ⚠ Examples of categories include: "Weapons," "Gameplay," "Patch."
    ⚠ Keep category names concise and relevant to the mod's purpose to not clutter the search pool.


- ##### 🛠 JSON Skeleton

        "CATEGORIES": []

- ##### ✅ JSON Example (Filled)

        "CATEGORIES": ["Weapons", "Gameplay", "Patch", "Localization", "Bug Fixes" "MEME"]

- ##### 🔹 Limitations & Tips

    - ⚠ Avoid duplicate or overly generic categories to maintain a clear and useful search pool.
    - ⚠ Keep category names concise and relevant to the mod's purpose

### 3️⃣ DataReplacementTable (Modifies Existing Data)
- ##### 🔹 File from Source:
    📌 ConfigStringReplacer9000.py

- ##### 🔹 Modifies Game?
    ✅ Yes – Replaces existing text entries within the allowed .json files

- ##### 🔹 Adds New Data?
    ❌ No

- ##### 🔹 Source File:
    - 📌 ConfigStringReplacer9000.py

- ##### 🔹 End Product File:
    - 📂 YES

- ##### 🔹 Purpose
    Allows modifying in-game text (e.g., item descriptions, subtitles).
    Used for replacing existing text in the game files.

- ##### 🔹 Limitations & Tips
    ⚠ Ensure Find values match exactly, including every possible character. and do the large enough unique strings to get the right one.

- #####  🛠 JSON Skeleton
```json
"DataReplacementTable": [
    {
        "File": "",
        "Find": { "value": "" },
        "Replace": { "value": "" }
    }
]
```
- ##### ✅ JSON Example (Filled) 3 items
```json
"DataReplacementTable": [
    {
        "File": "ImportTextTable-EN.json",
        "Find": {
            "name": "RoomType_Everyone",
            "type": "string",
            "value": "Everyone"
        },
        "Replace": {
            "name": "RoomType_Everyone",
            "type": "string",
            "value": "Change Me (Joinable)"
        }
    },
    {
        "File": "ImportTextTable-EN.json",
        "Find": {
            "value": "A standard room.\nStandard rooms are displayed in the lobby for everyone to join."
        },
        "Replace": {
            "value": "Modded hosting in public lobbies is not recommended due to the potential for instability and  unexpected behavior..."
        }
    },
    {
        "File": "ImportTextTable-EN.json",
        "Find": {
            "value": "Passcode Only"
        },
        "Replace": {
            "value": "Change Me (Password)"
        }
    }
]
```
### 4️⃣ NewToAddTextTableEntries (Adds New Text)
- ##### 🔹 File from Source:
    📌 ConfigTextBuilder.py

- ##### 🔹 Modifies Game?
    ❌ No

- ##### 🔹 Adds New Data?
    ✅ Yes – Adds new UI text & descriptions

- ##### 🔹 Source File:
    - 📌 ImportTextTable-EN.json

- ##### 🔹 End Product File:
    - 📂 TEXTTABLE_STEAM.EN.TXT.json

- ##### 🔹 Connections to Other Blocks:
    - ##### The name and value fields in NewToAddTextTableEntries are also connected to:
        - NewToAddModeList: The first two strings in both connectivity nodes are directly linked to the entries in to this NewToAddTextTableEntries.
        - NewToAddSoldierWeaponCategory Block: This block's String value is tied to the name values defined here to display Weapon categories.
        - NewToAddWeaponCatalog Block: This block's String value is tied to the name values defined here to display Weapon categories.

- ##### 🔹 Purpose
    Used for new mission names, item descriptions, ANYTHING WITH THE GAMES UI
    
- ##### 🔹 Limitations & Tips
    ⚠ Use unique name values to avoid overwriting default game text. but needs to be the same with all LANG files

🛠 JSON Skeleton
```json
"NewToAddTextTableEntries": {
    "CN": [{ "name": "", "type": "string", "value": "" }],
    "EN": [{ "name": "", "type": "string", "value": "" }],
    "KR": [{ "name": "", "type": "string", "value": "" }],
    "JA": [{ "name": "", "type": "string", "value": "" }],
    "SC": [{ "name": "", "type": "string", "value": "" }]
}
```
- ##### ✅ JSON Example (Filled)
```json
"NewToAddTextTableEntries": {
    "CN": [{ "name": "Test_Scenario", "type": "string", "value": "离线MODDED任务模式" }],
    "EN": [{ "name": "Test_Scenario", "type": "string", "value": "Offline MODDED Mission Mode" }],
    "KR": [{ "name": "Test_Scenario", "type": "string", "value": "오프라인 개조 미션 모드" }],
    "JA": [{ "name": "Test_Scenario", "type": "string", "value": "オフライン改造ミッションモード" }],
    "SC": [{ "name": "Test_Scenario", "type": "string", "value": "离线MODDED任务模式" }]
}
```

### 5️⃣ NewToAddSubTitleList (Adding New Subtitles)
🛠 Section: NewToAddSubTitleList
- ##### 🔹 File from Source:
    ##### 📌 ConfigSubtitleAppender.py

- ##### 🔹 Modifies Game?
    ##### ❌ No

- ##### 🔹 Adds New Data?
    ##### ✅ Yes – Adds new mission subtitles

- ##### 🔹 Source File:
    - 📌 ImportSubtitleVoiceTable.EN.json

- ##### 🔹 End Product File:
    - 📂 EDF6_VOICETABLE.EN.json

- ##### 🔹 Purpose
    Adds custom subtitles for missions, cutscenes, or dialogue.
    Supports multiple languages (CN, EN, JA, KR, SC).
    Allows for customized in-game text linked to missions. .AC or .RMPA AND .BVM files. USE .AC for online

- ##### 🔹 Limitations & Tips
    ⚠ Each subtitle must have a unique name to prevent overwriting existing data.
    ⚠ Subtitles are mission-specific, so ensure they match mission scripting.
    ⚠ Use consistent naming (YourModpackName_MissionXXX_#) for easy tracking.
    ⚠ If a language is not included, the game may use any filled in fallback default.

- ##### 🛠 JSON Skeleton
```json
"NewToAddSubTitleList": {
    "CN": [],
    "EN": [
        {
        "value": [
            {"value": "CharacterName", "type": "str", "name": ""},
            {"value": "", "type": "str", "name": "caption"}
        ],
        "type": "ptr",
        "name": ""
        }
    ],
    "JA": [],
    "KR": [],
    "SC": []
}
```
- ##### ✅ JSON Example (Filled)
```json
"NewToAddSubTitleList": {
    "CN": [],
    "EN": [
        {
            "value": [
                {
                    "value": "CharacterName",
                    "type": "str",
                    "name": "SARGE"
                },
                {
                    "value": "Don't worry, I'll take you to a safe place.",
                    "type": "str",
                    "name": "caption"
                }
            ],
            "type": "ptr",
            "name": "YourModpackName_Mission001_1"
        },
        {
            "value": [
                {
                    "value": "CharacterName",
                    "type": "str",
                    "name": "SOMENPC"
                },
                {
                    "value": "Second mission subtitle",
                    "type": "str",
                    "name": "caption"
                }
            ],
            "type": "ptr",
            "name": "YourModpackName_Mission001_2"
        },
        {
            "value": [
                {
                    "value": "CharacterName",
                    "type": "str",
                    "name": "SOMENPC"
                },
                {
                    "value": "Time loop mission subtitle",
                    "type": "str",
                    "name": "caption"
                }
            ],
            "type": "ptr",
            "name": "YourModpackName_Mission001_3"
        }
    ],
    "JA": [],
    "KR": [],
    "SC": []
}
```

### 6️⃣ NewToAddModeList (Adds New Mission Packs)
- ##### 🔹 File from Source:
    📌 ConfigBuilder.py

- ##### 🔹 Modifies Game?
    ❌ No

- ##### 🔹 Adds New Data?
    ✅ Yes – Adds new mission packs

- ##### 🔹 Source File:
    - 📌 ImportDefaultData.json

- ##### 🔹 End Product File:
    - 📂 CONFIG.json

- ##### 🔹 Connections to Other Blocks:
    - ##### The name and value fields in NewToAddTextTableEntries are also connected to:
        - This block is connected to `NewToAddTextTableEntries`, which provides the text entries for the mode names and descriptions.
        - See [NewToAddTextTableEntries](#newtoaddtexttableentries-block) for details on adding new text entries.
        - The `missionDifficultyScale`, `PlayerCountDiffScale`, and other variables used in this block are typically defined in the game's core files. Modders should be cautious when modifying these values.

- ##### 🔹 Purpose
    Defines custom game modes or mission packs.

- ##### 🔹 Limitations & Tips
    ⚠ Ensure unique identifiers (e.g., mission pack names) are used to prevent conflicts with existing game modes or other mods.
    ⚠ Test thoroughly in No Installer Mode (EDF HAKKEN NI.exe) before deploying with Installer Mode (EDF HAKKEN.exe) to avoid game instability, especially given the patch’s "nefarious" nature—back up files to maintain rhythm in your modding dance!
    ⚠ Verify compatibility with the latest EDF 6 patches to ensure the patch’s effects remain stable across updates.

- ##### ⚠ This functional part is thanks to a "Nefarious DLC Enablement txt patch." This patch addresses two key issues:  
    - ##### ⚠ Breaking DLC Ownership: 
        ##### The patch bypasses restrictions tied to EDF 6’s DLC Mission Pack Ownership, Enabling modders to add custom mission packs without requiring specific DLC activation, expanding accessibility for all players. 
    - ##### ⚠ Fixing Custom 'DLC Re-Enablement': 
        ##### It Checks If You Have Played The DLC Mission Packs. And Blocks You From Selecting The DLC Mission Packs And Have Best Vanilla Guns Drop With Them.

- ##### 🛠 JSON Skeleton
```json
"NewToAddModeList": [
    1. **Offline Mode:** Defines settings and configurations for offline mission packs.
    2. **Online Mode:** Defines settings and configurations for online mission packs.
]
```
- ##### ✅ JSON Example (Filled) just for Offline
```json
"NewToAddModeList": [
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
                // Repeat the block above 4 more times to set Normal, Hard, Hardest, and Inferno difficulties.
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
]
```

### 7️⃣ NewToAddSoldierWeaponCategory (Adding New Soldier Weapon Slots)
🛠 Section: NewToAddSoldierWeaponCategory
- ##### 🔹 File from Source:
    📌 ConfigBuilder.py

- ##### 🔹 Modifies Game?
    ❌ No

- ##### 🔹 Adds New Data?
    ✅ Yes – Adds new weapon slot categories for soldiers

- ##### 🔹 Source File:
    - 📌 ImportDefaultData.json

- ##### 🔹 End Product File:
    - 📂 CONFIG.json

- ##### 🔹 Connections to Other Blocks:
    - ##### The name and value fields in NewToAddTextTableEntries are also connected to:
        - This block is directly linked to `NewToAddTextTableEntries`, where you define the names of the weapon slots.
        - See [NewToAddTextTableEntries](#newtoaddtexttableentries-block) for instructions on adding new text entries for weapon slot names.
        - The Weapon Category IDs defined here correspond to the categories in `NewToAddWeaponTables`.

- ##### 🔹 Purpose
    Defines new weapon slots for each soldier class.
    Allows modders to add custom weapon types for Ranger, WingDiver, AirRaider, and Fencer.
    Used in conjunction with NewToAddWeaponCatalog-* to control weapon availability.

- ##### 🔹 Limitations & Tips
    ⚠ Each value ID must be unique to prevent overwriting existing weapon slots.
    ⚠ The string name must match NewToAddWeaponCatalog-* entries to properly assign weapons.
    ⚠ Support slots can be defined separately (e.g., "Ranger_Weapon_Slot_Support_Slot").

- ##### 🛠 JSON Skeleton
```json
"NewToAddSoldierWeaponCategory": [
    {
      "type": "ptr",
      "value": [
        {"type": "int", "value": 0},
        {"type": "string", "value": ""}
      ]
    }
]
```
- ##### ✅ JSON Example (Filled)
```json
"NewToAddSoldierWeaponCategory": [
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
        {"type": "int", "value": 10001},
        {"type": "string", "value": "Ranger_Weapon_Slot_Support_Slot"}
      ]
    },
    {
      "type": "ptr",
      "value": [
        {"type": "int", "value": 20000},
        {"type": "string", "value": "WingDiver_Weapon_Slot"}
      ]
    },
    {
      "type": "ptr",
      "value": [
        {"type": "int", "value": 20001},
        {"type": "string", "value": "WingDiver_Weapon_Slot_Support_Slot"}
      ]
    },
    {
      "type": "ptr",
      "value": [
        {"type": "int", "value": 30000},
        {"type": "string", "value": "AirRaider_Weapon_Slot"}
      ]
    },
    {
      "type": "ptr",
      "value": [
        {"type": "int", "value": 30001},
        {"type": "string", "value": "AirRaider_Weapon_Slot_Support_Slot"}
      ]
    },
    {
      "type": "ptr",
      "value": [
        {"type": "int", "value": 40000},
        {"type": "string", "value": "Fencer_Weapon_Slot"}
      ]
    },
    {
      "type": "ptr",
      "value": [
        {"type": "int", "value": 40001},
        {"type": "string", "value": "Fencer_Weapon_Slot_Support_Slot"}
      ]
    }
]
```

### 8️⃣ NewToAddWeaponCatalog (Assigning Weapons to Soldier Slots)
🛠 Section: NewToAddWeaponCatalog
- ##### 🔹 File from Source:
    📌 ConfigWeaponAppender.py, ConfigDLCWeaponCuller.py, ConfigWeaponCuller.py

- ##### 🔹 Modifies Game?
    ❌ No

- ##### 🔹 Adds New Data?
    ✅ Yes – Assigns weapons to specific soldier slots

- ##### 🔹 Source File:
    - 📌 ImportDefaultData.json

- ##### 🔹 End Product File:
    - 📂 CONFIG.json

- ##### 🔹 Connections to Other Blocks:
    - ##### The name and value fields in NewToAddTextTableEntries are also connected to:
        - This block is directly linked to `NewToAddSoldierWeaponCategory`, where you define the weapon categories.
        - See [NewToAddSoldierWeaponCategory](#newtoaddsoldierweaponcategory-block) for details on defining new weapon categories.
        - The Weapon Category IDs used here should match those defined in `NewToAddSoldierWeaponCategory`.

- ##### 🔹 Purpose
    Links weapon slots (defined in NewToAddSoldierWeaponCategory) to soldier classes.
    Controls which weapons are available in each slot.
    Allows multiple weapon categories per slot (e.g., support, vehicle, or dual-wielding).

- ##### 🔹 Limitations & Tips
    - ⚠ Weapon category IDs must match NewToAddSoldierWeaponCategory to ensure proper assignments.
    - ⚠ Fencer has dual-wielding slots (L & R)—configure accordingly.

- ##### 🛠 JSON Skeleton
```json
"NewToAddWeaponCatalog": {
    "SoldierClass": {
        "Weapon_Slot1": {"value": [{"type": "int", "value": 0}]}
    }
}
```
- ##### ✅ JSON Example (Filled)
```json
"NewToAddWeaponCatalog": {
    "Ranger": {
        "Weapon_Slot1": {"value": [{"type": "int", "value": 10000}]},
        "Weapon_Slot2": {"value": [{"type": "int", "value": 10000}]},
        "Weapon_SlotSupport1": {"value": [{"type": "int", "value": 10001}]},
        "Weapon_SlotSupport2": {"value": [{"type": "int", "value": 10001}]}
    },
    "WingDiver": {
        "Weapon_Slot1": {"value": [{"type": "int", "value": 20000}]},
        "Weapon_Slot2": {"value": [{"type": "int", "value": 20000}]},
        "Weapon_SlotPaleSupport1": {"value": [{"type": "int", "value": 20001}]},
        "Weapon_SlotPaleSupport2": {"value": [{"type": "int", "value": 20001}]}
    },
    "AirRaider": {
        "Weapon_Slot1": {"value": [{"type": "int", "value": 30000}]},
        "Weapon_Slot2": {"value": [{"type": "int", "value": 30000}]},
        "Weapon_Slot3": {"value": [{"type": "int", "value": 30000}]},
        "Weapon_SlotAirRaiderSupport": {"value": [{"type": "int", "value": 30001}]},
        "Weapon_SlotVehicle": {"value": [{"type": "int", "value": 30001}]}
    },
    "Fencer": {
        "Weapon_Slot1L": {"value": [{"type": "int", "value": 40000}]},
        "Weapon_Slot1R": {"value": [{"type": "int", "value": 40000}]},
        "Weapon_Slot2L": {"value": [{"type": "int", "value": 40000}]},
        "Weapon_Slot2R": {"value": [{"type": "int", "value": 40000}]},
        "Weapon_SlotFencerSupport": {"value": [{"type": "int", "value": 40001}]}
    }
}
```

### 9️⃣ NewToAddWeaponTables (Adding New Weapons to the Game)
🛠 Section: NewToAddWeaponTables
- ##### 🔹 File from Source:
    📌 ConfigWeaponAppender.py

- ##### 🔹 Modifies Game?
    ❌ No

- ##### 🔹 Adds New Data?
    ✅ Yes – Adds new weapons for all soldier classes

- ##### 🔹 Source File:
    - 📌 ImportWeaponTextTable.json
    - 📌 ImportWeaponTextTable-EN.json

- ##### 🔹 End Product File:
    - 📂 WEAPONTEXT.json
    - 📂 WEAPONTEXT.EN.json

- ##### 🔹 Connections to Other Blocks:
    - ##### The name and value fields in NewToAddTextTableEntries are also connected to:
        - NewToAddWeaponCatalog: Required if using custom weapon groups. This block links the weapon categories to the soldier classes.

- ##### 🔹 Purpose
    Defines new weapons for Ranger, WingDiver, AirRaider, and Fencer.
    Each weapon entry includes name, stats, and text descriptions.
    Works with NewToAddWeaponCatalog to assign weapons to the correct slots.

- ##### 🔹 Limitations & Tips
    ⚠ Ensure the weapon names are unique to prevent conflicts with existing weapons.
    ⚠ Stat values (e.g., damage, range, reload time) must be properly formatted in the "value" array. 
    ⚠ Localized text (EN, JA, etc.) must be structured correctly to display properly in-game.
    ⚠ Each weapon category (e.g., Assault Rifles, Shotguns) should be correctly assigned for organization.
    Text can also use the WSRLF foumula to display stats. or use the WSRLF.EXE to display the formula to a graph.
    - result = BASE_VALUE * (p1 * (TARGET_LEVEL / 5)^p2 - p1 + 1)
    \[
    \text{result} = \text{BASE\_VALUE} \times \left( p_1 \times \left( \frac{\text{TARGET\_LEVEL}}{5} \right)^{p_2} - p_1 + 1 \right)
    \]


- ##### 🛠 JSON Skeleton
```json
"NewToAddWeaponTables": {
    "SOLDIER_CLASS": {
        "WEAPON_CATEGORY": [
            {
                "name": "",
                "Data": {},
                "Text": {
                    "CN": {},
                    "EN": {},
                    "JA": {},
                    "KR": {},
                    "SC": {}
                }
            }
        ]
    }
}
```
- ##### ✅ JSON Example (Filled)
```json
"NewToAddWeaponTables": {
    "RANGER": {
        "Assault Rifles": [
            {
                "name": "Broken PA-11",
                "Data": {
                    "value": [
                        {"value": "AssultRifle01", "type": "str"},
                        {"value": "app:/weapon/AssultRifle01.sgo", "type": "str"},
                        {"value": 10000, "type": "double"},
                        {"value": 1, "type": "double"},
                        {"value": 0, "type": "double"},
                        {"value": 1, "type": "double"}
                    ],
                    "type": "ptr"
                },
            "Text": {
                "CN": {},
                "EN": {
                    "value": [
                        {"value": "Broken PA-11", "type": "str"},
                        {
                            "value": "A broken high-performance assault rifle.\nRepaired with spare parts, reducing its effectiveness.",
                            "type": "str"
                        }
                    ],
                    "type": "ptr"
                },
                "JA": [],
                "KR": [],
                "SC": []
                }
            }
        ],
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
    },
    "WINGDIVER": {
        "Short-Range": [],
        "Mid-Range Energy Weapons": [],
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
        "Enhanced Exoskeletons": []
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
    }
}
```

### 1️⃣0️⃣ DirManifestToFilesUninstaller (File Cleanup & Uninstallation)

- ##### 🔹 Modifies Game?
    ❌ No

- ##### 🔹 Adds New Data?
    ❌ No

- ##### 🔹 Source Files:
    - 📌 ManifestMAKER.py
    - 📌 NOT A PART, ITS IN THE MML GUI LOGIC,
    - 📌 ConfigManifestUninstaller.exe

- ##### 🔹 Purpose
    Ensures clean removal of mod files.
    Used by Mods Panel UI → "Uninstall" button.
    Included in the ~~~mymodfolder\Mods~~~ folder is a ManifestMAKER.exe will write out the dir tree and can write to your MCD file

- ##### 🔹 Limitations & Tips
    ⚠ Always use a single master folder for you mission packs.

- ##### 🛠 JSON Skeleton
```json
"DirManifestToFilesUninstaller": {
    "MISSION": { "Folders": [] "Files"; []},
    "WEAPON": ["Files": []],
    "OBJECT": ["Files": []],
    "HUD": ["Files": []]
}
```
- ##### ✅ JSON Example (Filled)
```json
"DirManifestToFilesUninstaller": {
    "MISSION": { "Folders": ["MY_MODDED_MISSION_PACK_FOLDER"] },
    "WEAPON": [
        "V605_BARGA_D_CANNON.SGO",
        "V610_MACHINEGUN.SGO"
    ],
    "OBJECT": [
        "DAMAGE_TEST.rab",
        "DAMAGE_TEST.sgo",
        "ANTFALL.rab",
        "ANTFALL.SGO"
    ]
}
```


### 1️⃣1️⃣ CHANGELOG (Tracking Mod Version History)
🛠 Section: CHANGELOG
- ##### 🔹 File from Source:
    📌 Not used by scripts – For Mod Pannel's Info only

- ##### 🔹 Modifies Game?
    ❌ No

- ##### 🔹 Adds New Data?
    ❌ No – Documentation only

- ##### 🔹 Purpose
    Keeps a record of changes for each mod version.
    Helps track updates, fixes, and new features over time.
    Used by modders and users to see what has changed.
- ##### 🔹 Limitations & Tips
    ⚠ Must be updated manually whenever a new mod version is released.
    ⚠ Should follow a structured format (version, "summary of changes").
    ⚠ Empty values ("") should be avoided unless marking an upcoming change.

- ##### 🛠 JSON Skeleton
```json
"CHANGELOG": []
```
- ##### ✅ JSON Example (Filled)
```json
"CHANGELOG": [
  "0.1.0", 
  "Initial mod release with new weapons and missions.",
  "0.0.9", 
  "Building Phase"
]
```


### Troubleshooting: Common Issues and How to Resolve Them

- Most Common Issue: Formatting errors in Mod_config_data.json.

    - ⚠ Solution: If there is a formatting issue, you will know it during the "i" mode installation of the generated content. as they will sit in
    - Make sure if you dont need a block that was defined with [] that you replace with a {} and vice versa
    - 🛠 Check AA-Log.txt: This log file will indicate what happened and provide clues to fix the error.