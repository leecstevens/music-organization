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

music_folder = shared.settings.get('music_folder')
dbname = shared.settings.get('sqlitedb')
conn = shared.sqlite.connect(dbname)
print (music_folder)
filelist = shared.file.list_path(music_folder,True)
for i in range(5):
    print('/'.join(filelist[i].split('/')[1:]))
conn.close()