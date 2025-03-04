import json
import os
import sys

def check_arguments():
    if len(sys.argv) < 3:
        print("Usage: python script.py <output_directory>")
        sys.exit(1)
    #print(f"[DEBUG] Output directory: {sys.argv[1]}")
    return sys.argv[1], sys.argv[2]

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

def main(output_directory, current_directory):
    # Compress all JSON files in the specified output directory
    compress_all_jsons_in_directory(output_directory)

# Allow the script to be called directly or from another script
if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python script.py <output_directory>")
        sys.exit(1)
    
    output_directory = sys.argv[1]
    main(output_directory)
