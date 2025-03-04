from PIL import Image
import os

def png_to_ico(png_file, output_dir=None, output_name="Icon_256", icon_sizes=[(16, 16), (32, 32), (48, 48), (64, 64), (128, 128), (256, 256)]):
    """
    Converts a PNG file to an ICO file.

    :param png_file: Path to the PNG file to convert.
    :param output_dir: Directory to save the output ICO file. If None, saves in the same directory as the PNG file.
    :param output_name: Name of the output ICO file (without extension).
    :param icon_sizes: List of icon sizes for the ICO file.
    """
    if not os.path.isfile(png_file):
        print("Error: The specified PNG file does not exist.")
        return
    
    if output_dir is None:
        output_dir = os.path.dirname(png_file)
    
    # Ensure output directory exists
    os.makedirs(output_dir, exist_ok=True)
    
    # Generate output ICO file path
    ico_file = os.path.join(output_dir, f"{output_name}.ico")
    
    try:
        # Open the PNG file
        img = Image.open(png_file)
        
        # Save the ICO file
        img.save(ico_file, format="ICO", sizes=icon_sizes)
        print(f"ICO file saved at: {ico_file}")
    except Exception as e:
        print(f"Error: {e}")

# Hardcoded file path
png_file_path = r"F:\SteamLibrary\steamapps\common\Earth Defense Force 6\EDF_ModloaderHead_B\Icon_2Kx2K_Source.png"
output_directory = r"F:\SteamLibrary\steamapps\common\Earth Defense Force 6\EDF_ModloaderHead_B"

# Run the conversion
png_to_ico(png_file_path, output_directory, output_name="Icon_256")
