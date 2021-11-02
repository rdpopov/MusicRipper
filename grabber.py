#!/usr/bin/python

import youtube_dl
# import mutagen # to edit tags of file


def print_key_if(col, key):
    if key in col:
        print(key, ":", col[key])
    else:
        print("no key", key)

def to_pth(pth,suf):
    if pth[-1] == '/':
        return pth + suf
    return pth + '/' + suf


def if_key(col, key):
    if key in col:
        return col[key]
    else:
        return None

global_settings = {
        '--force_replace': True,
        '--no_structure': False,
}


class Song:
    def __init__(self, vid_info):
        self._artist = if_key(i, 'artist')
        self._album = if_key(i, 'album')
        self._title = if_key(i, 'title')
        self._alt_title = if_key(i, 'alt_title')
        self._webpage_url = if_key(i, 'webpage_url')

    def form_name(self,path):
        fmt_map = {}
        if not self._alt_title or not self._artist:
            fmt_map['name'] = self._title.replace(' ', '_')
        fmt_map['name'] = "{}-{}.mp3".format(self._artist, self._alt_title)
        if not self._album or not self._artist:
            fmt_map['local_path'] = 'Unkown'
        fmt_map['path']

    def download(self,root_path,artist_and_album,force=False):
        ydl_opts = {
                'format': 'bestaudio/best',
                'postprocessors': [{
                    'key': 'FFmpegExtractAudio',
                    'preferredcodec': 'mp3',
                    'preferredquality': '192',
                    }],
                }
        with youtube_dl.YoutubeDL(ydl_opts) as ydl:
            ydl.download(self._webpage_url)



if __name__ == '__main__':
    
    ydl = youtube_dl.YoutubeDL({'outtmpl': '%(id)s.%(ext)s'})
    with ydl:
        result = ydl.extract_info(
            'https://www.youtube.com/watch?v=eJnQBXmZ7Ek&list=PLX1RXtit_D_2E17WA0uqyvhi0CJcfkJRC',
            download=False
        )
    if 'entries' in result:
        video = result['entries']
    else:
        video = result
    print(video[0].keys())
    
    for i in video:
        print('--------------------------------------------------------------------')
        print_key_if(i,'artist')
        print_key_if(i,'album')
        print_key_if(i,'title')
        print_key_if(i,'alt_title')
        print(i['title'],i['webpage_url'])
