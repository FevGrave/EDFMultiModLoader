import os
import shutil
import sys

def move_files(output_dir, current_dir, file_list):
    # Ensure output directory exists
    os.makedirs(output_dir, exist_ok=True)
    
    # Iterate over each file in the list
    for file_name in file_list:
        src_path = os.path.join(current_dir, file_name)
        dest_path = os.path.join(output_dir, file_name)
        
        # Move the file if it exists in the current directory
        if os.path.exists(src_path):
            shutil.move(src_path, dest_path)
            print(f"Moved {file_name} to {output_dir}")
        else:
            print(f"File {file_name} does not exist in {current_dir}")

def main(output_dir, current_dir):
    # Check that enough arguments are provided
    if len(sys.argv) < 3:
        print("Usage: ConfigYoinker.py <output_dir> <current_dir>")
        sys.exit(1)
    
    # First argument is the output directory
    output_dir = sys.argv[1]
    # Second argument is the current directory
    current_dir = sys.argv[2]
    
    # Define the list of files to move
    file_list = [
        "P501_PROTO_RANGER.json",
        "P502_PROTO_WINGDIVER.json",
        "P503_PROTO_FENCER.json",
        "P504_PROTO_AIRRADER.json",
        "P505_RANGER.json",
        "P506_WINGDIVER.json",
        "P507_FENCER.json",
        "P508_AIRRADER.json",
        "P601_PROTO_RANGER.json",
        "P602_PROTO_WINGDIVER.json",
        "P603_PROTO_FENCER.json",
        "P604_PROTO_AIRRADER.json",
        "P605_RANGER.json",
        "P606_WINGDIVER.json",
        "P607_FENCER.json",
        "P608_AIRRADER.json"
    ]
    
    # Call the function to move files
    move_files(output_dir, current_dir, file_list)

if __name__ == "__main__":
    main()
