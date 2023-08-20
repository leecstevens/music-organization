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
                val = line
                if val[0] != '#':
                    ret_settings[val.split(':')[0]] = val.split(':')[1].replace('\n','')
            
            return ret_settings
        except FileNotFoundError:
            print('File is missing.  Make sure you have a %s in the script folder.' % (settings_file))
        except:
            print('Something is really messed up beyond a standard file not found.\nLooking for %s.' % (settings_file))

class file:
    def list_path(path):
        filelist = []
        for root, dirs, files in os.walk(path):
            for file in files:
                filelist.append(os.path.join(root,file))
        return filelist
    
    def process(filelist, ext):
        dupe_list = []
        delete_list = []
        rename_list = []
        ignore_list = []
        extensions = tuple(list(ext.split(',')))
        for name in filelist:
            lower_name = name.lower()
            if '.ds_store' in lower_name:
                delete_list.append(name)
                filelist.remove(name)
            elif not lower_name.endswith(extensions):
                ignore_list.append(name)
                filelist.remove(name)
            else:
                if 'm4a' in name:
                    newname = name[:-4]+'.mp3'
                    if newname in [f.lower() for f in filelist]:
                        dupe_list.append(newname)
                        filelist.remove(name)
                for i in range(1,5):
                    newname = name[:-4] + str(i) + name[-4::]
                    if name in filelist and newname in filelist:
                        dupe_list.append(newname)
                        filelist.remove(newname)
        
        for name in filelist:
            fullname = os.path.split(name)[0]
            filename = os.path.split(name)[1]
            
            if filename.split(' ')[0].isnumeric():
                if int(filename.split(' ')[0]) <= 20:
                    filename = ' '.join(filename.split(' ')[1::])
                    newname = '/'.join(fullname)+'/'+filename
                    rename_list.append(newname)




        return filelist,dupe_list,delete_list,rename_list,ignore_list
    
    def dump_log(logfile, log):
        log_file = open(logfile,'w')
        for item in log:
            log_file.write(item+'\n')
        log_file.close() 