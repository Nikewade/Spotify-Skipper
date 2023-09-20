# Spotify Skipper

This is a Python application that allows you to skip songs on your Spotify playlist based on a predefined list of song names and timestamps. It periodically checks the currently playing song and if it matches a song in the list and reaches the specified timestamp, it skips to the next track.

## Table of Contents
- [Introduction](#introduction)
- [Features](#features)
- [Usage](#usage)
- [Configuration](#configuration)
- [How It Works](#how-it-works)
- [Contributing](#contributing)
- [License](#license)
- [Contact](#contact)

## Introduction
Spotify Skipper was initially created for personal use with a specific Spotify API key and hosted Gist file. However, it can be adapted for others to use with their own Spotify API key and Gist file. I currently have this running 24/7 via replit.com using flask and UptimeRobot. All I need to do to update the song list is to update the Gist. The code never has to be modified.

## Features
- Automatically skips songs based on a predefined list and timestamp.
- Periodically updates the song list from a hosted Gist on GitHub.
- Can run 24/7 on a hosting platform like Replit with Flask and UptimeRobot.
- Easy configuration using environment variables.

## Usage
To use Spotify Skipper, follow these steps:

1. Clone this repository to your local machine.
2. Configure your environment variables by creating a `.env` file with your Spotify API credentials and other necessary details. You'll need `CLIENT_ID`, `CLIENT_SECRET`, `GIST_ID`, and `FILENAME`. If you don't have a Spotify API key, there are many tutorials online on how to obtain one. I would recommend looking into something specific for the Spotipy library.
3. Create a virtual environment (recommended). 
4. Install the required Python libraries using `pip install -r requirements.txt`.
5. Run the application with `python main.py`.

## Configuration
Spotify Skipper relies on environment variables for configuration. Here are the variables you need to set in your `.env` file:

- `CLIENT_ID`: Your Spotify API client ID.
- `CLIENT_SECRET`: Your Spotify API client secret.
- `GIST_ID`: The Gist ID of your hosted song list on GitHub.
- `FILENAME`: The name of the Gist file containing your song list.

If you don't have a Spotify API key, you can find tutorials online on how to obtain one and connect it with Spotipy.

## How It Works
Spotify Skipper utilizes the Spotipy Python library, which allows you to manipulate the Spotify API with Python. It periodically checks the currently playing song and compares it to the song list hosted on a GitHub Gist. If a match is found, and the song reaches the specified timestamp, it skips to the next track on your Spotify playlist.

## Contributing
Contributions to Spotify Skipper are welcome! If you encounter issues, have suggestions, or want to improve the project, please feel free to submit issues or pull requests.

## License
This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

## Contact
- Email: nikewade1006@gmail.com
- Discord: nikewade
