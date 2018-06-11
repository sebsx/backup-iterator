# Simple backup file finder & iterator

## Warning: not tested on Windows


Also, this is a very basic and naïve implementation of the requirements.

### What it does


* searches a path and creates an index based on the filename without extension
* assumes filename is unique (so it won't bother dealing with `file.txt` and `file.doc` separately)
* finds all the files matching some extensions and treats them as backups
* checks the filestamps and reports back older files

### Things missing

* filetype checks based on header or metadata
* can't handle filename sans extension clashes
* doesn't handle files with multiple extensions (e.g. tar.gz)


### How to use it


Basic `unittest` testing is included (`run-tests.py`), it will also handle unpacking the mock data tarfile.

Main client is in the `run.py` file and usage looks like this:

```
./run-tests.py
... tests run ...
./run.py -p ./mock-data
./mock-data/backups/test.bak may be superseded by ./mock-data/new/test.xls
.
.
...
```

### How it works

To see exactly the train of thought and how the data looks like run the `prototype.py` file.

The Iterator does a few things:

1. Scans the path passed to the constructor
2. Builds a `dictionary` data structure to hold the file names, principals and backup files.
3. Finding the older backup files is done by going through the structure above and looking for files with a `mtime` older than what the principal has.
4. Final data structure is a `list` of `tuples` having the form of `[(principal1, backup1), (principal1, backup2), (principal2, backup)]` and so on and so forth.
5. The iterator results can either be stored into a list via a comprehension and simply iterated through and worked on.


Thanks for looking!