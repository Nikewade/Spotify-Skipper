import spotipy
from dotenv import load_dotenv
from spotipy.oauth2 import SpotifyOAuth, CacheFileHandler
from flask import Flask
import gist_request
import os
import time
import threading

def initialize_spotify():
    load_dotenv()
    CLIENT_ID = os.getenv("CLIENT_ID")
    CLIENT_SECRET = os.getenv("CLIENT_SECRET")
    REDIRECT_URI = "http://0.0.0.0:8888/callback"
    SCOPE = "user-modify-playback-state", "user-read-playback-state"

    return spotipy.Spotify(
        auth_manager=SpotifyOAuth(
            client_id=CLIENT_ID,
            cache_handler=CacheFileHandler(cache_path="t.cache"),
            client_secret=CLIENT_SECRET,
            redirect_uri=REDIRECT_URI,
            scope=SCOPE
        )
    )

def get_songs_loop():
    global songs_dict
    while True:
        print("Loading song list...")
        songs_dict = gist_request.fetch_loop()
        print(songs_dict)
        time.sleep(20)

def check_song_loop(sp):
    while True:
        current_track = sp.current_user_playing_track()
        print(songs_dict)
        if current_track is None:
            print("No track loaded.")
            time.sleep(1)
            continue
        
        if not current_track.get("is_playing", False):
            print("Track is paused or stopped.")
            time.sleep(1)
            continue
        
        current_song_info = current_track.get("item")
        
        if current_song_info is None or "name" not in current_song_info:
            print("No song information available.")
            time.sleep(1)
            continue
        
        current_song_name = str(current_song_info["name"]).replace(" ", "").lower()
        current_time_ms = current_track["progress_ms"]
        current_time_seconds = int(current_time_ms / 1000)

        print("Current Song:", current_song_name)
        print("Current Time (seconds):", current_time_seconds)

        if current_song_name in songs_dict:
            print("Song Name:", current_song_name, "is in the list!")
            print("Timestamp to cancel on:", songs_dict.get(current_song_name))
            if current_time_seconds >= int(songs_dict.get(current_song_name)):
                sp.next_track()
        
        time.sleep(1)

def main():
    threading.Thread(target=get_songs_loop).start()
    time.sleep(3)

    sp = initialize_spotify()
    threading.Thread(target=check_song_loop(sp)).start()

app = Flask(__name__)

@app.route('/')
def index():
    return "Flask running"

if __name__ == "__main__":
    main_thread = threading.Thread(target=main)
    main_thread.start()

    app.run(host="0.0.0.0",port=8080)