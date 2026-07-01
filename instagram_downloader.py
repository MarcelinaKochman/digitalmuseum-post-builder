import os
import shutil
import requests
from pathlib import Path
from instagrapi import Client

SESSION_FILE = os.path.join(os.path.dirname(__file__), "session.json")


def _get_client(username: str, password: str) -> Client:
    cl = Client()
    if os.path.exists(SESSION_FILE):
        cl.load_settings(SESSION_FILE)
    cl.login(username, password)
    cl.dump_settings(SESSION_FILE)
    return cl


def _download_url(url: str, dest: Path):
    r = requests.get(str(url), timeout=30)
    r.raise_for_status()
    dest.write_bytes(r.content)


def download_instagram_post(username: str, password: str, post_url: str, save_path: str = "downloads") -> str:
    folder = Path(save_path)
    if folder.exists():
        shutil.rmtree(folder)
    folder.mkdir(parents=True)

    cl = _get_client(username, password)

    media_pk = cl.media_pk_from_url(post_url)
    media = cl.media_info(media_pk)
    post_username = media.user.username

    if media.resources:
        for i, resource in enumerate(media.resources):
            url = resource.video_url or resource.thumbnail_url
            ext = ".mp4" if resource.video_url else ".jpg"
            _download_url(url, folder / f"post_{i}{ext}")
    else:
        url = media.video_url or media.thumbnail_url
        ext = ".mp4" if media.video_url else ".jpg"
        _download_url(url, folder / f"post{ext}")

    print("Download complete!")
    return post_username
