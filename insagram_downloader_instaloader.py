import os
from pathlib import Path
from instagrapi import Client
from instagrapi.exceptions import LoginRequired

SESSION_FILE = os.path.join(os.path.dirname(__file__), "session.json")



def _get_client() -> Client:
    cl = Client()
    if os.path.exists(SESSION_FILE):
        cl.load_settings(SESSION_FILE)
    cl.login(USERNAME, PASSWORD)
    cl.dump_settings(SESSION_FILE)
    return cl


def download_instagram_post_instaloader(post_url: str, download_folder: str) -> str:
    Path(download_folder).mkdir(parents=True, exist_ok=True)

    if not post_url.startswith("http"):
        post_url = f"https://www.instagram.com/p/{post_url}/"

    cl = _get_client()

    media_pk = cl.media_pk_from_url(post_url)
    media = cl.media_info(media_pk)
    username = media.user.username

    if media.resources:
        for i, resource in enumerate(media.resources):
            url = resource.video_url or resource.thumbnail_url
            cl.photo_download_by_url(str(url), str(Path(download_folder) / f"post_{i}"))
    else:
        url = media.video_url or media.thumbnail_url
        cl.photo_download_by_url(str(url), str(Path(download_folder) / "post"))

    return username
