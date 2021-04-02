import os
import sys
from pytube import YouTube
from pytube import Playlist
import ffmpeg

# https://python-pytube.readthedocs.io/en/latest/api.html
# https://python-pytube.readthedocs.io/en/latest/user/streams.html
# https://support.plex.tv/articles/205568377-adding-local-artist-and-music-videos/

class YoutubeDownloader:

	def __init__(self):
		self.audio_save_path = self.directory = os.path.expanduser("~/software/scrapers/youtube-downloader/audio")
		self.video_save_path = self.directory = os.path.expanduser("~/software/scrapers/youtube-downloader/videos")
		self.tmp_save_path = self.directory = os.path.expanduser("~/software/scrapers/youtube-downloader/tmp")

	def run(self):
		if len(sys.argv) != 2:
			print("Need playlist url")

		url = sys.argv[1]
		self.download_playlist(url)
		

	def download_playlist(self,url,video=True):
		
		playlist = Playlist(url)
		print("Playlist: " + playlist.title + " | total = " + str(len(playlist.video_urls)))

		for video in playlist.videos:
			title = video.title.replace('/','+')
			
			if video:
				# Download Video Only
				files = os.listdir(self.video_save_path)
				if title + ".mp4" in files:
					print("Already downloaded: " + title)
					continue
				self.download_video(video)
			else:
				# Download Audio Only
				files = os.listdir(self.audio_save_path)
				if video.title+".mp3" in files:
					print("Already downloaded: " + title)
					continue
				self.download_audio(video)

	def download_video(self,video):
		# Get Audio & Video
		video_stream = video.streams.filter(file_extension='mp4',adaptive=True).first()
		audio_stream = video.streams.filter(only_audio=True,adaptive=True).first()
		print(video_stream)
		print(audio_stream)
		# Download
		video_stream.download(TMP_PATH,filename="tmp_video")
		audio_stream.download(TMP_PATH,filename="tmp_audio")
		# Combine
		video_stream = ffmpeg.input(TMP_PATH+'tmp_video.mp4')
		audio_stream = ffmpeg.input(TMP_PATH+'tmp_audio.mp4')
		ffmpeg.output(audio_stream, video_stream, SAVE_PATH+video.title+'.mp4').run()

	def download_audio(self,video):
		files = os.listdir(self.audio_save_path)
		# Get Audio
		audio_stream = video.streams.filter(only_audio=True,adaptive=True).first()
		# Download
		audio_stream.download(TMP_PATH,filename="tmp_audio")
		ffmpeg.output(audio_stream, None, AUDIO_SAVE_PATH+video.title+'.mp3').run()

if __name__ == '__main__':
	ytd = YoutubeDownloader()
	ytd.run()
