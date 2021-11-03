#!/usr/bin/python

import youtube_dl
import os
import re
# import mutagen # to edit tags of file


def print_key_if(col, key):
    if key in col:
        print(key, ":", col[key])
    else:
        print("no key", key)


def to_pth(pth, suf):
    if pth[-1] == '/':
        return pth + suf
    return pth + '/' + suf


def if_key(col, key):
    if key in col:
        return col[key].replace(' ','_')
    else:
        return None


global_settings = {
        '--force-replace': True,
        '--no_structure': False,
        '--path': os.getcwd(),
        '--playlists-csv': 'library.csv',
        '--output-folder': 'Music'
}


class song:
    def __init__(self, vid_info,sub_path = None):
        self._artist     = if_key(vid_info, 'artist')
        self._album      = if_key(vid_info, 'album')
        self._title      = if_key(vid_info, 'title')
        self._alt_title  = if_key(vid_info, 'alt_title')
        self._webpage_url= if_key(vid_info, 'webpage_url')
        self.name = self.form_name()
        self.path = self.form_path(sub_path)

    def form_name(self):
        if self._alt_title and self._artist:
            return "{}-{}.mp3".format(self._artist, self._alt_title)
        else:
            return re.sub("[(].*[)]", '', self._title.replace(' ', '_'))

    def form_path(self, sub_path):
        fname = self.form_name()
        alb = self._album or 'Unknown'
        art = self._artist or 'Unknown'
        whr = art + '/' + alb
        whr = to_pth(whr, fname)
        pth = to_pth(global_settings['--path'],
                     global_settings['--output-folder'] + '/' + sub_path)
        if global_settings['--no_structure']:
            return to_pth(pth, fname)
        return to_pth(pth, whr)

    def fix_metadata():
        print("not yet implemented")
        pass

    def download(self):
        if not (os.path.isfile(self.path) or os.path.isfile(self.name)) or global_settings['--force_replace']:
            ydl_opts = {
                        'format': 'bestaudio',
                        'postprocessors': [{
                            'key': 'FFmpegExtractAudio',
                            'preferredcodec': 'mp3',
                            'preferredquality': '192'
                            }],
                        'prefer_ffmpeg': True,
                        'keepvideo': False,
                        'outtmpl': self.path,
                    }
            with youtube_dl.YoutubeDL(ydl_opts) as down:
                down.extract_info(self._webpage_url,download=True)


if __name__ == '__main__':
    with open(global_settings['--playlists-csv'], 'r') as playlists:
        ydl = youtube_dl.YoutubeDL()
        for i in playlists:
            name, link= i.split(',')
            with ydl:
                result = ydl.extract_info(
                    link,
                    download=False)
                if 'entries' in result:
                    video = result['entries']
                else:
                    video = result
                print(video[0].keys())
                for i in video:
                    trc = song(i,name)
                    trc.download()
