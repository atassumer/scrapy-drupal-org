import os

from scrapy.spider import BaseSpider


class CodebaseBaseSpider(BaseSpider):
    git_root = None
    target_version = '6'
    target_quality = 'ok'

    def get_file_dir(self):
        return os.path.dirname(os.path.realpath(__file__))

    def go_to_project_dir(self, root, project_machine_name=""):
        root = os.path.realpath(root)
        os.chdir("%s/%s" % (root, project_machine_name))
