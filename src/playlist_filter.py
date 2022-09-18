#!/usr/bin/python3
import fileinput
import sys
import argparse
import itertools

## Args
parser = argparse.ArgumentParser(
    prog="playlist_filter.py",
    description='Filter a list of yt playlists to videos for the use of downloader.py',
    exit_on_error=True
    )

parser.add_argument('-i', '--stdin', action="store_true", help='Force to use stdin')
parser.add_argument('-o', '--stdout', action="store_true", help='Force to use stdout as output')
parser.add_argument('-f', '--files', action="append", nargs='+',help='Files that contain the playlists')

def main():
    parsed = parser.parse_args(sys.argv[1:])
    file_list = list(itertools.chain.from_iterable(parsed.files))
    print(file_list)
    print("hello nibba")

if __name__ == "__main__":
    main()
