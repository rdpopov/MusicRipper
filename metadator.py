#!/usr/bin/python
from googlesearch import search
import requests
from bs4 import BeautifulSoup
from multiprocessing import Lock
import re
import os
import glob
import eyed3
import string


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

def match_helper(url,keywords):
    res = 0
    for i in keywords:
        if i in url:
            res = res + 1
    return res



def get_artwork_location(name, subs,keywords: list):
    # TODO: write a more intelligent filter
    # NOTE: make it so filter looks for keywords in the url, discogs does that.
    # so the one with the most amount of matches is the closest

    res = list(filter(lambda x: subs in x, search(name, num_results=10)))

    if res is not None:
        if res.__len__() == 0:
            return None
        else:
            lst = map(lambda x: (x,match_helper(x, keywords)),res)
            return max(lst,lambda x: x[1])[0]
    return None


class Requester:
    def __init__(self, site, cont_tag='table', clss='table table-striped table-bordered', cols={'ip': 0, 'port': 1}):
        self._site = site
        self._cont_tag = cont_tag
        self._clss = clss
        self._cols = cols
        self._lock = Lock()
        self._prox_list = []
        self.get_proxies()
        # if not work urllib3=1.23 ???

    def get_proxies(self, lck=True):
        if lck:
            self._lock.acquire()

        
        prox_list = BeautifulSoup(requests.get(self._site).text, 'html.parser').find(self._cont_tag, {'class': self._clss})
        # print (prox_list)
        # exit(0)
        children = prox_list.findChildren("tr")
        result = []
        for entry in children:
            tds = entry.findChildren("td")
            if tds:
                result.append((tds[self._cols['ip']].text, tds[self._cols['port']].text))

        self._prox_list = result
        if lck:
            self._lock.release()

    def get_proxy_for_request(self):
        self._lock.acquire()
        if self._prox_list.__len__() == 0:
            self.get_proxies(lck=False) # since we lock it inside and we already acquired the lock we wont be able to lock it
        ent = self._prox_list[0]
        self._prox_list.pop(0)
        self._lock.release()
        return {'https': 'https://{}:{}'.format(*ent),'http': 'http://{}:{}'.format(*ent),}

    def make_request(self, req_to):
        # if not work urllib=1.23 ???
        res = None
        while res is None:
            try:
                prox = self.get_proxy_for_request()
                # print(prox)
                res = requests.get(req_to, verify=False, proxies=prox, timeout=60)
                #print (res)
                res = res.text
                #print(res)
                if 'Access Denied' in res or 'unusual activity from your IP address' in res or 'violation of your Internet usage policy' in res:
                    res = None
            except OSError:
                continue
                # try again if anything happens
        return res


class albumArtwork:
    cache_artwork = {}

    def __init__(self, path):
        albumArtwork.cache_artwork = {}
        self.path = path
        if not os.path.isdir(path):
            os.mkdir(path)

    def extract_artwork(self, soupp):
        art = soupp.find('img', {'alt': re.compile(r'album cover$')})
        if art:
            return art['src']
        return ""

    def get_artwork(self, metadata_dict):
        artist = metadata_dict['artist']
        album = metadata_dict['album']
        if album is None or album == 'Unknown':
            album = metadata_dict['name']
        if (artist, album) in albumArtwork.cache_artwork:
            return albumArtwork.cache_artwork[(artist, album)]
        else:
            keywords = album.split() + artist.split()
            keywords = list(map(lower,keywords))
            discogs_url = get_artwork_location("{} {} {}".format(artist, album, 'discogs'), 'discogs.com',keywords)
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
            return albumArtwork.cache_artwork[(artist, album)]



class songMetadata:
    def __init__(self, path,requ ,useSite='azlyrics.com',artwork='discogs'):
        self.path = path
        self.name = extract_name(path)
        self.url = get_url(self.name, useSite)
        self.requester = requ
        self.discogs_url = get_artwork_location(self.name, artwork)

    def extract_name(self, soup):
        return soup.find('div', {'class': 'ringtone'}).findNext('b').get_text().strip('"')

    def extract_artist(self, soup):
        art = soup.find('div', {'class': 'lyricsh'}).find('b').get_text()
        if 'Lyrics' in art:
            return re.sub(' ?Lyrics', '', art)

    def extract_album(self, soup):
        alb = soup.find('div', {'class': 'songinalbum_title'})
        print(alb)
        if alb:
            if'album' in alb.text:
                return alb.find('b').get_text().strip('"') or ""
            else:
                return "Unknown"
        else:
            return "Unknown"

    def extract_lyrics(self, soup):
        return re.sub('\n', '\\n', soup.find('div', {'class': 'ringtone'}).findNext('div').get_text()).strip()

    def fetch_metadata(self):
        meta = {
                'name': '',
                'album': '',
                'artist': '',
                'lyrics': '',
                }
        if self.url is not None:
            text = self.requester.make_request(self.url)
            # print(text)
            soup = BeautifulSoup(text, 'html.parser')
            meta['name'] = self.extract_name(soup)
            meta['album'] = self.extract_album(soup)
            meta['artist'] = self.extract_artist(soup)
            meta['lyrics'] = self.extract_lyrics(soup)
        return meta

    def set_metadata(self, mdata):
        sng = eyed3.load(self.path)
        if not sng.tag:
            sng.add_tags()
        sng.tag.artist = u"{}".format(mdata['artist'])
        sng.tag.album = u"{}".format(mdata['album'])
        sng.tag.artist = u"{}".format(mdata['artist'])
        sng.tag.lyrics.set(u"{}".format(mdata['lyrics']))
        art = global_artwork.get_artwork(mdata)
        print("art ",art)
        if art:
            with open(art, "rb") as cover_art:
                sng.tag.images.set(3, cover_art.read(), "image/jpeg")
        sng.tag.save(self.path)


class FileLibrary:
    def __init__(self, root_path):
        self.root = root_path
        self.files = []

    def get_folder_list(self):
        return glob.glob(self.root+"/*/*.mp3")


global_artwork = albumArtwork('./tmp')

if __name__ == "__main__":
    global_requester = Requester(site="https://www.sslproxies.org/")
    # song = songMetadata("./Music/Like_Love/The Amity Affliction 'Like Love' Official Music Video.mp3",global_requester)
    ##song = songMetadata("./Music/Let_the_ocean_take_me/The Amity Affliction - Death's Hand.mp3",global_requester)
    # song = songMetadata("./Music/A_Thousand_Suns/Blackout - Linkin Park.mp3",global_requester)

    meta = {
            'name': 'Like Love',
            'album': 'Unknown',
            'artist': 'The Amity Affliction',
            'lyrics': 'asdf',
            }
    print(global_artwork.get_artwork(meta))
    # res = song.fetch_metadata()
    # song.set_metadata(res)
    # print(res['artist'])
    # print(res['name'])
    #print(res['album'])
    ##artworker.get_artwork(res)
    #print(res['lyrics'])
    # test = FileLibrary('./Music/')
    # for fl in test.get_folder_list():
    #     # maybe add caching as well
    #     tmp = songMetadata(fl)
    #     mdata = tmp.fetch_metadata()
    #     tmp.set_metadata(mdata=mdata)
    #     print('set meta for {} '.format(fl))
    #proxy_dict = {
    #        'https': 'https://121.244.147.137:8080'
    #        }
    #text = requests.get('https://www.discogs.com/artist/2446213-The-Amity-Affliction', proxies=proxy_dict).text
    #print(requests.get("https://www.azlyrics.com/lyrics/amityaffliction/likelove.html",proxies=    {'https': 'https://187.102.222.28:6666'} ).text)
