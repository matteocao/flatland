import argparse
import os

from PIL import Image


def split_image_grid(image_path, rows, cols, output_folder):
    image = Image.open(image_path)
    os.makedirs(output_folder, exist_ok=True)

    tile_width = image.width // cols
    tile_height = image.height // rows

    for row in range(rows):
        for col in range(cols):
            box = (
                col * tile_width,
                row * tile_height,
                (col + 1) * tile_width,
                (row + 1) * tile_height,
            )
            tile = image.crop(box)
            tile.save(os.path.join(output_folder, f"tile_{row}_{col}.png"))


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Split an image into an x by y grid.")
    parser.add_argument("-x", "--cols", type=int, required=True, help="Number of columns")
    parser.add_argument("-y", "--rows", type=int, required=True, help="Number of rows")
    parser.add_argument("-f", "--file", type=str, required=True, help="Path to input image file")
    parser.add_argument("-o", "--output", type=str, default="tiles", help="Output folder name")

    args = parser.parse_args()

    split_image_grid(args.file, args.rows, args.cols, args.output)
