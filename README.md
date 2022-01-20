# MusicRipper
MusicRipper is an instrument based on youtube-dl, to download music.

Terminal based and config is a plain text file or the source itself.
Just like god intended. GUIs are slow and limiting, CLI is best UI.

The whole idea is to be able to have something to rip out music from youtube.
Using just a playlist url.

Works on termux which means i can sync music with my phone very easy

## What it does & And how it does it
- We get all the songs from a playlist and download them one after the other,
    and some in parallel
- For each song we query google (discogs and azlyrics) for metadata (artwork too)
    then we store them locally in a database, and the images just on disk.
    - That database is a grpc based one with a rust back end. More
        services can be added and the functionality extended. But still remain
        robust, fast, and safe. For example other services that could use the
        db, say a primitive music player.
    - The database is required so we can do song metadata faster. web scraping
        with unreliable proxies can be very slow.
