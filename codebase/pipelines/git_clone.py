from codebase.shared.utils.filesystem import FileSystemAdapter
from codebase.settings import C_GIT_ROOT


class GitClonePipeline(object):

    def process_item(self, current_item, current_spider):
        if current_spider.name == "projects_releases":
            project_machine_name = current_item['project_machine_name']
            self._git_clone(project_machine_name)
        return current_item

    def _git_clone(self, project_machine_name):
        fs = FileSystemAdapter()
        print fs.chdir(C_GIT_ROOT)
        fs.run("git clone --no-checkout http://git.drupal.org/project/%s.git" % project_machine_name)