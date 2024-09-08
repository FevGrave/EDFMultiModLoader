import json
import os
import sys

def compress_json_file(input_file_path):
    # Read the original JSON data with UTF-8 encoding
    with open(input_file_path, 'r', encoding='utf-8') as file:
        json_data = json.load(file)
    
    # Write the minimized JSON data to the same file, also with UTF-8 encoding
    with open(input_file_path, 'w', encoding='utf-8') as file:
        json.dump(json_data, file, separators=(',', ':'), indent=2)

def compress_all_jsons_in_directory(directory_path):
    # Check if the directory exists
    if not os.path.exists(directory_path):
        print(f"Error: The directory {directory_path} does not exist.")
        return
    
    # Iterate over all files in the specified directory
    for filename in os.listdir(directory_path):
        if filename.endswith('.json'):
            file_path = os.path.join(directory_path, filename)
            print(f"Compressing: {file_path}")
            compress_json_file(file_path)
    print("Compression complete for all JSON files.")

if __name__ == "__main__":
    # Check if the directory path is provided as a command-line argument
    if len(sys.argv) < 2:
        print("Usage: python script.py <directory_path>")
        sys.exit(1)
    
    # Get the directory path from the command-line arguments
    directory_path = sys.argv[1]
    
    # Call the function with the directory path
    compress_all_jsons_in_directory(directory_path)
