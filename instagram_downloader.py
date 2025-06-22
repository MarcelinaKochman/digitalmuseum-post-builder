import os
import shutil
from instagrapi import Client

def download_instagram_post(username: str, password: str, post_url: str, save_path: str = "downloads/"):
    # Clear save_path directory
    if os.path.exists(save_path):
        shutil.rmtree(save_path)
    os.makedirs(save_path, exist_ok=True)

    cl = Client()
    cl.login(username, password)

    media_id = cl.media_id(cl.media_pk_from_url(post_url))
    media_info = cl.media_info(media_id)
    post_username = media_info.user.username

    if media_info.resources:
        for index, resource in enumerate(media_info.resources):
            file_url = resource.video_url if resource.video_url else resource.thumbnail_url
            cl.photo_download_by_url(file_url, save_path + f"post_{index}")
    else:
        file_url = media_info.video_url if media_info.video_url else media_info.thumbnail_url
        cl.photo_download_by_url(file_url, save_path + "post")

    print("Download complete!")
    return post_username

# Example usage:
# download_instagram_post("your_username", "your_password", "https://www.instagram.com/p/POST_ID/")


if __name__ == "__main__":
    # Example usage
    # post_url = input("Enter Instagram post URL: ")
    # username = input("Enter Instagram username (press Enter to skip): ").strip()
    # password = input("Enter Instagram password (press Enter to skip): ").strip()
    post_url = "https://www.instagram.com/p/DHeGtg7odkg/"
    username = "sophiaverney"
    password = "Sophi@2023Krakow"
    
    download_instagram_post(username, password, post_url)