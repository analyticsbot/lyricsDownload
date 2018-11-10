"""Module to download lyrics from lyrics.wikia.com"""

# import required modules
import requests
from bs4 import BeautifulSoup
import sys, codecs, json
import random
import wikipedia
try:
	from .config import *
except:
	from config import *

class LyricsWikia():

	def __init__(self):
		"""
		initialize the base url and a random header for the get request
		"""
		self.base_url = 'http://lyrics.wikia.com/'
		self.header = {'User-Agent': random.choice(user_agents)}

	@staticmethod
	def checkNone(name):
		"""
		Function to return the name with whitespaces replaced with underscore

		Args:
			name: str
		Returns:
			str
		"""
		if name:
			return name.replace(' ', '_')
		else:
			return name

	@staticmethod
	def getWikiData(name):
		"""
		Function to get wikipedia summary for a given subject

		Args:
			name: str
		Returns:
			str
		"""
		try:
			return wikipedia.summary(name)
		except:
			return 'Wikipedia did not return back summary for ' + name

	def getAlbumAndTracks(self, singerName, wikiData=False):
		"""
		Function to get albums and tracks for a given singer

		Args:
			singerName: str
			wikiData: boolean
		Returns:
			json
			{'album_name': {'url': 'https://www.abc.com', 'songs': ['song1', 'song2']}}
		"""
		self.singerName = self.checkNone(singerName)
		self.wikiData = wikiData

		album_url = self.base_url + self.singerName
		source_code = requests.get(album_url, self.header).content
		soup = BeautifulSoup(source_code, features="lxml")

		album_spans = soup.findAll('span',{'class':'mw-headline'})
		album_data = {}

		if self.wikiData:
			album_data['singerWiki'] = self.getWikiData(self.singerName)

		for album in album_spans:
			if 'information' in album.get_text().strip() or 'Songs Featuring' in album.get_text().strip() \
			or 'External links' in album.get_text().strip() or 'Other Songs' in album.get_text().strip():
				continue
			try:
				album_data[album.get_text().strip()] = {}
				album_data['albumWiki'] = self.getWikiData(album.get_text().strip())
			except:
				break
			try:
				album_data[album.get_text()]['url'] = self.base_url + album.findNext('a')['href'][1:]
			except:
				pass
			try:
				album_data[album.get_text()]['songs'] =  [song.get_text().strip() for song in album.findNext('ol').findAll('li')]
			except:
				pass
		return album_data

	def getAlbumLyrics(self, singerName, albumName, fileName=False):
		"""
		Function to get the lyrics for all the songs in a given album for a given singer

		Args:
			singerName: str
			albumName: str
			fileName: boolean
		Returns:
			boolean
		"""
		self.singerName = self.checkNone(singerName)
		self.albumName = self.checkNone(albumName)
		albumTracks = self.getAlbumAndTracks(singerName)
		for album, songs in albumTracks.items():
			if album.replace(' ', '_') != self.albumName:
				continue
			for songName in songs['songs']:
				self.getSongLyrics(self.singerName, songName, fileName=album + '_' + songName + '.txt')
		return True

	def getSongLyrics(self, singerName, songName, fileName=False):
		"""
		Function to get the lyrics for a given song for a given singer

		Args:
			singerName: str
			songName: str
			fileName: boolean
		Returns:
			str
		"""
		self.singerName = self.checkNone(singerName)
		self.songName = self.checkNone(songName)
		song_url = self.base_url + self.singerName + ":" + self.songName
		resp = requests.get(song_url, self.header)
		soup = BeautifulSoup(resp.content)
		lyricsbox = soup.find("div",{'class':'lyricbox'})
		if lyricsbox is None:
			return "Song or Singer does not exist or the API does not have Lyrics" + self.singerName + " and song " + self.songName
		
		lyrics = lyricsbox.getText(separator='\n')

		if fileName:
			if isinstance(fileName, str):
				f = open(fileName, 'w')
				f.write(lyrics)
				f.close()
			else:
				f = open(self.singerName + "_" + self.songName + ".txt", "w")
				f.write(lyrics)
				f.close()
		return lyrics

def main():
	abc = LyricsWikia()
	print (abc.getAlbumAndTracks(singerName='Linkin Park'))

if __name__=='__main__':
	main()