import sqlite3

class LyricDbSchema:
    lyric_db_name ="lyric.db"
    songs_table = """ CREATE TABLE IF NOT EXISTS songs (
            song_name text PRIMARY KEY,
            song_file_name text NOT NULL,
            yt_link text,
            lyrics text NOT NULL,
            album_name text,
            FOREIGN KEY (album_name) REFERENCES albums (Album_name)
            );"""

    album_table = """ CREATE TABLE IF NOT EXISTS albums (
            Album_name text PRIMARY KEY,
            artwork_uri text,
            Band_name text NOT NULL,
            FOREIGN KEY (band_name) REFERENCES bands (band_name)
            );"""

    bands_table = """ CREATE TABLE IF NOT EXISTS bands (
            band_name text PRIMARY KEY
            );"""



class Connection:
    def __init__(self):
        conn = sqlite3.connect(LyricDbSchema.lyric_db_name)
        if conn is not None:
            conn.execute(LyricDbSchema.songs_table)
            conn.execute(LyricDbSchema.album_table)
            conn.execute(LyricDbSchema.bands_table)
        else:
            print("Error! cannot create the database connection.")
        self.connection = conn

    def query_song(self,song_fname):
        pass

    def add_song(self,song_name, song_fname,lyrics,album,):
       pass

if __name__ == "__main__":
    test = Connection()
