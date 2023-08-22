"""

    Since the music app will have several different shared features, 
    no sense in writing things twice (or more).  You agree?

    This code is meant to be quick and dirty, I'm sure there are
    other/better ways of doing things.  We're all IT people and have
    our own set in our ways things.  Suggestions welcomed, but not always
    followed.

"""

import os

# Just to make it easy, leave any global vars at the top, so it will be easier to find.
settings_file = 'settings.txt'

class settings:
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
                        val = tuple(map(lambda i:i.replace('\'',''),val.split(',')))
                    ret_settings[key] = val
                
            print(ret_settings)
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

class file:
    def list_path(path):
        filelist = []
        for root, dirs, files in os.walk(path):
            for file in files:
                filelist.append(os.path.join(root,file))
        return filelist
    
    def get_music_files(filelist, ext):
        scan_log = ['','Music File Scan']
        for name in filelist:
            lower_name = name.lower()
            if not lower_name.endswith(ext):
                filelist.remove(name)
        scan_log.append('Found %s files with music extensions' % (len(filelist)))
        return scan_log, filelist

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
        if take_action:
            pre = ''
            logs.append('Take action is enabled, we will %s files.' % (action))
        else:
            pre = '(Log Only) '
            logs.append('Only logging here, not actually going to %s.' % (action))

        for name in filelist:
            logtext = pre+action.title()+': '
            if action == 'delete':
                logtext += '%s' % (name)
                os.remove(name)
            elif action == 'rename':
                src = name.split('||')[0]
                dest = name.split('||')[1]
                logtext += '%s to %s' % (src, dest)
                os.rename(src, dest)
            logs.append(logtext)
        return logs

    def dump_log(logfile, log):
        log_file = open(logfile,'w')
        for item in log:
            log_file.write(item+'\n')
        log_file.close() 