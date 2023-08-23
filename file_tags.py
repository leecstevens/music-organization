"""
    Music Consolidation project - Lee Stevens
    Released on the "you break something, not my fault" agreement.
    
    May this be useful to you as well as a good learning tool for you.
    The main code repository if you stole / slash and hacked it is here:

    https://github.com/leecstevens/music-organization

    This code is meant xto be quick and dirty, I'm sure there are
    other/better ways of doing things.  We're all IT people and have
    our own set in our ways things.  Suggestions welcomed, but not always
    followed.
"""

import shared
import music_tag

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
    replace_chars = shared.settings.get('replace_chars')
    for i in range(len(replace_chars)):
        src = replace_chars[i].split(':')[0]
        to = replace_chars[i].split(':')[0]
        artist = artist.replace(src, to)
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
    resolved = ''
    if artist not in albumartist:
        if len(artist) > 0 and len(albumartist) == 0:
            resolved = artist
        elif len(artist) == 0 and len(albumartist) == 0:
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
        if resolved == '':
            if title == '':
                file['title'] = shared.file.artist_file(name).split('.')[0]
            if artist == '':
                resolved = shared.file.artist_folder(name)
                if str(file['album']) == '':
                    a = shared.file.artist_album(name)
                    file['album'] = a if (a != '' and 'unknown' not in a.lower()) else resolved
        file['artist'] = resolved
        if shared.input.truefalse(shared.settings.get('same_string')) == True:
            file['albumartist'] = resolved
        scan_log.append('Title: %s\nArtist: %s\nAlbum Artist: %s\nResolved: %s' % (title,artist,albumartist,resolved))
        scan_log.append('%spdating file: %s\n' % ('U' if take_action else '(Log Only) Not u', name))
        if take_action:
            file.save()
    return (scan_log)

def startup():
    log = []
    settings = {}
    settings = shared.settings.read()
    scan_only = shared.input.truefalse(settings['scan_only'])
    take_action = shared.input.truefalse(settings['take_action'])
    act = True if take_action == True or scan_only == False else False
    log.append('Searching folder: %s' % (settings['music_folder']))
    filelist = shared.file.list_path(settings['music_folder'])
    log.append('Found %s files in the folder and subfolders.' % (len(filelist)))
    scan_logs,filelist = shared.file.get_music_files(filelist, settings['extensions'])
    log += scan_logs
    log += process_tags(filelist, act)
    shared.file.dump_log(settings['logfile'],log)
    
startup()
