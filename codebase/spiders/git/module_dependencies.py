from codebase.spiders.git import GitSpider
from codebase.items.git.module_dependency import ModuleDependency, module_dependency_title_format
from codebase.items.git.module import module_title_format
from codebase.items.project_page.project.project import project_title_format


class GitModuleDependenciesSpider(GitSpider):
    """
    Before using this module call `scrapy crawl clone`
    """
    name = 'module_dependencies'

    def parseFile(self, file_path, module, project):
        default_item = ModuleDependency()
        default_item['from_version'] = self.get_version(project, file_path)
        default_item['version_major'] = self.target_version
        default_item['quality'] = self.target_quality
        default_item['from_project_reference'] = project_title_format % project
        default_item['from_module_reference'] = module_title_format % (
            module, self.target_version, self.target_quality, project)
        default_item['from_project_machine_name'] = project
        default_item['from_module_machine_name'] = module
        default_item['description'] = "NA"
        for line in open(file_path):
            depends_on = self.parse_line(line, "dependencies")  # module, not project
            if depends_on:
                item = default_item
                item['to_module_machine_name'] = depends_on
                item['title'] = module_dependency_title_format % (
                    module, self.target_version, self.target_quality, project, depends_on)
                yield item
