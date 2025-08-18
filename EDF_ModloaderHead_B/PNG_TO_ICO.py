from PIL import Image
import os

input_png = "Icon_2Kx2K_Source.png"  # Source 2K image
output_ico = "Icon_256.ico"

# Sizes Windows expects for crisp icons
sizes = [256, 128, 64, 48, 32, 24, 16]

# Open and convert
img = Image.open(input_png).convert("RGBA")

# Resize and collect all layers
img.save(output_ico, format='ICO', sizes=[(s, s) for s in sizes])
print(f"✅ Icon saved with layers: {sizes}")
