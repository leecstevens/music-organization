import shared
import music_tag

def test_mp3():
    test_file = 'music/file1.mp3'
    file = music_tag.load_file(test_file)
    print(file['title'])
    #for key,value in file.items():
        #print('%s: %s' % (key,value))

def ret_artist(artist):
    delims = shared.settings.get('delims')
    safe_artists = shared.settings.get_safe_artists()
    for i in range(len(safe_artists)):
         if artist == safe_artists[i]:
            return artist
    d = []
    a = artist
    for i in range(len(delims)):
        if delims[i] in artist:
            d.append(delims[i])
    if len(d) > 0:
        for i in range(len(d)):
            a = a.split(d[i])[0]
        return a
    else:
        
        return artist

def final_clean(artist):
    if shared.format.has_delims(artist):
        artist = ret_artist(artist)
    final_actions = shared.settings.get_final_tag_actions()
    for item in final_actions:
        action = item.split('||')[0].lower()
        src = item.split('||')[1].lower()
        to = item.split('||')[2]
        if action == 'replace':
            if src == artist.lower():
                artist = to
        elif action == 'in':
            if src in artist.lower():
                artist = to
    return artist


def resolve_tag(artist, albumartist, folder):
    scan_log = ['','Resolving tags']
    resolved = ''
    if artist not in albumartist:
        if len(artist) > 0 and len(albumartist) == 0:
            resolved = artist
        elif len(artist) == 0 and len(albumartist) == 0:
            print('')
            resolved = shared.file.artist_folder(folder)
        elif 'unknown' in artist.lower():
            if 'unknown' not in albumartist.lower() and len(albumartist) > 2:
                resolved = albumartist
        elif artist.lower() != albumartist.lower():
            resolved = artist
        elif shared.format.check_case(artist, albumartist):
                resolved = shared.format.convert_case(artist, albumartist)
        elif artist.lower() == albumartist.lower():
            if shared.format.has_delims(artist) and not shared.format.has_delims(albumartist):
                resolved = albumartist
            else:
                resolved = ret_artist(artist)
        else:
            resolved = artist

    else:
        resolved = artist

    resolved = final_clean(resolved)
    return resolved

def process_tags(filelist,take_action):
    scan_log = []
    scan_log.append('Processing tags.  We will%sbe taking action on the tags.' % (' ' if take_action else ' NOT '))
    for name in filelist:
        file = music_tag.load_file(name)
        title = str(file['title'])
        artist = str(file['artist'])
        albumartist = str(file['albumartist'])
        folder = shared.file.artist_folder(name)
        resolved = resolve_tag(artist, albumartist, folder)
        scan_log.append('File: %s\nTitle: %s\nArtist: %s\nAlbum Artist: %s\nResolved: %s\n' % (name,title,artist,albumartist,resolved))
    return (scan_log)

def startup():
    log = []
    settings = {}
    settings = shared.settings.read()
    take_action = shared.input.truefalse(settings['take_action'])
    log.append('Searching folder: %s' % (settings['music_folder']))
    filelist = shared.file.list_path(settings['music_folder'])
    log.append('Found %s files in the folder and subfolders.' % (len(filelist)))
    scan_logs,filelist = shared.file.get_music_files(filelist, settings['extensions'])
    log += scan_logs
    log += process_tags(filelist, take_action)
    shared.file.dump_log(settings['logfile'],log)
    
startup()
#test_mp3()