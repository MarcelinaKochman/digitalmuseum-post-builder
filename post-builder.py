import glob
import os
import sys
from pathlib import Path

import instaloader
from PIL import Image, ImageFont, ImageDraw
from instaloader import Post

from instagram_downloader import download_instagram_post

TOP_MARGIN = 251

LEFT_MARGIN = 138

WHITE = (255, 255, 255)
IMAGE_SIZE = 1024
IMAGE_SIZE_X = 1000
IMAGE_SIZE_Y = 1333
MAX_PHOTO_SIZE = 757
POST_DIRECTORY_PATH = "post"


# def list_files_in_folder_with_extension(folder_path, extension):
#     folder = Path(folder_path)
#     files = [str(file) for file in folder.glob('**/*') if file.is_file()
#              and file.suffix == extension and not file.name.startswith('.')]
#     return files


def list_files_in_folder_with_extension(folder_path):
    folder = Path(folder_path)
    files = [str(file) for file in folder.glob('**/*') if file.is_file() and not file.name.startswith('.')]
    return files


def create_instagram_post():
    global L, post
    L = instaloader.Instaloader()
    postShortcode = sys.argv[1]
    post = Post.from_shortcode(L.context, postShortcode)
    return post


def resize_image(original_width, original_height, max_size):
    # Calculate aspect ratio
    aspect_ratio = original_width / original_height

    # Determine which side is longer
    if original_width < original_height:
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


# post = create_instagram_post()
# L.download_post(post, target=POST_DIRECTORY_PATH)

post_url = sys.argv[1]
login_username = ""
password = ""
download_folder = "downloads/"

username = download_instagram_post(login_username, password, post_url, download_folder)

# username = post.owner_profile.username
title = sys.argv[2]

imagesPaths = list_files_in_folder_with_extension(download_folder)

output_folder = "output/" + download_folder
files = glob.glob(output_folder + "*")
for f in files:
    os.remove(f)

for path in imagesPaths:
    resultImage = Image.new("RGB", (IMAGE_SIZE_X, IMAGE_SIZE_Y), WHITE)
    photo = Image.open(path)
    new_width, new_height = resize_image(photo.width, photo.height, MAX_PHOTO_SIZE)
    photo = photo.resize((new_width, new_height))
    x, y = calculate_photo_position(new_width, new_height, TOP_MARGIN, MAX_PHOTO_SIZE, IMAGE_SIZE_X)

    fontItalic = ImageFont.truetype("font/PoltawskiNowy-Italic.ttf", 24)
    fontBold = ImageFont.truetype("font/PoltawskiNowy-Bold.ttf", 24)

    draw = ImageDraw.Draw(im=resultImage)
    text_y = y + new_height
    draw.text(xy=(LEFT_MARGIN, text_y + 70), text="@" + username, font=fontItalic, fill='black', align='left')
    draw.text(xy=(LEFT_MARGIN, text_y + 40), text=title, font=fontBold, fill='black', align='left')


    resultImage.paste(photo, (x, y))
    print("Image processing completed!")
    output_path = output_folder + Path(path).stem + ".jpg"  # Zmiana rozszerzenia na .jpg
    resultImage.save(output_path, format="JPEG")
    print("Image saved! " + output_path)

