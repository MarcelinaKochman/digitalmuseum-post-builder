import instaloader

login_username = "nieczyndrugiemu"
password = "M@r1995Koc"

L = instaloader.Instaloader()
L.login(login_username, password)  # logowanie

profile = instaloader.Profile.from_username(L.context, 'digitalaiartmuseum')

followers = []
for follower in profile.get_followers():
    followers.append((follower.username, follower.followers))

# Sortowanie od największych do najmniejszych
followers.sort(key=lambda x: x[1], reverse=True)

# Wyświetlenie top 10
for user in followers[:10]:
    print(user)
