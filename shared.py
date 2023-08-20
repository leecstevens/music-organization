"""

    Since the music app will have several different shared features, 
    no sense in writing things twice (or more).  You agree?

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
                    ret_settings[val.split(':')[0]] = val.split(':')[1]
            
            return ret_settings
        except FileNotFoundError:
            print('File is missing.  Make sure you have a %s in the script folder.' % (settings_file))
        except:
            print('Something is really messed up beyond a standard file not found.\nLooking for %s.' % (settings_file))        