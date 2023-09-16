import spotipy
from config import CLIENT_ID, CLIENT_SECRET, REDIRECT_URI, SCOPE
from spotipy.oauth2 import SpotifyOAuth, CacheFileHandler
from flask import Flask
from gist_request import GistRequest
import time
import threading

# Create a Flask app instance
app = Flask(__name__)

# Define a class for the SpotifySkipper
class SpotifySkipper:
    def __init__(self):
        # Initialize the Spotify client and GistRequest
        self.sp = self.initialize_spotify()
        self.gist_request = GistRequest()
        self.song_dict = self.gist_request.song_dict

    def initialize_spotify(self):
        # Create and configure the Spotify client for spotipy 
        return spotipy.Spotify(
            auth_manager=SpotifyOAuth(
                client_id=CLIENT_ID,
                cache_handler=CacheFileHandler(cache_path="t.cache"),
                client_secret=CLIENT_SECRET,
                redirect_uri=REDIRECT_URI,
                scope=SCOPE
            )
        )

    def check_song_loop(self, sp):
        while True:
            # Check the currently playing song on Spotify
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
            
            # Get song details and timestamp
            current_song_name = str(current_song_info["name"]).replace(" ", "").lower()
            current_time_ms = current_track["progress_ms"]
            current_time_seconds = int(current_time_ms / 1000)

            print("Current Song:", current_song_name)
            print("Current Time (seconds):", current_time_seconds)

            # Check if the song is in the dictionary and if it's time to skip
            if current_song_name in self.song_dict:
                print("Song Name:", current_song_name, "is in the list!")
                print("Timestamp to cancel on:", self.song_dict.get(current_song_name))
                if current_time_seconds >= int(self.song_dict.get(current_song_name)):
                    sp.next_track()
            
            time.sleep(1)

    def run(self):
        # Start the Flask app and other threads
        threading.Thread(target=app.run, kwargs={'host': '0.0.0.0', 'port': 8080}).start()
        threading.Thread(target=self.gist_request.fetch_loop).start()
        time.sleep(3)
        threading.Thread(target=self.check_song_loop(self.sp)).start()

@app.route('/')
def index():
    return "Flask running"

if __name__ == "__main__":
    skipper = SpotifySkipper()
    skipper.run()