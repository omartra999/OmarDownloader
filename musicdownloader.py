import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
from yt_dlp import YoutubeDL
import os
import re
from dotenv import load_dotenv
import logging

# Load environment variables from .env
load_dotenv()

class MusicDownloader:
    
    def __init__(self):
        # Get Spotify credentials from environment variables
        self.spotify_client_id = os.getenv("SPOTIFY_CLIENT_ID")
        self.spotify_client_secret = os.getenv("SPOTIFY_CLIENT_SECRET")
        self.spotify = self.authenticate_spotify()

    def authenticate_spotify(self):
        """
        Authenticates with Spotify API using Client Credentials Flow.
        """
        client_credentials_manager = SpotifyClientCredentials(
            client_id=self.spotify_client_id, 
            client_secret=self.spotify_client_secret
        )
        return spotipy.Spotify(client_credentials_manager=client_credentials_manager)

    def extract_track_id(self, spotify_input):
        """
        Extracts the track ID from a Spotify URL or validates if it's already an ID.
        """
        if "open.spotify.com" in spotify_input:
            match = re.search(r"track/([a-zA-Z0-9]+)", spotify_input)
            if match:
                return match.group(1)
            else:
                raise ValueError("Invalid Spotify URL.")
        return spotify_input  # Assume input is a valid track ID if it's not a URL

    def get_song_details(self, track_input):
        """
        Retrieves song details from Spotify using the song's Spotify track ID or URL.
        """
        try:
            track_id = self.extract_track_id(track_input)
            track = self.spotify.track(track_id)
            song_details = {
                'name': track['name'],
                'artist': track['artists'][0]['name'],
                'album': track['album']['name'],
            }
            return song_details
        except Exception as e:
            print(f"An error occurred while retrieving song details: {e}")
            return None

    def search_youtube(self, song_details):
        """
        Searches YouTube for the song based on the song details (name + artist).
        Downloads the audio as MP3 into a 'music' folder.
        """
        try:
            # Search query
            search_query = f"{song_details['name']} {song_details['artist']} "
            print(f"Searching for: {search_query}")
            
            # Set up the music folder path
            music_folder = os.path.join(os.getcwd(), 'music')
            
            # Ensure the 'music' folder exists
            if not os.path.exists(music_folder):
                os.makedirs(music_folder)
            
            # Set up logging
            logging.basicConfig(level=logging.INFO)
            logger = logging.getLogger()

            # yt-dlp options
            ydl_opts = {
                'quiet': False,  # Enable verbose logging to track what's happening
                'format': 'bestaudio/best',  # Download the best available audio
                'noplaylist': True,  # Avoid playlist results
                'extractaudio': True,  # Extract audio only (not video)
                'audioquality': 1,  # Highest audio quality
                'outtmpl': os.path.join(music_folder, '%(title)s.%(ext)s'),  # Save to 'music' folder
                'postprocessors': [{
                    'key': 'FFmpegExtractAudio',  # Use FFmpeg to extract and convert audio
                    'preferredcodec': 'mp3',  # Convert to MP3
                    'preferredquality': '192',  # Set bitrate to 192kbps
                }],
                'logger': logger  # Add logger to yt-dlp options
            }

            # Perform download
            with YoutubeDL(ydl_opts) as ydl:
                ydl.download([f"ytsearch:{search_query}"])

            print(f"Search complete. Audio downloaded and converted to MP3 successfully.")
        
        except Exception as e:
            print(f"An error occurred while searching on YouTube: {e}")

    def search_song_on_spotify_and_youtube(self, track_input):
        """
        Searches for a song on Spotify (via URL or ID) and then finds it on YouTube.
        """
        song_details = self.get_song_details(track_input)
        if song_details:
            print(f"Song details retrieved: {song_details}")
            self.search_youtube(song_details)
        else:
            print("Failed to retrieve song details.")
