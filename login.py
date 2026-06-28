from instagrapi import Client

username = "sophiaverney"
password = "Sophi@2023Krakow"

cl = Client()
cl.login(username, password)
cl.dump_settings("session.json")