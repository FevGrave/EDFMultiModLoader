import os, sys, time, subprocess
from contextlib import redirect_stdout, redirect_stderr, ExitStack

class Tee:
    def __init__(self, *files):
        self.files = files

    def write(self, obj):
        for f in self.files:
            f.write(obj)

    def flush(self):
        for f in self.files:
            f.flush()

def check_arguments():
    if len(sys.argv) < 2:
        print("Usage: python script.py <output_directory>")
        sys.exit(1)
    return sys.argv[1]

# Set the current directory
current_directory = os.path.dirname(os.path.abspath(__file__))

# Get the output directory
output_directory = os.path.abspath(os.path.join(current_directory, "..", ".."))  # check_arguments()

# Log file path
log_file_path = os.path.join(output_directory, "AA-Log.txt")

# Function to log messages to both console and file
def log_message(message):
    print(message)
    with open(log_file_path, "a") as log_file:
        log_file.write(message + "\n")

# Function to run a script and log its output in real-time
def run_script(script, output_directory):
    process = subprocess.Popen(
        ["python", script, output_directory],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
        bufsize=1
    )
    log_message(f"\nOutput from {script}:")

    while True:
        output = process.stdout.readline()
        if output == '' and process.poll() is not None:
            break
        if output:
            log_message(output.strip())
    
    # Capture any remaining output
    stdout, stderr = process.communicate()
    if stdout:
        log_message(stdout.strip())
    if stderr:
        log_message(stderr.strip())

# Redirect output to both console and log file
with open(log_file_path, "w") as log_file:
    with ExitStack() as stack:
        stack.enter_context(redirect_stdout(Tee(sys.stdout, log_file)))
        stack.enter_context(redirect_stderr(Tee(sys.stderr, log_file)))
        # Warming up tools
        log_message("Build Complete, Review for any errors or AA-Log.txt")

        # Run the Python scripts
        scripts = [
            "ConfigStringReplacer9000.py",
            "ConfigBuilder.py",
            "ConfigTextBuilder.py",
            "ConfigWeaponAppender.py",
            "ConfigCompressor.py"
        ]
        for script in scripts:
            run_script(os.path.join(current_directory, script), output_directory)

        # Baking SGO Extension From JSON With SGOTT.EXE, And Then Kills JSON
        log_message("\nBaking SGO Extension From JSON With SGOTT.EXE, And Then Kills JSON")
        

        # Set the possible paths for sgott.exe
        sgott_paths = [
            os.path.join(output_directory, "Mods", "TOOLS", "sgott.exe"),
            os.path.join(output_directory, "Mods", "EDF 6 MOD SETTINGS MAKER", "sgott.exe")
        ]
        sgottPath = None

        # Find the correct path for sgott.exe
        for path in sgott_paths:
            if os.path.exists(path):
                sgottPath = path
                log_message(f"Hello Fellow Modder {sgottPath}")
                break
        if not sgottPath:
            log_message("Sgott.exe not found in either directory.")
        else:
            # Loop through each JSON file in the output directory
            for filename in os.listdir(output_directory):
                if filename.lower().endswith(".json"):
                    filepath = os.path.join(output_directory, filename)
                    log_message(f"Processing file: {filename}")
                    result = subprocess.run([sgottPath, filepath], capture_output=True, text=True)
                    if result.returncode != 0:
                        log_message(f"Error processing {filename}. Error level: {result.   returncode}")
                        log_message(result.stderr)
                    else:
                        log_message(f"Conversion successful for {filename}")
                        os.remove(filepath)
                        log_message(f"{filename} deleted successfully.")

        # Post Processing Names Of Menu Text Files
        log_message("\nPost Processing Names Of Menu Text Files")
        
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
                log_message(f"Renaming {old_name} into {new_name}")
            else:
                log_message(f"File {old_name} does not exist, skipping renaming.")

        # Moving SGOs To Install Folders
        log_message("\nMoving SGOs To Install Folders")
        source_dir = output_directory
        destination_paths = {
            "CONFIG.SGO": os.path.join(output_directory, "Mods", "DEFAULTPACKAGE"),
            "TEXTTABLE_STEAM.CN.TXT_SGO": os.path.join(output_directory, "Mods", "ETC"),
            "TEXTTABLE_STEAM.EN.TXT_SGO": os.path.join(output_directory, "Mods", "ETC"),
            "TEXTTABLE_STEAM.KR.TXT_SGO": os.path.join(output_directory, "Mods", "ETC"),
            "TEXTTABLE_STEAM.JA.TXT_SGO": os.path.join(output_directory, "Mods", "ETC"),
            "TEXTTABLE_STEAM.SC.TXT_SGO": os.path.join(output_directory, "Mods", "ETC"),
            "WEAPONTABLE.SGO": os.path.join(output_directory, "Mods", "WEAPON"),
            "WEAPONTEXT.CN.SGO": os.path.join(output_directory, "Mods", "WEAPON"),
            "WEAPONTEXT.EN.SGO": os.path.join(output_directory, "Mods", "WEAPON"),
            "WEAPONTEXT.JA.SGO": os.path.join(output_directory, "Mods", "WEAPON"),
            "WEAPONTEXT.KR.SGO": os.path.join(output_directory, "Mods", "WEAPON")
        }

        for file_name, destination_dir in destination_paths.items():
            source_path = os.path.join(source_dir, file_name)
            destination_path = os.path.join(destination_dir, file_name)
            try:
                os.makedirs(destination_dir, exist_ok=True)
                os.replace(source_path, destination_path)
                log_message(f"Moving {file_name} into {destination_dir}")
                # Sleep after each file move
            except Exception as e:
                log_message(f"Failed to move {file_name}. Error: {str(e)}")