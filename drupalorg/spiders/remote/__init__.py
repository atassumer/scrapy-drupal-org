from scrapy_parsley.parsley_spider import ParsleyCrawlSpider
from scrapy_parsley.utils.file_system_adapter import FileSystemAdapter
from scrapy_parsley.utils.parselet.parselet import ItemsParselet, LinksParselet


class RemoteParsleySpider(ParsleyCrawlSpider):
    allowed_domains = ["drupal.org"]
    start_urls = [
        "https://drupal.org/project/usage",
    ]

    def _get_links_parselet_path(self):
        return FileSystemAdapter().get_full_path('spiders/remote/remote.links.json')

    def _get_items_parselet_path(self):
        return FileSystemAdapter('spiders').glob('%s.items.json' % self.name)

    def parse_start_url(self, response):
        return LinksParselet(parselet_path=self._get_links_parselet_path()).parse(response, self.parse_items)

    def parse_items(self, response):
        return ItemsParselet(parselet_path=self._get_items_parselet_path()).parse(response)

# todo: profile classes to find bottlenecks
