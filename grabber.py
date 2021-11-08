#!/usr/bin/python

import youtube_dl
import os
import sys
import re
from itertools import repeat as repeat
from threading import Thread as pthr

global_settings = {
        '--force-replace': True,
        '--no_structure': False,
        '--path': os.getcwd(),
        '--playlists-csv': 'library.csv',
        '--output-folder': 'Music',
        '--concurent-flows': 16,
        }


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
        return col[key].replace(' ', '_')
    else:
        return None


def cast_arguments(key, val):
    if isinstance(global_settings[key], bool):
        global_settings[key] = bool(val)
        return
    elif isinstance(global_settings[key], int):
        global_settings[key] = int(val)
        return
    else:
        assert False, "Unknown arg type"


def download_song_vid_info(info):
    try:
        tmp = song(*info)
        tmp.download()
        # yes i know bad practice but sometimes it randomly fails, too much
        # traffic maybe ?
        #TODO: Add a better except catch block
    except:
        pass

def clean_name(name):
    return re.sub(" ?[(].*[)] ?| ?[[].*[]] ?", "", name)

# since android does not support termux, this is necessary, threads are
# supported and also might be more balanced in downloading in bursts

class PseudoPool:
    def __init__(self, size_pool):
        self._size = size_pool
        self._que = []

    def add_op(self, fnc, args):
        # should be thread but behaviour is a lot like pthr
        self._que = pthr(target=fnc, args=args)
        self.try_process()

    def try_process(self, force=False):
        if len(self._que) == self._size or force:
            for i in self._que:
                i.start()
            for i in self._que:
                i.join()
            self._que = []
        else:
            return

    def flush_try(self):
        self.try_process(True)


class song:
    def __init__(self, vid_info, sub_path = ""):
        self._artist = if_key(vid_info, 'artist')
        self._album = if_key(vid_info, 'album')
        self._title = if_key(vid_info, 'title')
        self._alt_title = if_key(vid_info, 'alt_title')
        self._webpage_url = if_key(vid_info, 'webpage_url')
        self._playlist = sub_path

    def form_name(self):
        if self._alt_title and self._artist:
            return "{}-{}".format(self._artist, self._alt_title)
        else:
            return re.sub("[(].*[)]|[[].*[]]", '', self._title.replace(' ', '_'))

    def form_ydl_name(self):
        if self._alt_title and self._artist:
            return "%(artist)s-%(alt_title)s.%(ext)s"
        else:
            return "%(title)s.%(ext)s"

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

    def form_ydl_path(self, sub_path):
        fname = self.form_ydl_name()
        alb = self._album or 'Unknown'
        art = self._artist or 'Unknown'
        whr = art + '/' + alb
        whr = to_pth(whr, fname)
        pth = to_pth(global_settings['--path'],
                        global_settings['--output-folder'] + '/' + sub_path)
        if global_settings['--no_structure']:
            return to_pth(pth, fname)
        return to_pth(pth, whr)

    def download(self):
            ydl_opts = {
                    'format': 'bestaudio',
                    'postprocessors': [{
                        'key': 'FFmpegExtractAudio',
                        'preferredcodec': 'mp3',
                        'preferredquality': '192'
                        }],
                    'prefer_ffmpeg': True,
                    'keepvideo': False,
                    'outtmpl': "./Music/"+ self._playlist + "/%(title)s.%(ext)s",
                    }
            with youtube_dl.YoutubeDL(ydl_opts) as down:
                inf = down.extract_info(self._webpage_url, download=True)
                dst_name = down.prepare_filename(inf)
                print("rename to ", clean_name(dst_name))
                os.rename(dst_name, clean_name(dst_name))


if __name__ == '__main__':
    for i in sys.argv[1:]:
        arg_type, arg_value = i.split(':')
        assert arg_type not in global_settings, "Argument {} is Unknown".format(arg_type)
        cast_arguments(arg_type, arg_value)

    ps_pool = PseudoPool(global_settings['--concurent-flows'])
    with open(global_settings['--playlists-csv'], 'r') as playlists:
        ydl = youtube_dl.YoutubeDL()
        for i in playlists:
            name, link = i.split(',')
            with ydl:
                result = ydl.extract_info(link, download=False)
                if 'entries' in result:
                    video = result['entries']
                else:
                    video = result
                video_name = list(zip(video, repeat(name)))
                for i in video_name:
                    ps_pool.add_op(download_song_vid_info, video_name)
        ps_pool.flush_try()
