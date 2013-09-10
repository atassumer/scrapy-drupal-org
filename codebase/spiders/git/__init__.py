import subprocess
import os
import re
import fnmatch
import string

from codebase.spiders import CodebaseBaseSpider


class GitSpider(CodebaseBaseSpider):
    allowed_domains = ["localhost"]
    start_urls = [
        "http://localhost/git/views/",
    ]
    git_root = 'http://localhost/git/'
    dummy_ini_section_name = 'info'

    supported_packages = {# todo: does the dataset contains any other parameters?
                          # https://drupal.org/node/171205
                          'themes': "name, description, screenshot, version, core, engine, base_theme, "
                                    "regions, features, theme_settings, stylesheets, scripts, php".split(', '),
                          # https://drupal.org/node/231036
                          'drupal6': ['name', 'description', 'core',
                                      'php', 'hidden', 'version', 'project'],
                          # `package` and `dependencies` are excluded
                          # https://drupal.org/node/542202
                          'drupal7': ['name', 'description', 'core', 'stylesheets', 'scripts', 'files',
                                      'package', 'php', 'version', 'configure', 'required', 'hidden', 'project'],
                          # python: `set(b1).intersection( set(b2) )`
                          'both_versions': ['php', 'package', 'core', 'name', 'version', 'description', 'hidden'],
                          'any_version': [],
    }

    def parse(self, response):
        # # content of the scraped page have no affect on script workflow
        root_directories = [
            '/usr/share/drupal6/modules/',
            # '/usr/share/drupal7/modules/',
            '/var/www/git'
        ]
        for directory in root_directories:
            for item in self.parseRootDirectory(directory):
                yield item

    def parseRootDirectory(self, directory):
        sub_directories = self.getTopLevelDirectoriesAkaProjects(directory)
        for project in sub_directories:
            full_subdirectory = "%s/%s" % (directory, project)
            for item in self.parseSubDirectory(full_subdirectory, project):
                yield item

    def parseSubDirectory(self, path, project):
        for root, dirnames, filenames in os.walk(path):
            for filename in fnmatch.filter(filenames, '*.info'):
                file_path = os.path.join(root, filename)
                module = re.search("^(.*?)\.info$", filename).group(1)
                for item in self.parseFile(file_path, module, project):
                    yield item

    def parseFile(self, file_path, module, project):
        # this method should be overridden
        pass

    # utility methods
    def trim(self, value):
        value = re.search("^[\s'\"]*(.*?)[\s'\"]*$", value).group(1)
        if value[-2:] == '[]':
            value = value[:-2]
        return value

    def getTopLevelDirectoriesAkaProjects(self, directory):
        return [name for name in os.listdir(directory) if os.path.isdir(os.path.join(directory, name))]

    def get_version(self, project, file_path):
        if string.find(file_path, '/var/www/git') != -1:
            command = 'git describe --tags'
            self.go_to_project_dir('/var/www/git', project)
            process = subprocess.Popen(command.split(), stdout=subprocess.PIPE)
            tag = process.stdout.readline().rstrip()
            return tag
        else:
            for line in open(file_path):
                buff = self.parse_line(line, 'version')
                if buff and buff != 'VERSION':
                    return buff

    def parse_line(self, line, marker):
        if line[0:len(marker)] == marker and string.find(line, '=') != -1:
            value = re.search('=\s*(.*?)$', line).group(1)
            return self.trim(value)
        return False
