import requests
import sys

gist_id = "6a8f32105497119045aa9da583bf919d"
filename = "gistfile1.txt"
songs_dict = {}

def fetch_loop():
    raw_url = fetch_gist_raw_url(gist_id, filename)
    if raw_url is not None:
        gist_content = fetch_gist_content(raw_url)
        if gist_content is not None:
            parse_content(gist_content)
    return songs_dict

def fetch_gist_raw_url(gist_id, filename):
    gist_api_url = f"https://api.github.com/gists/{gist_id}"
    response = requests.get(gist_api_url)
    if response.status_code == 200:
        gist_data = response.json()
        if filename in gist_data['files']:
            raw_url = gist_data['files'][filename]['raw_url']
            return raw_url
    print("Failed to fetch Gist raw URL.")
    return None

def fetch_gist_content(raw_url):
    response = requests.get(raw_url)
    if response.status_code == 200:
        return response.text
    else:
        print("Failed to fetch Gist content.")
        return None

def parse_content(content):
    lines = content.strip().split('\n')
    for line in lines:
        key, value = map(str.strip, line.split('='))
        songs_dict[key.lower()] = int(value)
    return songs_dict

def main():
    fetch_loop()

if __name__ == "__main__":
    main()
