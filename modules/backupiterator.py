import re
import os

class BackupIterator:
    # can be easily moved to be an argument instead of a static list
    extension_list = ['bak\d*', 'bk\d+', 'backup\d*']

    def __init__(self, path):
        self.regex = re.compile(r'(\w)(\.)(%s)' %
                                  '|'.join(self.extension_list), re.IGNORECASE)
        self.path = path
        # initial data structure
        self.scan_data = self.build_data()
        # final data structure is a list of tuples
        self.data = self.transform_data()
        self.index = len(self.data)

    def __iter__(self):
        return self

    def __next__(self):
        if self.index == 0:
            raise StopIteration
        self.index = self.index - 1
        return self.data[self.index]

    def build_data(self):
        data = {}
        for (path, dirs, files) in os.walk(self.path):
            for file_name in files:
                # naive split, doesn't account for multiple extensions
                (name, extension) = file_name.split('.')
                # grab fstat
                stats = os.stat(os.path.join(path, file_name))
                # init data structure for file_name
                if not name in data:
                    data[name] = {'backups': [], 'principal': {}}
                # run the regex
                if self.regex.search(file_name):
                    # there can be multiple backups so append to a list
                    data[name]['backups'].append(
                        {'ext': extension, 'path': path, 'mtime': stats.st_mtime})
                else:
                    # assumption is there is only one principal
                    data[name]['principal'] = {
                        'ext': extension, 'path': path, 'mtime': stats.st_mtime}
        return data

    def transform_data(self):
        data = []
        for file in self.scan_data:
            file_ext = self.scan_data[file]['principal']['ext']
            file_path = self.scan_data[file]['principal']['path']

            if len(self.scan_data[file]['backups']) > 0:
                # scan for older backups
                principal_mtime = self.scan_data[file]['principal']['mtime']
                for backup in self.scan_data[file]['backups']:
                    if backup['mtime'] < principal_mtime:
                        principal_file = os.path.join(file_path, '{:s}.{:s}'.format(file, file_ext))
                        backup_file = os.path.join(backup['path'], '{:s}.{:s}'.format(file, backup['ext']))
                        data.append((principal_file, backup_file))
        return data
