from yt_dlp import YoutubeDL
import os

class YoutubeDownloader():
    
    @staticmethod
    def download_video(url, save_path='videos'):
        try:
            # Ensure the 'videos' folder exists (default to 'videos' if no path is provided)
            if not os.path.exists(save_path):
                os.makedirs(save_path)
            
            # Configure yt-dlp options
            ydl_opts = {
                'format' : 'best[ext=mp4]',  # Best quality mp4 format
                'outtmpl' : os.path.join(save_path, '%(title)s.%(ext)s'),  # Save path with video title
            }
            
            with YoutubeDL(ydl_opts) as ydl:
                ydl.download([url])
            print("Video downloaded successfully")
        except Exception as e:
            print(f"An error occurred: {e}")
            
    @staticmethod
    def download_audio(url, save_path='music', preferred_codec="mp3", preferred_quality="320"):
        try:
            # Ensure the save_path exists (default to 'music' if no path is provided)
            if not os.path.exists(save_path):
                os.makedirs(save_path)

            # Configure yt-dlp options for high-quality audio
            ydl_opts = {
                'format': 'bestaudio/best',  # Get the best audio format available
                'postprocessors': [{
                    'key': 'FFmpegExtractAudio',
                    'preferredcodec': preferred_codec,  # Codec: mp3, wav, flac, etc.
                    'preferredquality': preferred_quality,  # Quality: 128, 192, 320 kbps
                }],
                'outtmpl': os.path.join(save_path, '%(title)s.%(ext)s'),  # Save with audio title
            }

            # Download the audio
            with YoutubeDL(ydl_opts) as ydl:
                ydl.download([url])
            print(f"Audio downloaded successfully in {preferred_codec} format at {preferred_quality} kbps.")
        except Exception as e:
            print(f"An error occurred: {e}")

    @staticmethod
    def download_playlist(url, save_path='videos'):
        try:
            # Ensure the save_path exists
            if not os.path.exists(save_path):
                os.makedirs(save_path)
            
            # Configure yt-dlp options for downloading a playlist
            ydl_opts = {
                'format': 'best[ext=mp4]',  # Best quality mp4 format
                'outtmpl': os.path.join(save_path, '%(playlist)s', '%(title)s.%(ext)s'),  # Save playlist in a folder
                'noplaylist': False,  # Allow downloading the entire playlist
                'ignoreerrors': True,  # Ignore errors and continue downloading
            }
            
            with YoutubeDL(ydl_opts) as ydl:
                ydl.download([url])
            print("Playlist downloaded successfully")
        except Exception as e:
            print(f"An error occurred while downloading the playlist: {e}")
