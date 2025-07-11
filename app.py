import os
import subprocess
import argparse
import json

class YoutubeDownloader:

	def __init__(self):
		self.audio_save_path = os.path.expanduser("~/software/scrapers/youtube-downloader/audio")
		self.video_save_path = os.path.expanduser("~/software/scrapers/youtube-downloader/videos")
		self.tmp_save_path = os.path.expanduser("~/software/scrapers/youtube-downloader/tmp")
		
		# Ensure directories exist
		os.makedirs(self.audio_save_path, exist_ok=True)
		os.makedirs(self.video_save_path, exist_ok=True)
		os.makedirs(self.tmp_save_path, exist_ok=True)

	def format_title(self, title):
		title = title.replace('/','+')
		title = title.replace('.','_')
		return title

	def run(self):
		parser = argparse.ArgumentParser()
		parser.add_argument("-u", "--url", dest="url", help="Url")
		parser.add_argument("-a", "--audio", help="Save As Audio", action="store_true")
		parser.add_argument("-p", "--playlist", help="Playlist Url Provided", action="store_true")
		parser.add_argument("-o", "--output", help="Path to save output", dest="outputpath")
		parser.add_argument("-q", "--quality", help="Video quality (best, worst, 360p, 480p, 720p, 1080p, 4k)", dest="quality", default="best")
		parser.add_argument("-l", "--list-formats", help="List available formats", action="store_true")
		args = parser.parse_args()

		if args.url == None:
			print("Missing url and flag -u or --url. Use -h for help")
			return
		
		url = args.url
		download_video = False if args.audio == True else True
		quality = args.quality

		if args.outputpath != None:
			self.video_save_path = os.path.expanduser(args.outputpath)
			self.audio_save_path = os.path.expanduser(args.outputpath)

		if args.list_formats:
			self.list_formats(url)
		elif args.playlist == True:
			self.download_playlist(url, download_video, quality)
		else:
			self.download_single_video(url, download_video, quality)

	def get_video_info(self, url):
		"""Get video information using yt-dlp"""
		try:
			cmd = [
				'yt-dlp',
				'--dump-json',
				'--no-playlist',
				url
			]
			result = subprocess.run(cmd, capture_output=True, text=True, check=True)
			return json.loads(result.stdout)
		except subprocess.CalledProcessError as e:
			print(f"Error getting video info: {e}")
			return None

	def get_quality_format(self, quality):
		"""Convert quality parameter to yt-dlp format string"""
		# Using specific format IDs for better quality control
		quality_map = {
			'best': 'bestvideo*+bestaudio/best',
			'worst': 'worst[ext=mp4]/worst',
			'720p': '136+140/best[height<=720][ext=mp4]/best[height<=720]',  # 720p video + audio
			'1080p': '137+140/best[height<=1080][ext=mp4]/best[height<=1080]',  # 1080p video + audio
			'4k': '401+140/best[height<=2160][ext=mp4]/best[height<=2160]',  # 4K video + audio
			'480p': '135+140/best[height<=480][ext=mp4]/best[height<=480]',  # 480p video + audio
			'360p': '134+140/best[height<=360][ext=mp4]/best[height<=360]'   # 360p video + audio
		}
		return quality_map.get(quality.lower(), 'best[ext=mp4]/best')

	def download_single_video(self, url, download_video, quality):
		info = self.get_video_info(url)
		if not info:
			print("Could not get video information")
			return
		
		title = self.format_title(info['title'])
		print(f"Video: {info['title']} | Length = {info.get('duration', 'Unknown')}s")
		
		if download_video:
			# Download Video
			if os.path.exists(os.path.join(self.video_save_path, f"{title}.mp4")):
				if os.path.getsize(os.path.join(self.video_save_path, f"{title}.mp4")) > 0:
					print(f"Already downloaded: {title}")
					return
			self.download_video(url, title, quality)
		else:
			# Download Audio
			if os.path.exists(os.path.join(self.audio_save_path, f"{title}.mp3")):
				if os.path.getsize(os.path.join(self.audio_save_path, f"{title}.mp3")) > 0:
					print(f"Already downloaded: {title}")
					return
			self.download_audio(url, title)

	def download_playlist(self, url, download_video, quality):
		"""Download playlist using yt-dlp"""
		try:
			# Get playlist info
			cmd = ['yt-dlp', '--flat-playlist', '--dump-single-json', url]
			result = subprocess.run(cmd, capture_output=True, text=True, check=True)
			playlist_info = json.loads(result.stdout)
			
			print(f"Playlist: {playlist_info.get('title', 'Unknown')} | total = {len(playlist_info.get('entries', []))}")
			
			# Download each video in playlist
			for entry in playlist_info.get('entries', []):
				video_url = entry.get('url')
				if video_url:
					title = self.format_title(entry.get('title', 'Unknown'))
					
					if download_video:
						if os.path.exists(os.path.join(self.video_save_path, f"{title}.mp4")):
							if os.path.getsize(os.path.join(self.video_save_path, f"{title}.mp4")) > 0:
								print(f"Already downloaded: {title}")
								continue
						self.download_video(video_url, title, quality)
					else:
						if os.path.exists(os.path.join(self.audio_save_path, f"{title}.mp3")):
							if os.path.getsize(os.path.join(self.audio_save_path, f"{title}.mp3")) > 0:
								print(f"Already downloaded: {title}")
								continue
						self.download_audio(video_url, title)
						
		except subprocess.CalledProcessError as e:
			print(f"Error downloading playlist: {e}")

	def download_video(self, url, title, quality):
		"""Download video using yt-dlp"""
		try:
			output_path = os.path.join(self.video_save_path, f"{title}.mp4")
			format_str = self.get_quality_format(quality)
			cmd = [
				'yt-dlp',
				'-f', format_str,
				'--merge-output-format', 'mp4',
				'--recode-video', 'mp4',
				'-o', output_path,
				url
			]
			subprocess.run(cmd, check=True)
			print(f"Downloaded video: {title} (quality: {quality})")
		except subprocess.CalledProcessError as e:
			print(f"[ERROR] Could not download video: {title}\n{str(e)}")
			if os.path.exists(output_path):
				os.remove(output_path)

	def download_audio(self, url, title):
		"""Download audio using yt-dlp"""
		try:
			output_path = os.path.join(self.audio_save_path, f"{title}.mp3")
			cmd = [
				'yt-dlp',
				'-x',  # Extract audio
				'--audio-format', 'mp3',
				'--audio-quality', '0',  # Best quality
				'-o', output_path,
				url
			]
			subprocess.run(cmd, check=True)
			print(f"Downloaded audio: {title}")
		except subprocess.CalledProcessError as e:
			print(f"[ERROR] Could not download audio: {title}\n{str(e)}")
			if os.path.exists(output_path):
				os.remove(output_path)

	def list_formats(self, url):
		"""List available formats for a video"""
		try:
			cmd = ['yt-dlp', '-F', url]
			subprocess.run(cmd, check=True)
		except subprocess.CalledProcessError as e:
			print(f"Error listing formats: {e}")

if __name__ == '__main__':
	ytd = YoutubeDownloader()
	ytd.run()
