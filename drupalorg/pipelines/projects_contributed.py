from drupalorg import settings

from scrapy_parsley.src.utils.file_system_adapter import FileSystemAdapter


class ProjectsContributedGitClonePipeline(object):
    fs = FileSystemAdapter(settings.PARSLEY_CONTRIBUTED_PROJECTS_ROOT)

    def process_item(self, current_item, current_spider):
        if current_spider.name == "projects_releases":
            project_machine_name = current_item['release_project_machine_name']
            self._git_clone(project_machine_name)
        return current_item

    def _git_clone(self, project_machine_name):  # todo
        # self.fs.run("git clone --no-checkout http://git.drupal.org/project/%s.git" % project_machine_name)
        pass