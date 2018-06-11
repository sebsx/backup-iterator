#!/usr/bin/env python3
from modules import backupiterator as bf
import unittest
import tarfile


class BackupIteratorTest(unittest.TestCase):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.results = [(file, backup) for (file, backup) in bf.BackupIterator('./mock-data')]

    def testResultsNotNndefined(self):
        self.assertIsNot(None, self.results)

    def testResultsCount(self):
        self.assertEqual(8, len(self.results))

    def testResultsContain(self):
        self.assertIn(('./mock-data/files/figures.dat',
                       './mock-data/new/figures.bk7'), self.results)

if __name__ == '__main__':
    tar = tarfile.TarFile('mock-data.tar', 'r')
    tar.extractall('.')
    tar.close()

    unittest.main()
