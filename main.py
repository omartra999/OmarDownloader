import os
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.popup import Popup
from kivy.uix.scrollview import ScrollView
from musicdownloader import MusicDownloader
from youtube import YoutubeDownloader

class DownloaderApp(App):
    def build(self):
        # Create a BoxLayout
        self.layout = BoxLayout(orientation='vertical', padding=10, spacing=10)
        
        # YouTube Downloader Section
        self.layout.add_widget(Label(text="YouTube Video URL:"))
        self.youtube_url_input = TextInput(hint_text="Enter YouTube URL")
        self.layout.add_widget(self.youtube_url_input)

        youtube_download_btn = Button(text="Download YouTube Video")
        youtube_download_btn.bind(on_press=self.download_youtube_video)
        self.layout.add_widget(youtube_download_btn)

        # Spotify Downloader Section
        self.layout.add_widget(Label(text="Spotify Track URL or ID:"))
        self.spotify_input = TextInput(hint_text="Enter Spotify URL or ID")
        self.layout.add_widget(self.spotify_input)

        spotify_download_btn = Button(text="Download Spotify Song")
        spotify_download_btn.bind(on_press=self.download_spotify_song)
        self.layout.add_widget(spotify_download_btn)

        return self.layout

    def get_save_path(self):
        """
        Determines the save path based on the platform.
        On Android: Uses the app's storage directory.
        On other platforms: Uses the "Downloads" directory.
        """
        if os.name == "posix":  # Likely Android
            save_path = "/storage/emulated/0/Download"  # Typical Android download path
        else:  # Likely Windows or Linux
            save_path = os.path.join(os.getcwd(), "videos")

        os.makedirs(save_path, exist_ok=True)
        return save_path

    def download_youtube_video(self, instance):
        url = self.youtube_url_input.text
        if not url:
            self.show_popup("Error", "Please enter a YouTube URL.")
            return

        save_path = self.get_save_path()
        try:
            # Use YoutubeDownloader class to download video
            YoutubeDownloader.download_video(url, save_path)
            self.show_popup("Success", "YouTube video downloaded successfully!")
        except Exception as e:
            self.show_popup("Error", f"Failed to download YouTube video: {e}")

    def download_spotify_song(self, instance):
        spotify_input = self.spotify_input.text
        if not spotify_input:
            self.show_popup("Error", "Please enter a Spotify URL or ID.")
            return

        save_path = self.get_save_path()
        try:
            # Use MusicDownloader class to search and download song
            music_downloader = MusicDownloader()
            music_downloader.search_song_on_spotify_and_youtube(spotify_input)
            self.show_popup("Success", "Spotify song downloaded successfully!")
        except Exception as e:
            self.show_popup("Error", f"Failed to download Spotify song: {e}")

    def show_popup(self, title, message):
        content = BoxLayout(orientation='vertical', padding=10)
        content.add_widget(Label(text=message))
        close_btn = Button(text="Close")
        content.add_widget(close_btn)

        popup = Popup(title=title, content=content, size_hint=(None, None), size=(300, 200))
        close_btn.bind(on_press=popup.dismiss)
        popup.open()

if __name__ == "__main__":
    DownloaderApp().run()
