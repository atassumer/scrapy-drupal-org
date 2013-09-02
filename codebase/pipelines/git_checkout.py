from codebase.shared.utils.filesystem import FileSystemAdapter
from codebase.settings import C_GIT_ROOT


class GitCheckoutPipeline(object):

    def process_item(self, current_item, current_spider):
        if current_spider.name == "projects_releases":
            project_machine_name = current_item['project_machine_name']
            tag = current_item['tag']
            self._git_checkout(project_machine_name, tag)
        return current_item

    def _git_checkout(self, project_machine_name, tag):
        fs = FileSystemAdapter()
        fs.chdir("%s/%s" % (C_GIT_ROOT, project_machine_name))
        fs.run("git checkout %s" % tag)