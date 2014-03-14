from scrapy.exceptions import DropItem

from drupalorg import settings
from scrapy_parsley.src.utils.file_system_adapter import FileSystemAdapter


class ProjectsLinkedDropSelfLinkedPipeline(object):
    fs = FileSystemAdapter(settings.PARSLEY_CONTRIBUTED_PROJECTS_ROOT)

    def process_item(self, current_item, current_spider):
        if current_spider.name == "projects_linked" and current_item['linked_from'] == current_item['linked_to']:
            raise DropItem("Self-linked item")
        return current_item
