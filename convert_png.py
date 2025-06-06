import os

from PIL import Image

# Set the folder path
folder_path = "assets/sprites/man"  # ⬅️ Replace with your actual folder

# Loop through all PNG files in the folder
for filename in os.listdir(folder_path):
    if filename.lower().endswith(".png"):
        full_path = os.path.join(folder_path, filename)

        try:
            img = Image.open(full_path)
            img.save(full_path, icc_profile=None)
            print(f"Cleaned: {filename}")
        except Exception as e:
            print(f"Failed to clean {filename}: {e}")
