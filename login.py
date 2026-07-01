from instagrapi import Client


cl = Client()
cl.login(username, password)
cl.dump_settings("session.json")
