import spotipy
from dotenv import load_dotenv
from spotipy.oauth2 import SpotifyOAuth, CacheFileHandler
import gist_request
import os
import time
import threading

songs_dict = {}

def load_songs_from_file(file_path):
    songs = {}
    with open(file_path) as f:
        songs = dict(s.lower().replace(" ", "").strip().split("=") for s in f)
    return songs

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
    while True:
        print(gist_request.fetch_loop())
        time.sleep(10)

def check_song_loop(songs, sp):
    while True:
        current_track = sp.current_user_playing_track()

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

        if current_song_name in songs:
            print("Song Name:", current_song_name, "is in the list!")
            print("Timestamp to cancel on:", songs.get(current_song_name))
            if current_time_seconds >= int(songs.get(current_song_name)):
                sp.next_track()
        
        time.sleep(1)

def main():
    print("Loading song list...")
    threading.Thread(target=get_songs_loop).start()
    sp = initialize_spotify()
    threading.Thread(target=check_song_loop(songs_dict, sp)).start()

if __name__ == "__main__":
    main()