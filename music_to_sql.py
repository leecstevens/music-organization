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
import re, os
import music_tag
from mutagen.mp3 import MP3

all_artists = []
all_titles = []
all_albums = []
all_paths = []
all_filenames = []

class cache:
    def build_cache():
        records = shared.mysql.return_table('select id,name from music_artists')
        for record in records:
            all_artists.append(record[0])
            all_artists.append(record[1])
        print('Artists cached: %s' % (len(all_artists)))
        records = shared.mysql.return_table('select id,name from music_albums')
        for record in records:
            all_albums.append(record[0])
            all_albums.append(record[1])
        print('Albums cached: %s' % (len(all_albums)))
        records = shared.mysql.return_table('select id,name from music_titles')
        for record in records:
            all_titles.append(record[0])
            all_titles.append(record[1])
        print('Titles cached: %s' % (len(all_titles)))
        records = shared.mysql.return_table('select id, name from music_paths')
        for record in records:
            all_paths.append(record[0])
            all_paths.append(record[1])
        print('Paths cached: %s' % (len(all_paths)))
        records = shared.mysql.return_table('select id, name from music_filenames')
        for record in records:
            all_filenames.append(record[0])
            all_filenames.append(record[1])
        print('File names cached: %s' % (len(all_filenames)))

    def read_cache():
        pass

    def commit_tracks(thelist):
        data = []
        print('Reading all the tracks to commit')
        for file in thelist:
            path = os.path.split(file)[0]
            name = os.path.split(file)[1]
            track = get_song_data(file)
            try:
                artist = all_artists[all_artists.index(track['artist'])-1]
            except ValueError:
                artist = -1
            
            try:
                album = all_albums[all_albums.index(track['album'])-1]
            except ValueError:
                album = -1

            try:
                title = all_titles[all_titles.index(track['title'])-1]
            except ValueError:
                title = -1

            try:
                filepath = all_paths[all_paths.index(path)-1]
            except ValueError:
                filepath = -1

            try:
                filename = all_filenames[all_filenames.index(name)-1]
            except ValueError:
                filename = -1

            data_tup = (artist, album, title, int(track['length']), 
                        int(track['bitrate']), filepath, filename,track['lyrics'])
            data.append(data_tup)

        print ('Committing tracks')
        sql = ('call sp_add_track (%s,%s,%s,%s,%s,%s,%s,%s)')
        shared.mysql.execute_many_sp(sql,data)
        data = []

    def prep_cache(thelist):
        print('Reading all the tracks to cache')
        diff_artists = []
        diff_titles = []
        diff_albums = []
        diff_paths = []
        diff_filenames = []
        
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
            if name not in all_filenames:
                if path not in diff_filenames:
                    diff_filenames.append(name)
        
        print ('Committing artists...')
        sql = ('call sp_add_artist (%s)')
        data = list([(item,) for item in diff_artists])
        shared.mysql.execute_many_sp(sql,data)
        diff_artists=[]
        
        print ('Committing albums...')
        sql = ('call sp_add_album (%s)')
        data = list([(item,) for item in diff_albums])
        shared.mysql.execute_many_sp(sql,data)
        diff_albums=[]
        
        print ('Committing titles...')
        sql = ('call sp_add_title (%s)')
        data = list([(item,) for item in diff_titles])
        shared.mysql.execute_many_sp(sql,data)
        diff_titles=[]
        
        print ('Committing paths...')
        sql = ('call sp_add_path (%s)')
        data = list([(item,) for item in diff_paths])
        shared.mysql.execute_many_sp(sql,data)
        diff_paths=[]
        
        print ('Committing file names...')
        sql = ('call sp_add_filename (%s)')
        data = list([(item,) for item in diff_filenames])
        shared.mysql.execute_many_sp(sql,data)
        diff_filenames=[]

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
    lyric = lyric.replace(')You might also like',')')
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
filelist = shared.file.list_path(music_folder,True)
#filelist = filelist[455:457]
cache.build_cache()
cache.prep_cache(filelist)
cache.commit_tracks(filelist)
print('Tracks: %s\nUnique Artists: %s\nUnique Albums: %s\nUnique Titles: %s\nUnique Paths: %s\nUnique Names: %s' % (
    len(filelist),
    len(all_artists),
    len(all_albums),
    len(all_titles),
    len(all_paths),
    len(all_filenames)
))
