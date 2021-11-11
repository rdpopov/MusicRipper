#!/usr/bin/python
from googlesearch import search
import requests
from bs4 import BeautifulSoup
import re
import os

def extract_name(inp):
    tmp = inp[inp.rindex('/'):]
    return tmp[:tmp.rindex('.')]


def get_url(name, subs):
    res = list(filter(lambda x: subs in x, search(name + ' lyrics', num_results=10)))
    if res is not None:
        if res.__len__() == 0:
            return None
        return res[0]
    return None


def get_artwork_location(name, subs):
    res = list(filter(lambda x: subs in x, search(name , num_results=10)))
    if res is not None:
        if res.__len__() == 0:
            return None
        return res[0]
    return None

class albumArtwork:
    cache_artwork = {}

    def __init__(self, path):
        albumArtwork.cache_artwork = {}
        self.path = path
        if not os.path.isdir(path):
            os.mkdir(path)

    def extract_artwork(self, soupp):
        art = soupp.find('img', {'alt': re.compile(r'album cover$')})
        print(art)
        if art:
            return art['src']
        return ""

    def get_artwork(self, metadata_dict):
        artist = metadata_dict['artist']
        album = metadata_dict['album']
        if album == None or album == 'Unknown':
            return None
        if (artist, album) in albumArtwork.cache_artwork:
            return albumArtwork.cache_artwork[(artist, album)]
        else:
            discogs_url = get_artwork_location("{} {} {}".format(artist, album, 'discogs'), 'discogs')
            discogs = requests.get(discogs_url).text
            thin = BeautifulSoup(discogs, 'html.parser')
            url = self.extract_artwork(thin)
            if url:
                img_data = requests.get(url).content
                img_name = '{}/{} {}'.format(self.path, artist, album)
                with open('{}/{} {}'.format(self.path, artist, album), 'wb') as handler:
                    handler.write(img_data)
                albumArtwork.cache_artwork[(artist, album)] = img_name
            else:
                albumArtwork.cache_artwork[(artist, album)] = None


class songMetadata:
    def __init__(self, path, useSite='azlyrics',artwork='discogs'):
        self.path = path
        self.name = extract_name(path)
        self.url = get_url(self.name, useSite)
        self.discogs_url = get_artwork_location(self.name, artwork)

    def extract_name(self, soup):
        return soup.find('div', {'class': 'ringtone'}).findNext('b').text.strip('"')

    def extract_artist(self, soup):
        art = soup.find('div', {'class': 'lyricsh'}).find('b').text
        if 'Lyrics' in art:
            return re.sub(' ?Lyrics', '', art)

    def extract_album(self, soup):
        alb = soup.find('div', {'class': 'songinalbum_title'})
        if 'album' in alb.text:
            return soup.find('div', {'class': 'songinalbum_title'}).find('b').text or ""
        else:
            return "Unknown"

    def extract_lyrics(self, soup):
        return re.sub('\n', '\\n', soup.find('div', {'class': 'ringtone'}).findNext('div').text).strip()


    def fetch_metadata(self):
        meta = {
                'name': '',
                'album': '',
                'artist': '',
                'lyrics': '',
                }
        if self.url is not None:
            text = requests.get(self.url).text
            soup = BeautifulSoup(text, 'html.parser')
            meta['name'] = self.extract_name(soup)
            meta['album'] = self.extract_album(soup)
            meta['artist'] = self.extract_artist(soup)
            meta['lyrics'] = self.extract_lyrics(soup)
        return meta


if __name__ ==  "__main__":
    artworker = albumArtwork('./.tmp')
    song = songMetadata("./Music/Like_Love/The Amity Affliction 'Like Love' Official Music Video.mp3")
    #song = songMetadata("./Music/Let_the_ocean_take_me/The Amity Affliction - Death's Hand.mp3")
    #song = songMetadata("./Music/A_Thousand_Suns/Blackout - Linkin Park.mp3")
    res = song.fetch_metadata()
    print(res['artist'])
    print(res['name'])
    print(res['album'])
    artworker.get_artwork(res)
    #print(res['lyrics'])
