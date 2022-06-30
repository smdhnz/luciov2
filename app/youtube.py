import os
import discord
import youtube_dl
from apiclient.discovery import build
from urllib.parse import urlparse, parse_qs


class Music():
    def __init__(self, title: str, artist: str | list[str], videoId: str, thumbnail: str):
        self.title = title
        self.artist = ' & '.join(artist) if isinstance(artist, list) else artist
        self.url = f'https://www.youtube.com/watch?v={videoId}'
        self.thumbnail = thumbnail


class Youtube():
    def __init__(self, api_key, ytdl_options, ffmpeg_options):
        self.ytapi = build('youtube', 'v3', developerKey=api_key)
        self.ytdl = youtube_dl.YoutubeDL(ytdl_options)
        self.ffmpeg_options = ffmpeg_options


    def get_video_id(self, url: str) -> str:
        return parse_qs(urlparse(url).query)['v'][0]


    def search(self, query: str) -> Music:
        if query.startswith('https://www.youtube.com'):
            result = self.ytapi.videos().list(
                part='id,snippet',
                id=self.get_video_id(query),
                maxResults=1,
            ).execute().get('items', [])[0]
            videoId = result['id']
        else:
            result = self.ytapi.search().list(
                part='id,snippet',
                q=query,
                type='video',
                maxResults=1,
                order='relevance'
            ).execute().get('items', [])[0]
            videoId = result['id']['videoId']

        return Music(
            result['snippet']['title'],
            result['snippet']['channelTitle'],
            videoId,
            result['snippet']['thumbnails']['default']['url'],
        )


    def create_stream_source(self, music: Music):
        info = self.ytdl.extract_info(music.url, download=False)
        return discord.PCMVolumeTransformer(
            discord.FFmpegPCMAudio(info["formats"][0]["url"], **self.ffmpeg_options),
            volume=0.05
        )

