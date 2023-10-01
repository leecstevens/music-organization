"""

    Music Consolidation project - Lee Stevens
    Released on the "you break something, not my fault" agreement.
    
    May this be useful to you as well as a good learning tool for you.
    The main code repository if you stole / slash and hacked it is here:

    https://github.com/leecstevens/music-organization
    (The readme file is always your friend here)

    This code is meant to be quick and dirty, I'm sure there are
    other/better ways of doing things.  We're all IT people and have
    our own set in our ways things.  Suggestions welcomed, but not always
    followed.

"""

import shared
import sqlite3
import re, os
import music_tag
from mutagen.mp3 import MP3

all_artists = []
diff_artists = []
all_titles = []
diff_titles = []
all_albums = []
diff_albums = []
all_paths = []
diff_paths = []
all_names = []
diff_names = []

class cache:
    def prep_cache(thelist):
        for file in thelist:
            path = os.path.split(file)[0]
            name = os.path.split(file)[1]
            track = get_song_data(file)
            if track['artist'] not in all_artists:
                if track['artist'] not in diff_artists:
                    diff_artists.append(track['artist'])
            if track['album'] not in all_albums:
                if track['album'] not in diff_albums:
                    diff_albums.append(track['album'])
            if track['title'] not in all_titles:
                if track['title'] not in diff_titles:
                    diff_titles.append(track['title'])
            if path not in all_paths:
                if path not in diff_paths:
                    diff_paths.append(path)
            if name not in all_names:
                if path not in diff_names:
                    diff_names.append(name)


def convert_length(length):
    pass

def clean_song_data(lyric):
    re_ticket = 'See (.*) LiveGet tickets as low as \$(.*)You might also like'
    printed = False
    trimnum = 0
    if lyric[-1].isnumeric():
        printed = True
        done = False
        trimnum = 1
        while not done:
            if lyric[-(trimnum+1)].isnumeric():
                trimnum += 1
            else:
                done = True
    lyric = re.sub(re_ticket, '', lyric)
    if trimnum > 0:
        lyric = lyric[:-trimnum]
    lyric = lyric.replace('<br>You might also like','<br>')
    lyric = lyric.replace('<br><br>','<br>')
    return lyric

def get_song_data(file):
    f = music_tag.load_file(file)
    ex = MP3(file)
    song = {
    'path': os.path.split(file)[0],
    'name': os.path.split(file)[1], 
    'artist': str(f['artist']),
    'title': str(f["title"]),
    'album': str(f["album"]),
    'lyrics': clean_song_data(str(f['lyrics'])) if str(f['lyrics']) != '' else '',
    'length': round(ex.info.length),
    'bitrate': ex.info.bitrate
    }
    return song

music_folder = shared.settings.get('music_folder')
dbname = shared.settings.get('sqlitedb')
conn = shared.sqlite.connect(dbname)
filelist = shared.file.list_path(music_folder,True)
cache.prep_cache(filelist)
print('Tracks: %s\nUnique Artists: %s\nUnique Albums: %s\nUnique Titles: %s\nUnique Paths: %s\nUnique Names: %s' % (
    len(filelist),
    len(all_artists)+len(diff_artists),
    len(all_albums)+len(diff_albums),
    len(all_titles)+len(diff_titles),
    len(all_paths)+len(diff_paths),
    len(all_names)+len(diff_names)
))
conn.close()