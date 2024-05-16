import shutil
import sys
from pathlib import Path

import instaloader
from instaloader import Post
from PIL import Image, ImageFont, ImageDraw

TOP_MARGIN = 81

LEFT_MARGIN = 138

WHITE = (255, 255, 255)
IMAGE_SIZE = 1024
MAX_PHOTO_SIZE = 757
INPUT_DIRECTORY_PATH = "input"


def list_files_in_folder_with_extension(folder_path):
    folder = Path(folder_path)
    files = [str(file) for file in folder.glob('**/*') if file.is_file()]
    return files


def resize_image(original_width, original_height, max_size):
    # Calculate aspect ratio
    aspect_ratio = original_width / original_height

    # Determine which side is longer
    if original_width > original_height:
        # If width is longer, calculate new width and height based on max_size
        new_width = max_size
        new_height = int(max_size / aspect_ratio)
    else:
        # If height is longer or they are equal, calculate new width and height based on max_size
        new_height = max_size
        new_width = int(max_size * aspect_ratio)

    return new_width, new_height


def calculate_photo_position(photo_width, photo_height, min_top_margin, max_photo_size, background_width):
    # Calculate margins
    x = (background_width - photo_width) // 2  # Center horizontally
    y = min_top_margin + ((max_photo_size - photo_height) // 2)  # Ensure minimum top margin of 81 pixels

    # Ensure minimum left margin of 138 pixels
    return x, y


username = sys.argv[1]
title = sys.argv[2]

imagesPaths = list_files_in_folder_with_extension(INPUT_DIRECTORY_PATH)

for path in imagesPaths:
    resultImage = Image.new("RGB", (IMAGE_SIZE, IMAGE_SIZE), WHITE)
    photo = Image.open(path)
    new_width, new_height = resize_image(photo.width, photo.height, MAX_PHOTO_SIZE)
    photo = photo.resize((new_width, new_height))
    x, y = calculate_photo_position(new_width, new_height, TOP_MARGIN, MAX_PHOTO_SIZE, IMAGE_SIZE)

    fontItalic = ImageFont.truetype("font/PoltawskiNowy-Italic.ttf", 24)
    fontBold = ImageFont.truetype("font/PoltawskiNowy-Bold.ttf", 24)

    draw = ImageDraw.Draw(im=resultImage)
    draw.text(xy=(LEFT_MARGIN, 920), text="@" + username, font=fontItalic, fill='black', align='left')
    draw.text(xy=(LEFT_MARGIN, 885), text=title, font=fontBold, fill='black', align='left')

    resultImage.paste(photo, (x, y))
    resultImage.save("output/" + path, "png")

