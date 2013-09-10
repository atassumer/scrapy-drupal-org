import string

from codebase.spiders.git import GitSpider
from codebase.items.git.module import Module, module_title_format
from codebase.items.project_page.project.project import project_title_format


class GitModulesSpider(GitSpider):
    name = 'modules'
    config = None

    def parseFile(self, file_path, module, project):  # todo: check how it works with themes
        item = Module()
        self.extractFileData(file_path, item, self.supported_packages['both_versions'])

        item['project_machine_name'] = project
        item['module_machine_name'] = module

        item['version_major'] = self.target_version
        item['quality'] = self.target_quality

        item['project_reference'] = project_title_format % project
        item['title'] = module_title_format % (module, self.target_version, self.target_quality, project)
        yield item

    def extractFileData(self, file_path, item, supported_parameters):
        for line in open(file_path):
            line = line.rstrip()
            if string.find(line, '=') == -1:
                continue
            key, value = string.split(line, "=", maxsplit=1)
            key = self.trim(key)
            value = self.trim(value)
            if key not in supported_parameters:
                continue
            item['info_%s' % key] = value
