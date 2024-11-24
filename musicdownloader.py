import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
from yt_dlp import YoutubeDL
import os
from dotenv import load_dotenv

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

    def get_song_details(self, song_id):
        """
        Retrieves song details from Spotify using the song's Spotify ID.
        """
        try:
            track = self.spotify.track(song_id)
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
        """
        try:
            search_query = f"{song_details['name']} {song_details['artist']} official audio"
            print(f"Searching for: {search_query}")
            
            ydl_opts = {
                'quiet': True,
                'format': 'bestaudio',  # Only download the best audio
                'noplaylist': True,  # Avoid playlist results
                'extractaudio': True,  # Extract audio if available
                'outtmpl': os.path.join(os.getcwd(), '%(title)s.%(ext)s'),  # Output path
            }

            with YoutubeDL(ydl_opts) as ydl:
                ydl.download([f"ytsearch:{search_query}"])

            print(f"Search complete. Audio downloaded successfully.")
        except Exception as e:
            print(f"An error occurred while searching on YouTube: {e}")

    
    def search_song_on_spotify_and_youtube(self, song_id):
        """
        Searches for a song on Spotify and then finds it on YouTube.
        """
        song_details = self.get_song_details(song_id)
        if song_details:
            print(f"Song details retrieved: {song_details}")
            self.search_youtube(song_details)
        else:
            print("Failed to retrieve song details.")

