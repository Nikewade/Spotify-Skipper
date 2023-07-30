import spotipy
from dotenv import load_dotenv
from spotipy.oauth2 import SpotifyOAuth
from subprocess import Popen
import os
import time

starttime = time.time()
stopTime = 1
sp = None
process = None
songs = {}

with open(os.getcwd() + "\data.txt") as f:
    songs = dict(s.lower().replace(" ", "").strip().split("=") for s in f)
    print(songs)


def initialize():
    global sp
    load_dotenv()
    CLIENT_ID = os.getenv("CLIENT_ID")
    CLIENT_SECRET = os.getenv("CLIENT_SECRET")
    REDIRECT_URI = "http://localhost:8888/callback"
    SCOPE = "user-modify-playback-state", "user-read-playback-state"


    sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id=CLIENT_ID,
                                                client_secret=CLIENT_SECRET,
                                                redirect_uri=REDIRECT_URI,
                                                scope=SCOPE))
    print("Init Done")

def open_spotify():
    global process
    spotify_path = r"C:\Users\nikew\AppData\Roaming\Spotify\Spotify.exe"
    process = Popen([spotify_path])
    check_song_loop()

def check_song_loop():
    while process.poll() == None:
        current_track = sp.current_user_playing_track()
        if current_track is not None and current_track["is_playing"]:
            current_song_name = str(current_track["item"]["name"]).replace(" ", "").lower()

            current_time_ms = current_track["progress_ms"]
            current_time_seconds = int(current_time_ms / 1000)

            print("Current Song:", current_song_name)
            print("Current Time (seconds):", current_time_seconds)

            if(current_song_name in songs):
                print("Song Name: " + current_song_name + " is in the list!")
                print("Timestamp to cancel on: " + songs.get(current_song_name))
                if(current_time_seconds >= int(songs.get(current_song_name))):
                    sp.next_track()
                    
        else:
            print("No track is currently playing.")
        time.sleep(1)


initialize()
open_spotify()


