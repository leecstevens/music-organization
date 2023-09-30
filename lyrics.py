import shared
from urllib.parse import quote_plus
import shared
import lyricsgenius
import music_tag

api_key = shared.settings.get('genius_api_key')
genius = lyricsgenius.Genius(api_key)
genius.remove_section_headers = True

def search_artist(who: str, max: int):
    max = max if max == 0 else 99999
    for i in range(1,6):
        try:
            artist = genius.search_artist(who, max_songs=0, sort="title")
            break
        except:
            print('Error looking for %s, %s' % (who, ', retry' if i == 1 else ', retry '+str(i)))
    return artist

def search_artist_and_title (who: str, title: str):
    artist = search_artist(who,1)
    for i in range(1,6):
        try:
            song = artist.song(title)
            l = convert_lyrics(song.lyrics)
            return l
            break
        except:
            if i == 5:
                print('No info found for %s by %s' % (title,artist))
                break
            else:
                print('Error processing, %s' % ('try again' if i == 1 else 'retry '+str(i)))


def convert_lyrics(lyrics):
    lyrics = lyrics.split('Lyrics',1)[1:]
    lyrics = lyrics[0]
    lyrics = lyrics.split('Embed')[0]
    return lyrics

def get_song_data(file):
    f = music_tag.load_file(file)
    artist = str(f['artist'])
    title = str(f["title"])
    if str(f['lyrics']) == '':
        l = search_artist_and_title(artist, title)
        if l != '':
            f['lyrics'] = l
            f.save()
    else:
        print('Lyrics already exist for %s by %s' % (title,artist))

def startup():
    log = []
    settings = {}
    settings = shared.settings.read()
    skip_artists = list(shared.settings.get_skip_artists())
    scan_only = shared.input.truefalse(settings['scan_only'])
    take_action = shared.input.truefalse(settings['take_action'])
    act = True if take_action == True or scan_only == False else False
    log.append('Searching folder: %s' % (settings['music_folder']))
    filelist = shared.file.list_path(settings['music_folder'])
    log.append('Found %s files in the folder and subfolders.' % (len(filelist)))
    scan_logs,file_list = shared.file.get_music_files(filelist, settings['extensions'])
    log += scan_logs
    file_list = shared.file.remove_skipped_artists(file_list)
    for item in file_list:
        if not shared.file.artist_folder(item) in skip_artists:
            get_song_data(item)
    shared.file.dump_log(settings['logfile'],log)

startup()
