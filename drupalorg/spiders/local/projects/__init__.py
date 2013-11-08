from drupalorg.spiders.local import LocalSpider
from scrapy_parsley.scrapy_parsley2.file_system_adapter import FileSystemAdapter
from drupalorg.settings import PARSLEY_CORE_PROJECTS_ROOT
from scrapy_parsley.scrapy_parsley2.parsley_item import ScrapyItemListWrapper


class ProjectsLocalSpider(LocalSpider):
    """

    """
    allowed_domains = ["localhost"]
    start_urls = [
        "http://localhost/",
    ]


class CoreProjectsLocalSpider(ProjectsLocalSpider):
    """
    Runs in less then a second
    """
    name = 'projects_core'

    def parse(self, response):
        fs = FileSystemAdapter(PARSLEY_CORE_PROJECTS_ROOT)
        projects = fs.get_subdirectories_names()
        for project in projects:
            data = dict()
            data['machine_name'] = project
            data['project_uid'] = 0
            data['project_maintenance_status'] = 'Core module'
            data['project_development_status'] = 'Core module'

            item = ScrapyItemListWrapper(data.keys())
            for key, value in data.iteritems():
                item[key] = value
            yield item
