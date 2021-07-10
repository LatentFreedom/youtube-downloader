import os
import sys
import ssl
from pytube import YouTube
from pytube import Playlist
import ffmpeg
import argparse

# https://python-pytube.readthedocs.io/en/latest/api.html
# https://python-pytube.readthedocs.io/en/latest/user/streams.html
# https://support.plex.tv/articles/205568377-adding-local-artist-and-music-videos/

class YoutubeDownloader:

	def __init__(self):
		self.audio_save_path = os.path.expanduser("~/software/scrapers/youtube-downloader/audio")
		self.video_save_path = os.path.expanduser("~/software/scrapers/youtube-downloader/videos")
		self.tmp_save_path = os.path.expanduser("~/software/scrapers/youtube-downloader/tmp")

	def format_title(self,title):
		title = title.replace('/','+')
		title = title.replace('.','_')
		return title

	def run(self):

		parser = argparse.ArgumentParser()
		parser.add_argument("-u", "--url", dest="url", help="Url")
		parser.add_argument("-a", "--audio", help="Save As Audio", action="store_true")
		parser.add_argument("-p", "--playlist", help="Playlist Url Provided", action="store_true")
		parser.add_argument("-o", "--output", help="Path to save output", dest="outputpath")
		args = parser.parse_args()

		url = args.url
		download_video = False if args.audio == True else True

		if args.outputpath != None:
			self.video_save_path = os.path.expanduser(args.outputpath)
			self.audio_save_path = os.path.expanduser(args.outputpath)
		
		if args.playlist != None:
			self.download_playlist(url,download_video)
		else:
			self.download_single_video(url,download_video)

	def download_single_video(self,url,download_video):
		video = YouTube(url)
		print(video)
		print("Video: " + video.title + " | Length = " + str(video.length))

		title = self.format_title(video.title)
		
		if download_video:
			# Download Video Only
			files = os.listdir(self.video_save_path)
			if title + ".mp4" in files:
				print("Already downloaded: " + title)
			self.download_video(video)
		else:
			# Download Audio Only
			files = os.listdir(self.audio_save_path)
			if title + ".mp3" in files:
				print("Already downloaded: " + title)
			self.download_audio(video)
		

	def download_playlist(self,url,download_video):

		playlist = Playlist(url)
		print("Playlist: " + playlist.title + " | total = " + str(len(playlist.video_urls)))

		for video in playlist.videos:
			
			title = self.format_title(video.title)

			if download_video:
				# Download Video Only
				files = os.listdir(self.video_save_path)
				if title + ".mp4" in files:
					print("Already downloaded: " + title)
					continue
				self.download_video(video)
			else:
				# Download Audio Only
				files = os.listdir(self.audio_save_path)
				if title + ".mp3" in files:
					print("Already downloaded: " + title)
					continue
				self.download_audio(video)

	def download_video(self,video):
		title = self.format_title(video.title)
		# Get Audio & Video
		video_stream = video.streams.filter(file_extension='mp4',adaptive=True).first()
		audio_stream = video.streams.filter(only_audio=True,adaptive=True).first()
		print(video_stream)
		print(audio_stream)
		# Download
		video_stream.download(self.tmp_save_path,filename="tmp_video")
		audio_stream.download(self.tmp_save_path,filename="tmp_audio")
		# Combine & Format
		video_stream = ffmpeg.input(self.tmp_save_path+'/tmp_video.mp4')
		audio_stream = ffmpeg.input(self.tmp_save_path+'/tmp_audio.mp4')
		ffmpeg.output(audio_stream, video_stream, self.video_save_path+"/"+title+'.mp4').run()

	def download_audio(self,video):
		title = self.format_title(video.title)
		# Get Audio
		audio_stream = video.streams.filter(only_audio=True,adaptive=True).first()
		# Download
		audio_stream.download(self.tmp_save_path,filename="tmp_audio")
		# Format
		audio_stream = ffmpeg.input(self.tmp_save_path+'/tmp_audio.mp4')
		ffmpeg.output(audio_stream, self.audio_save_path+"/"+title+'.mp3').run()


if __name__ == '__main__':
    ssl._create_default_https_context = ssl._create_stdlib_context
    ytd = YoutubeDownloader()
    ytd.run()
