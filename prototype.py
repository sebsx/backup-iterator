#!/usr/bin/env python3

import os
import time
import pprint as pp
import re

test_path = './data'
test_data = {}

# extend as needed
backup_exts = ['bak\d*', 'bk\d+', 'backup\d*']
backup_regex = re.compile(r'(\w)(\.)(%s)' % '|'.join(backup_exts), re.IGNORECASE)

print ('--- scan path and build data structure ---')
# build test data structure
for (path, dirs, files) in os.walk(test_path):
    for file_name in files:
        # naive split, doesn't account for multiple extensions
        (name, extension) = file_name.split('.')

        # grab fstat
        fstat = os.stat(os.path.join(path, file_name))

        # init data structure for file_name
        if not name in test_data:
            test_data[name] = {'backups': [], 'principal': {}}

        # run the regex
        if backup_regex.search(file_name):
            print('{:s}.{:s} looks like a backup'.format(name, extension))
            # there can be multiple backups so append to a list
            test_data[name]['backups'].append({'ext': extension, 'path': path, 'mtime': fstat.st_mtime})
        else:
            print('{:s}.{:s} looks like a principal'.format(name, extension))
            # assumption is there is only one principal
            test_data[name]['principal'] = {
                'ext': extension, 'path': path, 'mtime': fstat.st_mtime}

# dump data structure
print('--- data dump ---')
pp.pprint(test_data)

print('--- sample results ---')
# try out the logic, compare file mtime, older is backup
for file in test_data:
    ext = test_data[file]['principal']['ext']

    if len(test_data[file]['backups']) > 0:
        # scan for older backups
        principal_mtime = test_data[file]['principal']['mtime']
        for backup in test_data[file]['backups']:
            if backup['mtime'] < principal_mtime:
                print('file {:s}.{:s} has older backup {:s}'.format(file, ext, backup['ext']))
    else:
        print('file {:s}.{:s} has no backups'.format(file, ext))
