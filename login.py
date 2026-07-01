import os
from instagrapi import Client
from dotenv import load_dotenv

load_dotenv()

cl = Client()
cl.login(os.environ["IG_USERNAME"], os.environ["IG_PASSWORD"])
cl.dump_settings("session.json")
