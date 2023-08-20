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

def startup():
    log = []
    settings = {}
    settings = shared.settings.read()
    take_action = shared.input.truefalse(settings['take_action'])
    log.append('Searching folder: %s' % (settings['music_folder']))
    filelist = shared.file.list_path(settings['music_folder'])
    log.append('Found %s files in the folder and subfolders.' % (len(filelist)))
    scan_logs,file_list,dupe_list,delete_list,rename_list,ignore_list = shared.file.process(filelist,settings['extensions'])
    log.append('\nScan findings: \nNo Modifications Needed: %s\nDuplicates: %s\nRenames Needed: %s\nIgnored Files: %s\nDeleted Files: %s' % (len(file_list),len(dupe_list),len(rename_list),len(ignore_list),len(delete_list)))
    if shared.input.truefalse(settings['show_scanlogs']):
        log += scan_logs
    log += shared.file.delete_files(delete_list, False if not take_action else shared.input.truefalse(settings['del_deletelist']))
    log += shared.file.delete_files(dupe_list, False if not take_action else shared.input.truefalse(settings['del_duplicates']))
    shared.file.dump_log(settings['logfile'],log)
startup()