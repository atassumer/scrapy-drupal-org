from codebase.shared.utils.file_system_adapter import FileSystemAdapter
from scrapy.conf import get_project_settings


class ProjectsContributedGitClonePipeline(object):
    fs = FileSystemAdapter(get_project_settings()['C_CONTRIBUTED_PROJECTS_ROOT'])

    def process_item(self, current_item, current_spider):
        if current_spider.name == "projects_releases":
            project_machine_name = current_item['project_machine_name']
            self._git_clone(project_machine_name)
        return current_item

    def _git_clone(self, project_machine_name):
        self.fs.run("git clone --no-checkout http://git.drupal.org/project/%s.git" % project_machine_name)
