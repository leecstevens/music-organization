"""

    Music Consolidation project - Lee Stevens
    Released on the "you break something, not my fault" license.
    
    May this be useful to you as well as a good learning tool for you.
    The main code repository if you stole / slash and hacked it is here:

    https://github.com/leecstevens/music-organization

    This code is meant to be quick and dirty, I'm sure there are
    other/better ways of doing things.  We're all IT people and have
    our own set in our ways things.  Suggestions welcomed, but not always
    followed.

"""

import shared
settings = {}

def startup():
    global settings
    settings = shared.settings.read()
    print(settings)
    

startup()
print (settings['music_folder'])