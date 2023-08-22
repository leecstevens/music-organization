import shared
import music_tag

def test_mp3():
    test_file = 'music/file1.mp3'
    file = music_tag.load_file(test_file)
    print(file['title'])
    #for key,value in file.items():
        #print('%s: %s' % (key,value))

def process_tags(filelist,take_action):
    scan_log = []
    scan_log.append('Processing tags.  We will%sbe taking action on the tags.' % (' ' if take_action else ' NOT '))
    for name in filelist:
        file = music_tag.load_file(name)
        title = file['title']
        artist = file['artist']
        albumartist = file['albumartist']
        composer = file['composer']
        scan_log.append('File: %s\nTitle: %s\nArtist: %s\nAlbum Artist: %s\nComposer: %s\n' % (name,title,artist,albumartist,composer))
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