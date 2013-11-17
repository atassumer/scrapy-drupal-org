import pickle
import os

from scrapy_parsley.tests.file_system_adapter import FileSystemAdapter


class Dump:
    """
    >>> structure = {'key': 'value'}
    >>> obj = Dump('test_Dump')
    >>> obj.dump(structure)
    >>> obj.load()
    {'key': 'value'}
    """

    name = ""
    path = ""

    def __init__(self, name):
        self.name = name
        self.path = FileSystemAdapter().get_full_path('../../files/pickle/%s.dump' % self.name)

    def dump(self, value):
        fp = open(self.path, 'w')
        return pickle.dump(value, fp)

    def load(self):
        fp = open(self.path, 'r')
        return pickle.load(fp)

    def exists(self):
        return os.path.exists(self.path)
