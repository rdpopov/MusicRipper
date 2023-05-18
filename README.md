# MusicRipper
[MusicRipper](MusicRipper.md) is an instrument based on yt-dlp, to download music.

Levarages barebones ytdlp to handle downloading and incremental updates of music
library

With add on scripts to
    - Get song metadata - Song name, Album, Album artwork, Artist and Lyrics 
    - Save them in a local database if anything happens to the songs
    - Sort the songs based on artist and album


# TODO
- [ ] Create a script to sync playlists from youtube
    - [ ] Add the 'Remember which songs you have'
    - [ ] Add the 'Multithreaded'
    - [ ] Add the 'Read playlists from file'
    - [ ] Who knows how caching of this works so, going to have additional to
      handle deletions

- [ ] Script to grab the metadata for a song
    - [ ] A service to manage the db, ideally in rust, but sadly no, maybe c++
        - [ ] possible candidates are lua, golang, python, c++ currently maybe
          golang ...
    - [ ] Get metadata for songs from:
        - [ ] [Genius](https://genius.com/) ideally, all the info is one place, pacing is hard .. kind of
        - [ ] [https://www.discogs.com/](https://www.discogs.com/) + [https://www.azlyrics.com/](https://www.azlyrics.com/)
    - [ ] A script to send the songs in the proper directories
