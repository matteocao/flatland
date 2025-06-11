import os

from PIL import Image

for root, dirs, files in os.walk("assets"):
    for filename in files:
        if filename.lower().endswith(".png"):
            full_path = os.path.join(root, filename)

            try:
                img = Image.open(full_path)
                img.save(full_path, icc_profile=None)
                print(f"Cleaned: {full_path}")
            except Exception as e:
                print(f"Failed to clean {full_path}: {e}")
