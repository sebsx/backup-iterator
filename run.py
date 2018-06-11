#!/usr/bin/env python3
from modules import backupiterator as bf
import optparse

def main():
    parser = optparse.OptionParser()
    parser.add_option('-p', '--path')
    opts, args = parser.parse_args()

    if opts.path == None:
        print("Usage: run.py -p PATH")
        exit()

    backup_list = [(file, backup) for (file, backup) in bf.BackupIterator(opts.path)]
    # print('\n# Found {} potential older backups\n'.format(len(backup_list)))
    for (file, backup) in backup_list:
        print('{:s} may be superseded by {:s}'.format(backup, file))

if __name__ == '__main__':
    main()
