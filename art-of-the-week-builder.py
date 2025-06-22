import instaloader
import os
import glob
from datetime import datetime, timedelta


def download_posts():
    global start_date, end_date, most_liked_post, max_likes
    # Initialize Instaloader object
    L = instaloader.Instaloader()
    # Log in (optional)
    # L.login('your_username', 'your_password')
    # Load the profile (replace 'profile_username' with the actual username)
    profile = instaloader.Profile.from_username(L.context, 'digitalaiartmuseum')
    # Define the date range
    start_date = datetime.today() - timedelta(days=14)  # Starting date
    end_date = datetime.today()  # Ending date
    # Variables to track the most liked post
    most_liked_post = None
    max_likes = 0
    # Use a filter to get only the posts within the date range
    posts = profile.get_posts()
    for post in posts:
        # Filter by date_utc (post.date_utc in UTC timezone)
        if start_date <= post.date_utc <= end_date:
            L.download_post(post, target=f"{profile.username}_posts")
            # Check if the current post has more likes than the tracked one
            if post.likes > max_likes:
                max_likes = post.likes
                most_liked_post = post
    return most_liked_post

files = glob.glob('digitalaiartmuseum_posts/*')
for f in files:
    os.remove(f)

most_liked_post = download_posts()


# Display the result
if most_liked_post:
    print(f"The most liked post between {start_date} and {end_date} has {max_likes} likes.")
    print(f"Post URL: https://www.instagram.com/p/{most_liked_post.shortcode}/")
else:
    print("No posts found in the specified date range.")