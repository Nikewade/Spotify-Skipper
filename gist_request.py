import requests
import time
from config import GIST_ID, FILENAME

class GistRequest:
    
    def __init__(self):
        self.song_dict = {} # Initialize an empty dictionary to store song information

    def fetch_gist_raw_url(self, gist_id, filename):
        # Construct the GitHub Gist API URL
        gist_api_url = f"https://api.github.com/gists/{gist_id}"
        response = requests.get(gist_api_url) # Send a GET request to fetch the Gist data
        if response.status_code == 200:
            gist_data = response.json()
            if filename in gist_data['files']:
                raw_url = gist_data['files'][filename]['raw_url']  # Parse the JSON response and extract raw URL for the specified file
                return raw_url
        print("Failed to fetch Gist raw URL.")
        return None

    def fetch_gist_content(self, raw_url):
        # Send a GET request to fetch the content of the Gist file
        response = requests.get(raw_url)
        if response.status_code == 200:
            # Return the text content of the Gist file
            return response.text
        else:
            print("Failed to fetch Gist content.")
            return None

    def parse_content(self, content):
        # Split the content into lines and parse key-value pairs
        lines = content.strip().split('\n')
        for line in lines:
            key, value = map(str.strip, line.split('='))
            self.song_dict[key.lower()] = int(value)
    
    def update_song_dict(self):
        # Fetch the Gist data, parse it, and update the song dictionary
        raw_url = self.fetch_gist_raw_url(GIST_ID, FILENAME)
        if raw_url is not None:
            gist_content = self.fetch_gist_content(raw_url)
            if gist_content is not None:
                self.parse_content(gist_content)

    def fetch_loop(self):
        while True:
            # Periodically update the song dictionary
            self.update_song_dict()
            print("Loading song list...")
            self.song_dict = self.get_song_dict()
            print(self.song_dict)
            time.sleep(60)

    def get_song_dict(self):
        # Returns the current song dictionary
        return self.song_dict
