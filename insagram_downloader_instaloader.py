import os
import shutil
import requests
from pathlib import Path
from instagrapi import Client
from dotenv import load_dotenv

load_dotenv()

SESSION_FILE = os.path.join(os.path.dirname(__file__), "session.json")
USERNAME = os.environ["IG_USERNAME"]
PASSWORD = os.environ["IG_PASSWORD"]


def _get_client() -> Client:
    cl = Client()
    if os.path.exists(SESSION_FILE):
        cl.load_settings(SESSION_FILE)
    cl.login(USERNAME, PASSWORD)
    cl.dump_settings(SESSION_FILE)
    return cl


def _download_url(url: str, dest: Path):
    r = requests.get(str(url), timeout=30)
    r.raise_for_status()
    dest.write_bytes(r.content)


def download_instagram_post_instaloader(post_url: str, download_folder: str) -> str:
    folder = Path(download_folder)
    if folder.exists():
        shutil.rmtree(folder)
    folder.mkdir(parents=True)

    if not post_url.startswith("http"):
        post_url = f"https://www.instagram.com/p/{post_url}/"

    cl = _get_client()

    media_pk = cl.media_pk_from_url(post_url)
    media = cl.media_info(media_pk)
    username = media.user.username

    if media.resources:
        for i, resource in enumerate(media.resources):
            url = resource.video_url or resource.thumbnail_url
            ext = ".mp4" if resource.video_url else ".jpg"
            _download_url(url, folder / f"post_{i}{ext}")
    else:
        url = media.video_url or media.thumbnail_url
        ext = ".mp4" if media.video_url else ".jpg"
        _download_url(url, folder / f"post{ext}")

    return username
