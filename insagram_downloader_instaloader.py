import instaloader
from instaloader import Post
from pathlib import Path
import os

def download_instagram_post_instaloader(post_url, download_folder):
    # Utwórz folder, jeśli nie istnieje
    Path(download_folder).mkdir(parents=True, exist_ok=True)

    # Wyodrębnij shortcode z linka
    shortcode = post_url.rstrip('/').split('/')[-1]

    # Inicjalizacja Instaloadera
    L = instaloader.Instaloader(
        download_video_thumbnails=False,
        save_metadata=False,
        download_comments=False,
        compress_json=False
    )

    # Pobierz metadane posta
    post = Post.from_shortcode(L.context, shortcode)

    # Pobierz username autora posta
    username = post.owner_username

    # Pobierz wszystkie media (zdjęcia / film)
    L.download_post(post, target=download_folder)

    return username
