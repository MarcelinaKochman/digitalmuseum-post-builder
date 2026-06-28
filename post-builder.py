import glob
import sys
from pathlib import Path

import instaloader
from PIL import Image, ImageDraw, ImageFont
from instaloader import Post

import os

from instagram_downloader import download_instagram_post

os.environ["IMAGEIO_FFMPEG_EXE"] = "/opt/homebrew/bin/ffmpeg"  # lub to co zwróciło `which ffmpeg`

from moviepy.video.VideoClip import TextClip, ColorClip
from moviepy.video.compositing.CompositeVideoClip import CompositeVideoClip
from moviepy.video.fx.crop import crop
from moviepy.video.fx.resize import resize
from moviepy.video.io.VideoFileClip import VideoFileClip
import moviepy.config as mpy_config

from insagram_downloader_instaloader import download_instagram_post_instaloader

mpy_config.change_settings({"IMAGEMAGICK_BINARY": "/opt/homebrew/bin/convert"})

TOP_MARGIN = 251
TOP_MARGIN_REEL = 201

LEFT_MARGIN = 138

WHITE = (255, 255, 255)
IMAGE_SIZE = 1024
IMAGE_SIZE_X = 1000
IMAGE_SIZE_Y = 1333
IMAGE_SIZE_Y_REEL = 1777
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


def list_files_in_folder_with_extension_for_instaloader(folder_path):
    folder = Path(folder_path)
    valid_ext = {".jpg", ".jpeg", ".png", ".mp4", ".mov"}
    files = [
        str(file)
        for file in folder.glob("**/*")
        if file.is_file() and file.suffix.lower() in valid_ext
    ]
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
        new_height = int(max_size / aspect_ratio)
        new_width = max_size

    return new_width, new_height


def calculate_photo_position_reel(photo_width, photo_height, min_top_margin, max_photo_size, background_width):
    # Calculate margins
    x = (background_width - photo_width) // 2  # Center horizontally
    y = TOP_MARGIN_REEL  # Ensure minimum top margin of 81 pixels

    # Ensure minimum left margin of 138 pixels
    return x, y


def calculate_photo_position(photo_width, photo_height, min_top_margin, max_photo_size, background_width):
    # Calculate margins
    x = (background_width - photo_width) // 2  # Center horizontally
    y = min_top_margin + ((max_photo_size - photo_height) // 2)  # Ensure minimum top margin of 81 pixels

    # Ensure minimum left margin of 138 pixels
    return x, y


# post = create_instagram_post()
# L.download_post(post, target=POST_DIRECTORY_PATH)

post_url = sys.argv[1]
arg = sys.argv[2] if len(sys.argv) > 2 and sys.argv[2] else ""

is_reel = False

login_username = ""
password = ""
# login_username = ""
# password = ""
download_folder = "downloads"

output_folder = "output/" + download_folder + "/"
files = glob.glob(output_folder + "*")
for f in files:
    os.remove(f)

files = glob.glob(download_folder + "/" + "*")
for f in files:
    os.remove(f)

username = download_instagram_post_instaloader(post_url, download_folder)
# username = download_instagram_post(login_username, password, post_url, download_folder)
# username = "marcosmicozzi and @hef.prentice"
title = sys.argv[2]

# imagesPaths = list_files_in_folder_with_extension(download_folder)
imagesPaths = list_files_in_folder_with_extension_for_instaloader(download_folder)

size_y = IMAGE_SIZE_Y_REEL if is_reel else IMAGE_SIZE_Y

for path in imagesPaths:
    path = Path(path)
    output_path = Path(output_folder) / (path.stem + ".jpg")

    if path.suffix.lower() in ['.mp4', '.mov']:
        print(f"Processing video: {path.name}")

        clip = VideoFileClip(str(path))
        duration = clip.duration

        # Utwórz biały background
        background = ColorClip(size=(IMAGE_SIZE_X, size_y + 2), color=WHITE, duration=duration)

        # Przeskaluj i ustaw zdjęcie jak w obrazie
        frame = clip.get_frame(0)  # pierwsza klatka jako obraz
        img = Image.fromarray(frame)
        new_width, new_height = resize_image(img.width, img.height, MAX_PHOTO_SIZE)

        if is_reel:
            x, y = calculate_photo_position_reel(new_width, new_height, TOP_MARGIN, MAX_PHOTO_SIZE, IMAGE_SIZE_X)
        else:
            x, y = calculate_photo_position(new_width, new_height, TOP_MARGIN, MAX_PHOTO_SIZE, IMAGE_SIZE_X)

        # Przeskaluj oryginalne video do odpowiedniego rozmiaru
        resized_clip = resize(clip, newsize=(new_width, new_height)).set_position((x, y))

        # Teksty (tak samo jak w obrazie)
        composite_layers = [background, resized_clip]

        if title.strip():
            title_text = TextClip(
                title,
                fontsize=24,
                font="font/PoltawskiNowy-Bold.ttf",
                color='black',
                method='label'
            ).set_position((LEFT_MARGIN, y + new_height + 40)).set_duration(duration)
            composite_layers.append(title_text)

        username_text = TextClip(
            "@" + username,
            fontsize=24,
            font="font/PoltawskiNowy-Italic.ttf",
            color='black',
            method='label'
        ).set_position((LEFT_MARGIN, y + new_height + 70)).set_duration(duration)
        composite_layers.append(username_text)

        # Finalny klip
        print(is_reel)
        print(size_y)
        final_clip = CompositeVideoClip(composite_layers, size=(IMAGE_SIZE_X, size_y))

        # Zapisz
        output_video_path = Path(output_folder) / (path.stem + "_with_text.mp4")

        # Crop 1 pixel from the bottom
        cropped = crop(final_clip, y2=final_clip.h - 1)
        cropped.set_audio(clip.audio)

        # Write the result to a new file
        cropped.write_videofile(
            str(output_video_path),
            codec="libx264",
            audio_codec="aac"
        )
        print(f"Video saved! {output_video_path}")

    else:
        print(f"Processing image: {path.name}")
        resultImage = Image.new("RGB", (IMAGE_SIZE_X, size_y), WHITE)
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
        resultImage.save(output_path, format="JPEG")
        print("Image saved! " + str(output_path))
