import os
from PySide6.QtWidgets import QApplication, QWidget, QVBoxLayout, QLabel, QLineEdit, QPushButton, QMessageBox
from PySide6.QtCore import Qt
from yt_dlp import YoutubeDL
from musicdownloader import MusicDownloader  
from youtube import YoutubeDownloader  

class DownloaderApp(QWidget):
    def __init__(self):
        super().__init__()
        self.init_ui()

    def init_ui(self):
        # Set up the main window
        self.setWindowTitle("Downloader App")
        self.setGeometry(300, 300, 400, 200)

        # Layout
        layout = QVBoxLayout()

        # YouTube Downloader Section
        layout.addWidget(QLabel("YouTube Video URL:"))
        self.youtube_url_input = QLineEdit()
        layout.addWidget(self.youtube_url_input)

        youtube_download_btn = QPushButton("Download YouTube Video")
        youtube_download_btn.clicked.connect(self.download_youtube_video)
        layout.addWidget(youtube_download_btn)

        # Spotify Downloader Section
        layout.addWidget(QLabel("Spotify Track ID:"))
        self.spotify_id_input = QLineEdit()
        layout.addWidget(self.spotify_id_input)

        spotify_download_btn = QPushButton("Download Spotify Song")
        spotify_download_btn.clicked.connect(self.download_spotify_song)
        layout.addWidget(spotify_download_btn)

        # Set layout
        self.setLayout(layout)

    def download_youtube_video(self):
        url = self.youtube_url_input.text()
        if not url:
            QMessageBox.warning(self, "Error", "Please enter a YouTube URL.")
            return

        save_path = os.path.join(os.getcwd(), "downloads")
        try:
            YoutubeDownloader.download_video(url, save_path)
            QMessageBox.information(self, "Success", "YouTube video downloaded successfully!")
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to download YouTube video: {e}")

    def download_spotify_song(self):
        track_id = self.spotify_id_input.text()
        if not track_id:
            QMessageBox.warning(self, "Error", "Please enter a Spotify Track ID.")
            return

        save_path = os.path.join(os.getcwd(), "downloads")
        try:
            music_downloader = MusicDownloader()
            music_downloader.search_song_on_spotify_and_youtube(track_id)
            QMessageBox.information(self, "Success", "Spotify song downloaded successfully!")
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to download Spotify song: {e}")


if __name__ == "__main__":
    import sys
    app = QApplication(sys.argv)

    # Create and show the downloader app
    downloader_app = DownloaderApp()
    downloader_app.show()

    sys.exit(app.exec())
