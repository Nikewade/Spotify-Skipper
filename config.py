import os 
from dotenv import load_dotenv

load_dotenv()

CLIENT_ID = os.getenv("CLIENT_ID")
CLIENT_SECRET = os.getenv("CLIENT_SECRET")
GIST_ID = os.getenv("GIST_ID")
FILENAME = os.getenv("FILENAME")

REDIRECT_URI = "http://0.0.0.0:8888/callback"
SCOPE = "user-modify-playback-state", "user-read-playback-state"