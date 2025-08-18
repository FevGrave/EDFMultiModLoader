import os
import sys
import subprocess
import ConfigStringReplacer9000
import ConfigBuilder
import ConfigTextBuilder
import ConfigWeaponAppender
import ConfigSubtitleAppender
import ConfigCompressor
import GamemodeConfig
import ConfigDLCWeaponCuller
import ConfigWeaponCuller
import ConfigYoinker
from contextlib import redirect_stdout, redirect_stderr, ExitStack

debug_mode = False  # Set to True if you want to skip sections 10+ for testing json compiling | False to do Full Processing

def check_arguments():
    if len(sys.argv) < 3:
        print("Usage: python script.py <output_directory> <current_directory>")
        sys.exit(1)
    return sys.argv[1], sys.argv[2]

class Tee:
    def __init__(self, *files):
        self.files = files

    def write(self, obj):
        for f in self.files:
            f.write(obj)

    def flush(self):
        for f in self.files:
            f.flush()

def log_message(message):
    print(message)
    with open(log_file_path, "a") as log_file:
        log_file.write(message + "\n")
        log_file.flush()  # Ensure immediate writing

def run_module(module, output_directory, current_directory):
    if hasattr(module, "main"):
        module.main(output_directory, current_directory)
    else:
        log_message(f"{module.__name__} does not have a main function.")

def find_sgott_path(output_directory):
    sgott_paths = [
        os.path.join(output_directory, "Mods", "TOOLS", "sgott.exe"),
        os.path.join(output_directory, "Mods", "EDF 6 MOD SETTINGS MAKER", "sgott.exe")
    ]
    for path in sgott_paths:
        if os.path.exists(path):
            log_message(f"Using sgott.exe at {path}")
            return path
    log_message("sgott.exe not found.")
    return None

# Main function
def main(output_directory, current_directory):
    log_message("Starting the EDF HAKKEN build process...")

    # 1. Run Data Replacement
    log_message("\nRunning data replacement...")
    run_module(ConfigStringReplacer9000, output_directory, current_directory)

    # 2. Yoink over non additive configs
    log_message("\nYoink over non additive configs...")
    run_module(ConfigYoinker, output_directory, current_directory)

    # 3. Build Config
    log_message("\nBuilding config...")
    run_module(ConfigBuilder, output_directory, current_directory)

    # 4. Configure DLC Mission Packs Or Modded And Adjust Positions
    #log_message("\nEDIT out DLC in config...")
    #run_module(GamemodeConfig, output_directory, current_directory)

    # 5. Process Text Tables and Subtitles
    log_message("\nProcessing text tables...")
    run_module(ConfigTextBuilder, output_directory, current_directory)
    log_message("\nProcessing subtitles...")
    run_module(ConfigSubtitleAppender, output_directory, current_directory)

    # 6. Append Weapon Data
    log_message("\nAppending weapon data...")
    run_module(ConfigWeaponAppender, output_directory, current_directory)

    # 7.Cull DLC Weapon Tables of non selected mission packs
    #log_message("\nEDIT DLC Weapon drops for matching mission packs...")
    #run_module(ConfigDLCWeaponCuller, output_directory, current_directory)

    # 8.Cull MODDED Weapon Tables of non selected mission packs
    #log_message("\nEDIT MODDED Weapon drops for matching mission packs...")
    #run_module(ConfigWeaponCuller, output_directory, current_directory)

    # 9. Compress Files, Brakes WEAPONTEXTTABLE.lang.json, Might be deprecated 
    #log_message("\nCompressing files...")
    #run_module(ConfigCompressor, output_directory, current_directory)

    # 10. SGO Conversion (only run if not in debug mode)
    if not debug_mode:
        sgottPath = find_sgott_path(output_directory)
        if sgottPath:
            log_message("\nStarting SGO conversion...")
            for filename in os.listdir(output_directory):
                if (
                    filename.lower().endswith(".json") 
                    and filename not in ["MMLsettings.json", "user_selections.json"]
                ):
                    filepath = os.path.join(output_directory, filename)
                    result = subprocess.run(
                        [sgottPath, filepath],
                        capture_output=True,
                        text=True,
                        encoding="utf-8",
                        creationflags=subprocess.CREATE_NO_WINDOW,
                    )
                    if result.returncode == 0:
                        log_message(f"Converted and removed {filename}")
                        os.remove(filepath)
                    else:
                        log_message(f"Error converting {filename}: {result.stderr}")

    # 11. Rename Text Files (only run if not in debug mode)
    if not debug_mode:
        log_message("\nRenaming in game text data files...")
        files_to_rename = [
            ("TEXTTABLE_STEAM.CN.TXT.SGO", "TEXTTABLE_STEAM.CN.TXT_SGO"),
            ("TEXTTABLE_STEAM.EN.TXT.SGO", "TEXTTABLE_STEAM.EN.TXT_SGO"),
            ("TEXTTABLE_STEAM.KR.TXT.SGO", "TEXTTABLE_STEAM.KR.TXT_SGO"),
            ("TEXTTABLE_STEAM.JA.TXT.SGO", "TEXTTABLE_STEAM.JA.TXT_SGO"),
            ("TEXTTABLE_STEAM.SC.TXT.SGO", "TEXTTABLE_STEAM.SC.TXT_SGO")
        ]
        for old_name, new_name in files_to_rename:
            old_path = os.path.join(output_directory, old_name)
            new_path = os.path.join(output_directory, new_name)
            if os.path.exists(old_path):
                os.replace(old_path, new_path)
                log_message(f"Renamed {old_name} to {new_name}")

    # 12. Move SGOs to Install Folders (only run if not in debug mode)
    if not debug_mode:
        log_message("\nInstalling SGOs to Mods folders...")
        destination_paths = {
            "CONFIG.SGO": "DEFAULTPACKAGE",
            "TEXTTABLE_STEAM.CN.TXT_SGO": "ETC",
            "TEXTTABLE_STEAM.EN.TXT_SGO": "ETC",
            "TEXTTABLE_STEAM.KR.TXT_SGO": "ETC",
            "TEXTTABLE_STEAM.JA.TXT_SGO": "ETC",
            "TEXTTABLE_STEAM.SC.TXT_SGO": "ETC",
            "WEAPONTABLE.SGO": "WEAPON",
            "WEAPONTEXT.CN.SGO": "WEAPON",
            "WEAPONTEXT.EN.SGO": "WEAPON",
            "WEAPONTEXT.JA.SGO": "WEAPON",
            "WEAPONTEXT.KR.SGO": "WEAPON",
            "WEAPONTEXT.SC.SGO": "WEAPON",
            "EDF6_VOICETABLE.CN.SGO": "MISSION",
            "EDF6_VOICETABLE.EN.SGO": "MISSION",
            "EDF6_VOICETABLE.JA.SGO": "MISSION",
            "EDF6_VOICETABLE.KR.SGO": "MISSION",
            "EDF6_VOICETABLE.SC.SGO": "MISSION",
            "P501_PROTO_RANGER.SGO": "OBJECT",
            "P502_PROTO_WINGDIVER.SGO": "OBJECT",
            "P503_PROTO_FENCER.SGO": "OBJECT",
            "P504_PROTO_AIRRADER.SGO": "OBJECT",
            "P505_RANGER.SGO": "OBJECT",
            "P506_WINGDIVER.SGO": "OBJECT",
            "P507_FENCER.SGO": "OBJECT",
            "P508_AIRRADER.SGO": "OBJECT",
            "P601_PROTO_RANGER.SGO": "OBJECT",
            "P602_PROTO_WINGDIVER.SGO": "OBJECT",
            "P603_PROTO_FENCER.SGO": "OBJECT",
            "P604_PROTO_AIRRADER.SGO": "OBJECT",
            "P605_RANGER.SGO": "OBJECT",
            "P606_WINGDIVER.SGO": "OBJECT",
            "P607_FENCER.SGO": "OBJECT",
            "P608_AIRRADER.SGO": "OBJECT"
        }

        for file_name, folder in destination_paths.items():
            source_path = os.path.join(output_directory, file_name)
            destination_dir = os.path.join(output_directory, "Mods", folder)
            destination_path = os.path.join(destination_dir, file_name)
            try:
                os.makedirs(destination_dir, exist_ok=True)
                os.replace(source_path, destination_path)
                log_message(f"Moved {file_name} to {destination_dir}")
            except Exception as e:
                log_message(f"Failed to move {file_name}. Error: {e}")

# Define log file path
output_directory, current_directory = check_arguments()
log_file_path = os.path.join(output_directory, "AA-Log.txt")

# Run main function with logging setup
with open(log_file_path, "w") as log_file:
    with ExitStack() as stack:
        stack.enter_context(redirect_stdout(Tee(sys.stdout, log_file)))
        stack.enter_context(redirect_stderr(Tee(sys.stderr, log_file)))
        main(output_directory, current_directory)
