# 📌 EDF MML Documentation: Introduction for Mod_config_data.json
## 🌟 Welcome to Earth Defense Force 6 Modding!
This documentation serves as a comprehensive guide to using EDF MML (Multi-Mod Loader) HAKKEN Core and the Mod_config_data.json (MCD) system for modding Earth Defense Force 6. Whether you are creating new missions, weapons, or localizations, this guide will help you understand the modding pipeline from setup to execution. Your Already [Ready to Get Started With Your MCD](#-ready-to-get-started-with-your-mcd)? WOW

### ❌Disclaimer 
#### 🔹 Important Modding Requirements
- This tool requires knowledge of EDF asset modding.
- EDF MML merges multiple mods into a structured list, ensuring correct file placement.
- It uses SGOTT (Always Latest) to convert SGO ↔ JSON.
#### 🔹 Not used by This Tools:
- EDFTools (SGO ↔ XML) Allows MAB data to be read
- DSGO (SGO ↔ JSON) Slight Different Format
#### 🔹 Need Help? Access the Modding Wiki & Guides!
- Click "Get Into Modding" in the EDF MML UI to access useful resources:

#### 🔹 Documentation/Wiki (Advanced & Comprehensive)

- Covers detailed EDF modding knowledge, including asset modifications, advanced techniques, and full integration methods.

#### 🔹 Maybe Birb’s Guide to Mod EDF Assets (Beginner-Friendly)

- A starter-oriented guide for learning how to modify EDF assets, perfect for newcomers.
- This ensures both beginners and advanced users have access to the right tools and information for modding EDF 4.1, 5, 6.

### 📂 What’s in This Guide?
- 🔹 Setup & Basics for content generation for EDF HAKKEN
- ✅ How to Understand and configure the Mod_config_data.json (MCD)

### 🔹 Core Modding Sections
- 🛠 Patching Content → That Is Deemed Incorrect And Must Be Fixed
- 🛠 Text Modifications → Modify in-game UI text & descriptions
- 🛠 Mission Pack Creation → Add custom mission sets
- 🛠 Weapon & Soldier Expansion → Define new weapons & categories
- 🛠 Mod Cleanup & Uninstallation → Ensure a clean Uninstallation mod process

### 📢 Important Notes for Modders
- ⚠ Repair Tables Before Modding! Always test changes before deploying.
- ⚠ Check JSON Formatting! Use a JSON validator to avoid syntax errors.
- ⚠ Use Unique Identifiers! Prevent text or weapon conflicts in game.

## 📌 EDF HAKKEN Core Executables (EDF HAKKEN.exe & EDF HAKKEN NI.exe)
### Double Meaning: Modding and Hardstyle/Gabber Dance (Hakken/Hakka) HUH?
#### Modding Aspect: 
- HAKKEN’s primary role as a highly adaptive, core modding tool for EDF 6 is clear, processing `Mod_config_data.json` to build and integrate modded content seamlessly across the MML ecosystem (e.g., patching content, creating mission packs, expanding weapons, as outlined in your updated sections).
#### Hardstyle/Gabber Dance Aspect: 
- The acronym of this HAKKEN tool ties into the Hakken/Hakka dance styles, known for their energetic, stomping, and rhythmic movements synced to the fast, pounding beats of Hardstyle and Gabber music genres (typically 140–150 BPM or WAYYY higher). "Highly Adaptive" mirrors a dancer’s ability to adapt to rapid tempo changes and intense rhythms, while "Kernel Kit" suggests the foundational beat and moves of the dance. "EDF Network" implies a network of ravers or EDF soldiers moving in unison, defending Earth with the same intensity as a Hardstyle/Gabber dance floor, adding a high-energy, cultural twist that resonates with EDF’s action-packed universe and modding’s dynamic creativity.

### WHAT IS HAKKEN: Highly Adaptive Kernel Kit for the EDF Network
- **Highly**: This word highlights HAKKEN’s exceptional capability and flexibility, emphasizing its ability to adapt to diverse modding needs in EDF 6—such as processing `Mod_config_data.json` for missions, weapons, and text (e.g., `NewToAddModeList`, `NewToAddWeaponTables`). In the Hardstyle/Gabber context, it mirrors the intense, high-energy beats that drive the Hakken/Hakka dance, suggesting a modding tool that moves with the same vigor and adaptability as a dancer stomping to rapid tempos.
- **Adaptive**: Reinforces HAKKEN’s versatility, adjusting seamlessly to mod configurations, game updates, and user inputs (e.g., switching between EDF HAKKEN.exe and EDF HAKKEN NI.exe modes). It also evokes the fluid, responsive movements of Hakken/Hakka dancing, syncing with the modding "rhythm" of creativity and precision, much like a dancer adapting to the pounding beats of Hardstyle or Gabber.
- **Kernel**: Positions HAKKEN as the core engine or processing unit, central to building modded tables and generating files like `CONFIG.json` and `WEAPONTEXT.json`. In the Hardstyle/Gabber context, it represents the steady, driving beat or core rhythm that fuels the Hakken/Hakka performance on the dance floor.
- **Kit**: Suggests HAKKEN as a comprehensive toolkit for modders, aligning with its executable nature and the "Build Tables" functionality in the MML UI. In the Hardstyle/Gabber context, it evokes a collection of dance moves or techniques (e.g., stomping, kicking) that modders use to choreograph their "performance" in the EDF universe.
- **for EDF**: Maintains the direct link to Earth Defense Force, ensuring specificity to EDF 6 modding and its military/sci-fi theme, with a nod to the disciplined, aggressive energy of military maneuvers (akin to the fierce, stomping energy of Hakken/Hakka dancing).
- **Network**: Evokes a broader, interconnected system within EDF 6 modding, connecting modders, players, game data, and online/offline progress (e.g., via the Online Progress Tracker and Mods Panel). In the Hardstyle/Gabber context, it suggests a network of ravers or dancers at a festival, moving in sync to the music, reflecting the collaborative, synchronized nature of modding the EDF universe.

#### 🛠 What Are These Files?
- The HAKKEN Core executables are responsible for building and processing modded tables in EDF MML. They handle mod integration in two different ways:

#### Executable Mode Purpose?
- EDF HAKKEN.exe Installer Mode	Fully integrates mod data into game files for public release.
- EDF HAKKEN NI.exe	No Installer Mode	Used for testing mods without modifying core game files, reducing crash risks.

### 🛠 How They Work in MML
- 1️⃣ User Clicks "Build Tables" in the EDF MML UI.
- 2️⃣ Triggers EDF HAKKEN.exe or EDF HAKKEN NI.exe based on the mode.
- 3️⃣ Processes Mod_config_data.json and builds the necessary game tables.
- 4️⃣ Finalizes mod integration or prepares for testing.

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
- ##### 🔹 Generated Files
        /==================================|=====================================|=====================================\
        |                                  |                                     |                                     |
        | SOURCE STARTING JSON FILE        | FINISHED PRODUCT WITH MODIFICATIONS | WHAT ARE THEY ?                     |
        |                                  |                                     |                                     |
        |==================================|=====================================|=====================================|
        | ImportDefaultData.json           | CONFIG.json                         |📂 Mission Pack Data                ::
        |==================================|=====================================|=====================================|
        | ImportSubtitleVoiceTable.CN.json | EDF6_VOICETABLE.CN.json             |📂 Subtitle Table Data              ::
        | ImportSubtitleVoiceTable.EN.json | EDF6_VOICETABLE.EN.json             |  Holds All Text In The Missions     |
        | ImportSubtitleVoiceTable.JA.json | EDF6_VOICETABLE.JA.json             |                                     |
        | ImportSubtitleVoiceTable.KR.json | EDF6_VOICETABLE.KR.json             |                                     |
        | ImportSubtitleVoiceTable.SC.json | EDF6_VOICETABLE.SC.json             |                                     |
        |==================================|=====================================|=====================================|
        | ImportTextTable-CN.json          | TEXTTABLE_STEAM.CN.TXT.json         |📂 GUI Text Tables (Localization)   ::
        | ImportTextTable-EN.json          | TEXTTABLE_STEAM.EN.TXT.json         |  Holds All Text In The Games UI     |
        | ImportTextTable-JA.json          | TEXTTABLE_STEAM.JA.TXT.json         |  Translators Of Other Languages     |
        | ImportTextTable-KR.json          | TEXTTABLE_STEAM.KR.TXT.json         |  Use This File For Your Translation |
        | ImportTextTable-SC.json          | TEXTTABLE_STEAM.SC.TXT.json         |                                     |
        |==================================|=====================================|=====================================|
        | ImportWeaponTextTable.json       | WEAPONTEXT.json                     |📂 Weapon Level, Config Data        ::
        |==================================|=====================================|=====================================|
        | ImportWeaponTextTable-CN.json    | WEAPONTEXT.CN.json                  |📂 Weapon Text Stats (Localization) ::
        | ImportWeaponTextTable-EN.json    | WEAPONTEXT.EN.json                  |  Visual Text To Display The Items   |
        | ImportWeaponTextTable-KR.json    | WEAPONTEXT.KR.json                  |  Stats.                             |
        | ImportWeaponTextTable-SC.json    | WEAPONTEXT.SC.json                  |                                     |
        |==================================|=====================================|=====================================|
        | P501_PROTO_RANGER.json           | P501_PROTO_RANGER.json              | 📂 EDF 5 Civ Skin                  ::
        | P502_PROTO_WINGDIVER.json        | P502_PROTO_WINGDIVER.json           |  Settings for Camera, Grip Offsets  |
        | P503_PROTO_FENCER.json           | P503_PROTO_FENCER.json              |  "IK" lengths, Spotlight, Color,    |
        | P504_PROTO_AIRRADER.json         | P504_PROTO_AIRRAIDER.json           |  And many more, Same Applies Bellow |
        |==================================|=====================================|=====================================|
        | P505_RANGER.json                 | P505_RANGER.json                    | 📂 EDF 5 Military Skin             ::
        | P506_WINGDIVER.json              | P506_WINGDIVER.json                 |                                     |
        | P507_FENCER.json                 | P507_FENCER.json                    |                                     |
        | P508_AIRRADER.json               | P508_AIRRAIDER.json                 |                                     |
        |==================================|=====================================|=====================================|
        | P601_PROTO_RANGER.json           | P601_PROTO_RANGER.json              | 📂 EDF 6 Tattered Military Skin    ::
        | P602_PROTO_WINGDIVER.json        | P602_PROTO_WINGDIVER.json           |                                     |
        | P603_PROTO_FENCER.json           | P603_PROTO_FENCER.json              |                                     |
        | P604_PROTO_AIRRADER.json         | P604_PROTO_AIRRAIDER.json           |                                     |
        |==================================|=====================================|=====================================|
        | P605_RANGER.json                 | P605_RANGER.json                    | 📂 EDF 6 Future Military Skin      ::
        | P606_WINGDIVER.json              | P606_WINGDIVER.json                 |                                     |
        | P607_FENCER.json                 | P607_FENCER.json                    |                                     |
        | P608_AIRRADER.json               | P608_AIRRAIDER.json                 |                                     |
        \==================================|=====================================|=====================================/

### 🛠 How to Switch Modes
    - 1️⃣ In EDF MML, locate the "Request Mod Code" text box. 
    - 2️⃣ Type ni → Press Enter → Switches to No Installer Mode.
    - 3️⃣ Type i → Press Enter → Switches to Installer Mode.
    - 4️⃣ The selected mode will be applied when clicking "Build Tables".

### 🚀 Best Practices
    - ✅ Use ni mode for safe mod testing before finalizing changes.
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

### 💡 Ready to Get Started With Your MCD?
- ##### [Step 1️⃣ MOD_INFO](#1️⃣-mod_info-metadata)
- ##### [Step 2️⃣ DataReplacementTable](#2️⃣-datareplacementtable-modifies-existing-data)
- ##### [Step 3️⃣ NewToAddTextTableEntries](#3️⃣-newtoaddtexttableentries-adds-new-text)
- ##### [Step 4️⃣ NewToAddSubTitleList](#4️⃣-newtoaddsubtitlelist-adding-new-subtitles)
- ##### [Step 5️⃣ NewToAddModeList](#5️⃣-newtoaddmodelist-adds-new-mission-packs)
- ##### [Step 6️⃣ NewToAddSoldierWeaponCategory](#6️⃣-newtoaddsoldierweaponcategory-adding-new-soldier-weapon-slots)
- ##### [Step 7️⃣ NewToAddWeaponCatalog ](#7️⃣-newtoaddweaponcatalog-assigning-weapons-to-soldier-slots)
- ##### [Step 8️⃣ NewToAddWeaponTables](#8️⃣-newtoaddweapontables-adding-new-weapons-to-the-game)
- ##### [Step 9️⃣ DirManifestToFilesUninstaller](#9️⃣-dirmanifesttofilesuninstaller-file-cleanup--uninstallation)
- ##### [Step 1️⃣0️⃣ CHANGELOG](#1️⃣0️⃣-changelog-tracking-mod-version-history)

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
### 2️⃣ DataReplacementTable (Modifies Existing Data)
- ##### 🔹 File from Source:
    📌 ConfigStringReplacer9000.py

- ##### 🔹 Modifies Game?
    ✅ Yes – Replaces existing text entries within the allowed .json files

- ##### 🔹 Adds New Data?
    ❌ No

- ##### 🔹 Purpose
    Allows modifying in-game text (e.g., item descriptions, subtitles).
- ##### 🔹 Limitations & Tips
    ⚠ Ensure Find values match exactly, including every possible character. and do the large enough to be unique out of the noise of data

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
- ##### ✅ JSON Example (Filled)
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
    }
]
```
### 3️⃣ NewToAddTextTableEntries (Adds New Text)
- ##### 🔹 File from Source:
    📌 ConfigTextBuilder.py

- ##### 🔹 Modifies Game?
    ❌ No

- ##### 🔹 Adds New Data?
    ✅ Yes – Adds new UI text & descriptions

- ##### 🔹 Purpose
    Adds new localizations across multiple languages.
    Used for new mission names, item descriptions, etc.
- ##### 🔹 Limitations & Tips
    ⚠ Use unique name values to avoid overwriting default game text.

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
    "EN": [{ "name": "Test_Scenario", "type": "string", "value": "Offline MODDED Mission Mode" }],
    "JA": [{ "name": "Test_Scenario", "type": "string", "value": "オフライン改造ミッションモード" }]
}
```

### 4️⃣ NewToAddSubTitleList (Adding New Subtitles)
🛠 Section: NewToAddSubTitleList
- ##### 🔹 File from Source:
    ##### 📌 ConfigSubtitleAppender.py

- ##### 🔹 Modifies Game?
    ##### ❌ No

- ##### 🔹 Adds New Data?
    ##### ✅ Yes – Adds new mission subtitles

- ##### 🔹 Purpose
    Adds custom subtitles for missions, cutscenes, or dialogue.
    Supports multiple languages (CN, EN, JA, KR, SC).
    Allows for customized in-game text linked to missions.

- ##### 🔹 Limitations & Tips
    ⚠ Each subtitle must have a unique name to prevent overwriting existing data.
    ⚠ Subtitles are mission-specific, so ensure they match mission scripting.
    ⚠ Use consistent naming (YourModpackName_MissionXXX_#) for easy tracking.
    ⚠ If a language is not included, the game may use any filled in fallback default.

- ##### 🛠 JSON Skeleton
```json
"NewToAddSubTitleList": {
    "CN": [],
    "EN": [],
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
                    "name": "name"
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
                    "name": "name"
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
                    "name": "name"
                },
                {
                    "value": "Time loop mission subtitle",
                    "type": "str",
                    "name": "caption"
                }
            ],
            "type": "ptr",
            "name": "YourModpackName_Mission001_3"
        },
        {
            "value": [
                {
                    "value": "CharacterName",
                    "type": "str",
                    "name": "name"
                },
                {
                    "value": "End mission subtitle",
                    "type": "str",
                    "name": "caption"
                }
            ],
            "type": "ptr",
            "name": "YourModpackName_Mission001_4"
        }
    ],
    "JA": [],
    "KR": [],
    "SC": []
}
```

### 5️⃣ NewToAddModeList (Adds New Mission Packs)
- ##### 🔹 File from Source:
    📌 ConfigBuilder.py

- ##### 🔹 Modifies Game?
    ❌ No

- ##### 🔹 Adds New Data?
    ✅ Yes – Adds new mission packs

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
    {
        "type": "ptr",
        "value": []
    }
]
```
- ##### ✅ JSON Example (Filled)
```json
"NewToAddModeList": [
    {
        "type": "ptr",
        "value": [
            { "type": "string", "value": "Test_Scenario" },
            { "type": "string", "value": "Test_Scenario_Desc" }
        ]
    }
]
```

### 6️⃣ NewToAddSoldierWeaponCategory (Adding New Soldier Weapon Slots)
🛠 Section: NewToAddSoldierWeaponCategory
- ##### 🔹 File from Source:
    📌 ConfigBuilder.py

- ##### 🔹 Modifies Game?
    ❌ No

- ##### 🔹 Adds New Data?
    ✅ Yes – Adds new weapon slot categories for soldiers

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

### 7️⃣ NewToAddWeaponCatalog (Assigning Weapons to Soldier Slots)
🛠 Section: NewToAddWeaponCatalog
- ##### 🔹 File from Source:
    📌 ConfigWeaponAppender.py, ConfigDLCWeaponCuller.py, ConfigWeaponCuller.py

- ##### 🔹 Modifies Game?
    ❌ No

- ##### 🔹 Adds New Data?
    ✅ Yes – Assigns weapons to specific soldier slots

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

### 8️⃣ NewToAddWeaponTables (Adding New Weapons to the Game)
🛠 Section: NewToAddWeaponTables
- ##### 🔹 File from Source:
    📌 ConfigWeaponAppender.py

- ##### 🔹 Modifies Game?
    ❌ No

- ##### 🔹 Adds New Data?
    ✅ Yes – Adds new weapons for all soldier classes

- ##### 🔹 Purpose
    Defines new weapons for Ranger, WingDiver, AirRaider, and Fencer.
    Each weapon entry includes name, stats, and text descriptions.
    Works with NewToAddWeaponCatalog to assign weapons to the correct slots.
- ##### 🔹 Limitations & Tips
    ⚠ Ensure the weapon names are unique to prevent conflicts with existing weapons.
    ⚠ Stat values (e.g., damage, range, reload time) must be properly formatted in the "value" array. 
    ⚠ Localized text (EN, JA, etc.) must be structured correctly to display properly in-game.
    ⚠ Each weapon category (e.g., Assault Rifles, Shotguns) should be correctly assigned for organization.

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

### 9️⃣ DirManifestToFilesUninstaller (File Cleanup & Uninstallation)
- ##### 🔹 File from Source:
    📌 ManifestMAKER.py & ConfigManifestUninstaller.exe

- ##### 🔹 Modifies Game?
    ❌ No

- ##### 🔹 Adds New Data?
    ❌ No

- ##### 🔹 Purpose
    Ensures clean removal of mod files.
    Used by Mods Panel UI → "Uninstall" button.
- ##### 🔹 Limitations & Tips
    ⚠ Always use a single master folder for you mission packs.

- ##### 🛠 JSON Skeleton
```json
"DirManifestToFilesUninstaller": {
    "MISSION": { "Folders": [] "Files"; []},
    "WEAPON": [],
    "OBJECT": []
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
        "ANTFALL.SGO"
    ]
}
```


### 1️⃣0️⃣ CHANGELOG (Tracking Mod Version History)
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