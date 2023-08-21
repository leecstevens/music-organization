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

    shared.file.dump_log(settings['logfile'],log)

startup()