from codebase.spiders.git import GitSpider
from codebase.items.project_page.project.project import Project, project_title_format


class GitCoreProjectsSpider(GitSpider):
    name = 'core_projects'

    def parse(self, response):
        # # content of the scraped page have no affect on script workflow
        root_directories = [
            '/usr/share/drupal6/modules/',
            # '/usr/share/drupal7/modules/',
        ]
        for directory in root_directories:
            for item in self.parseRootDirectory(directory):
                yield item

    # parseRootDirectory and parseSubDirectory are implemented in one of the parent classes

    def parseFile(self, file_path, module, project):
        item = Project()
        item['machine_name'] = project
        item['node_alias'] = '%s/%s' % ('project', project)
        item['top_position'] = 'core'
        item['description'] = '<p>'
        item['title'] = project_title_format % project

        for line in open(file_path):
            visible_name = self.parse_line(line, "name")
            if visible_name:
                item['visible_name'] = visible_name
                break
        for line in open(file_path):
            visible_name = self.parse_line(line, "description")
            if visible_name:
                item['description'] += visible_name
                break
        item['description'] += "</p><p><strong>Included in Drupal Core</strong></p>"
        yield item
