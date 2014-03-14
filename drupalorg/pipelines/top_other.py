from drupalorg import settings
from scrapy_parsley.src.utils.file_system_adapter import FileSystemAdapter


class TopOtherTopCategoriesPipeline(object):
    fs = FileSystemAdapter(settings.PARSLEY_CONTRIBUTED_PROJECTS_ROOT)

    def process_item(self, current_item, current_spider):
        if current_spider.name == "other_top":
            digits_count = len(current_item['top_place'])
            category_title = "TOP 1"
            category_title += "0" * digits_count
            current_item['top_category'] = category_title
        return current_item
