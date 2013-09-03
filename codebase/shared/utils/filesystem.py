import os
import subprocess
import fnmatch


class FileSystemAdapter:

    _pwd = ""

    def get_full_path(self, relative_path='', target_file=None):
        """
        >>> from codebase.settings import C_CODEBASE_ROOT
        >>> FileSystemAdapter().get_full_path() == C_CODEBASE_ROOT
        True
        >>> FileSystemAdapter().get_full_path('tests/yelp/yelp.items.json') == C_CODEBASE_ROOT + '/tests/yelp/yelp.items.json'
        True
        >>> FileSystemAdapter().get_full_path('.', C_CODEBASE_ROOT + '/tests/yelp/yelp.py') == C_CODEBASE_ROOT + '/tests/yelp'
        True
        >>> FileSystemAdapter().get_full_path('/home') == '/home'
        True
        """
        if relative_path == '/':
            relative_path = '.'
        if relative_path and relative_path[0] == '/':  # fs root_node path
            self._pwd = relative_path
        elif target_file:     # relative path
            self._pwd = os.path.realpath("%s/../%s" % (target_file, relative_path))
        else:               # project root_node path
            self._pwd = os.path.realpath("%s/../../../%s" % (__file__, relative_path))
        return self._pwd

    def chdir(self, relative_path='', target_file=None):
        path = self.get_full_path(relative_path, target_file)
        if os.path.isdir(path):
            self._pwd = path
            os.chdir(self._pwd)
            return self._pwd
        else:
            raise FileSystemAdapterException('ERROR: `%s` is not a directory' % self._pwd)

    def pwd(self):
        if not self._pwd:
            raise FileSystemAdapterException('ERROR: You should specify working directory prior to remote call')
        return self._pwd

    def run(self, command):
        """
        >>> fs = FileSystemAdapter()
        >>> dont_output = fs.chdir('.')
        >>> fs.run('pwd')
        0
        """
        self.pwd()  # make checks
        return os.system(command)

    def run_with_feedback(self, command):
        """
        >>> from codebase.settings import C_CODEBASE_ROOT
        >>> fs = FileSystemAdapter()
        >>> fs.chdir('.') == C_CODEBASE_ROOT
        True
        >>> fs.run_with_feedback('pwd') == C_CODEBASE_ROOT
        True
        """
        self.pwd()  # make checks
        process = subprocess.Popen(command.split(), stdout=subprocess.PIPE)
        return process.stdout.readline().rstrip()

    def glob(self, pattern='*.info'):
        """
        >>> from codebase.settings import C_GIT_ROOT
        >>> fs = FileSystemAdapter()
        >>> dont_output = fs.chdir(C_GIT_ROOT + '/views')
        >>> list(fs.glob('*.info'))[2][-30:]
        'views_export/views_export.info'
        """
        for root, dirnames, filenames in os.walk(self.pwd()):
            for filename in fnmatch.filter(filenames, pattern):
                file_path = os.path.join(root, filename)
                yield file_path


class FileSystemAdapterException(Exception):
    pass