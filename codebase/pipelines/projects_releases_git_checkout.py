from codebase.shared.utils.file_system_adapter import FileSystemAdapter
from codebase.settings import C_CONTRIBUTED_PROJECTS_ROOT


class ProjectsReleasesGitCheckoutPipeline(object):

    def process_item(self, current_item, current_spider):
        if current_spider.name == "projects_releases":
            project_machine_name = current_item['project_machine_name']
            tag = current_item['tag']
            self._git_checkout(project_machine_name, tag)
        return current_item

    def _git_checkout(self, project_machine_name, tag):
        fs = FileSystemAdapter()
        fs.chdir("%s/%s" % (C_CONTRIBUTED_PROJECTS_ROOT, project_machine_name))
        fs.run("git checkout %s" % tag)