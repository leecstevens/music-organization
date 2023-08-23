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

    Since the music app will have several different shared features, 
    no sense in writing things twice (or more).  You agree?

    This code is meant to be quick and dirty, I'm sure there are
    other/better ways of doing things.  We're all IT people and have
    our own set in our ways things.  Suggestions welcomed, but not always
    followed.

"""

import os, platform

# Just to make it easy, leave any global vars at the top, so it will be easier to find.
settings_file = 'settings.txt'

class settings:
    def get(name):
        tmp = settings.read()
        if tmp[name] != None:
            return tmp[name]

    def get_safe_artists():
        try:
            file = open('safe_artists.txt','r')
            safe_artists = []
            s = file.readlines()
            for i in s:
                if i[0] != '#':
                    safe_artists.append(i.replace('\n', ''))
            return tuple(safe_artists)
        except:
            print('No safe artists found.')

    def get_final_tag_actions():
        try:
            file = open('final_clean.txt','r')
            final_clean = []
            s = file.readlines()
            for i in s:
                if i[0] != '#':
                    final_clean.append(i.replace('\n', ''))
            return tuple(final_clean)
        except:
            print('No safe artists found.')

    def read():
        ret_settings = {}
        try:
            file = open(settings_file,'r')
            tmp_settings = file.readlines()
        
            for line in tmp_settings:
                if line[0] != '#':
                    key = line.split('||')[0]
                    val = line.split('||')[1].replace('\n', '')
                    if key.lower() == 'extensions' or key.lower() == 'replace_chars':
                        val = tuple(val.split(','))
                    elif key.lower() == 'delims':
                        val = tuple(map(lambda i:i.replace('\'',''),val.split('`')))
                    ret_settings[key] = val
            return ret_settings
        except FileNotFoundError:
            print('File is missing.  Make sure you have a %s in the script folder.' % (settings_file))
        except:
            print('Something is really messed up beyond a standard file not found.\nLooking for %s.' % (settings_file))

class input:
    def truefalse(answer):
        a = answer.lower()
        if 'yes' in a or 'true' in a or a == 'y':
            return True
        else:
            return False

class format:
    def replace_chars(item, chars):
        for i in range(len(chars)):
            se = chars[i].split(':')[0]
            re = chars[i].split(':')[1]
            item = item.replace(se, re)
        return item
    
    def check_case(artist,albumartist):
        if (artist.islower() or artist.isupper()):
            return True
        elif (albumartist.islower() or albumartist.isupper()):
            return True
        else:
            return False

    def convert_case(artist,albumartist):
        if (artist.islower() and albumartist.islower()):
            return artist
        elif (artist.isupper() and albumartist.isupper()):
            return artist
        elif (artist.islower() and not albumartist.islower()):
            return albumartist
        elif (artist.isupper() and not albumartist.isupper()):
            return albumartist
        elif (not artist.islower() and albumartist.islower()):
            return artist
        elif (not artist.isupper() and albumartist.isupper()):
            return artist
        else:
            return artist


    def has_delims(string):
        delims = settings.get('delims')
        d = []
        for i in range(len(delims)):
            if delims[i] in string:
                d.append(delims[i])
        if len(d) == 0:
            return False
        else:
            return True

class file:
    def artist_folder(folder):
        f = os.path.join(folder)
        if platform.system().lower() == 'windows':
            delim = '\\'
            pos = 2
        else:
            delim = '/'
            pos = 1
        return f.split(delim)[pos]

    def artist_album(folder):
        f = os.path.join(folder)
        if platform.system().lower() == 'windows':
            delim = '\\'
            pos = 3
        else:
            delim = '/'
            pos = 2
        return f.split(delim)[pos]
    
    def artist_file(name):
        f = os.path.join(name)
        if platform.system().lower() == 'windows':
            delim = '\\'
        else:
            delim = '/'
        return f.split(delim)[-1]

    def list_path(path):
        filelist = []
        for root, dirs, files in os.walk(path):
            for file in files:
                filelist.append(os.path.join(root,file))
        return filelist
    
    def get_music_files(filelist, ext):
        scan_log = ['','Music File Scan']
        file_list = []
        for name in filelist:
            lower_name = name.lower()
            if lower_name.endswith(ext):
                file_list.append(name)
        scan_log.append('Found %s files with music extensions' % (len(file_list)))
        return scan_log, file_list

    def process(filelist, ext):
        dupe_list = []
        delete_list = []
        rename_list = []
        ignore_list = []
        scan_log = ['','Scan Results:']
        for name in filelist:
            lower_name = name.lower()
            if '.ds_store' in lower_name:
                delete_list.append(name)
                filelist.remove(name)
                scan_log.append('Found OS File: %s' % (name))
            elif not lower_name.endswith(ext):
                ignore_list.append(name)
                filelist.remove(name)
                scan_log.append('Found Ignorable File: %s' % (name))
            else:
                if 'm4a' in name:
                    newname = name[:-4]+'.mp3'
                    if newname in [f.lower() for f in filelist]:
                        dupe_list.append(newname)
                        filelist.remove(name)
                        scan_log.append('Found File Combo: %s - %s' % (name, newname))

                for i in range(1,10):
                    dir = '/'.join(name.split('/')[:-1])
                    newname = dir + '/' + name.split('/')[-1].split('.')[0]+' '+str(i)+'.'+name.split('.')[-1]
                    if name in filelist and newname in filelist:
                        dupe_list.append(newname)
                        filelist.remove(newname)
                        scan_log.append('Found Training Duplicate: %s' % (name))
        
        for name in filelist:
            fullname = os.path.split(name)[0]
            filename = os.path.split(name)[1]
            
            if filename.split(' ')[0].isnumeric():
                if int(filename.split(' ')[0]) <= 20:
                    filename = ' '.join(filename.split(' ')[1::])
                    newname = ''.join(fullname)+'/'+filename
                    rename_list.append(name+'||'+newname)
                    scan_log.append('Found Leading Numbered File: %s' % (name))

                    filelist.remove(name)        
        
        return scan_log,filelist,dupe_list,delete_list,rename_list,ignore_list
    
    def file_action(filelist, take_action,action,type):
        logs = ['','File Action: '+action.title()+ ' of '+type.title()]
        pre = '' if take_action == True else '(Log Only) '
        for name in filelist:
            logtext = pre+action.title()+': '
            if action == 'delete':
                logtext += '%s' % (name)
                if take_action:
                    os.remove(name)
            elif action == 'rename':
                src = name.split('||')[0]
                dest = name.split('||')[1]
                logtext += '%s to %s' % (src, dest)
                if take_action:
                    os.rename(src, dest)
            logs.append(logtext)
        return logs

    def dump_log(logfile, log):
        log_file = open(logfile,'w')
        for item in log:
            log_file.write(item+'\n')
        log_file.close() 