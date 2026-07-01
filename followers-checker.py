import os
import instaloader
from dotenv import load_dotenv

load_dotenv()

L = instaloader.Instaloader()
L.login(os.environ["IG_USERNAME_2"], os.environ["IG_PASSWORD_2"])  # logowanie

profile = instaloader.Profile.from_username(L.context, 'digitalaiartmuseum')

followers = []
for follower in profile.get_followers():
    followers.append((follower.username, follower.followers))

# Sortowanie od największych do najmniejszych
followers.sort(key=lambda x: x[1], reverse=True)

# Wyświetlenie top 10
for user in followers[:10]:
    print(user)
