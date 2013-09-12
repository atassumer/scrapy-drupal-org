from scrapy_parsley.spiders.parsley_spider import ParsleySpider
from scrapy_parsley.utils.file_system_adapter import FileSystemAdapter
from drupalorg.utils.dump import Dump
from scrapy_parsley.spiders.parsley_spider import overrides


class RemoteParsleySpider(ParsleySpider):
    """
    
    """
    allowed_domains = ["drupal.org"]
    start_urls = [
        "https://drupal.org/project/usage",
    ]

    @overrides(ParsleySpider)
    def get_links_parselet_path(self):
        return FileSystemAdapter().get_full_path('spiders/parsley/remote/remote.links.json')

    @overrides(ParsleySpider)
    def parse_items(self, response):
        if response.url in self.start_urls:
            return []
        return [item for item in super(RemoteParsleySpider, self).parse_items(response)]

    @overrides(ParsleySpider)
    def parse_links(self, response):
        dump = Dump('drupalorg_projects')
        if dump.exists():  # todo: implement caching in other places?
            links_dict = dump.load()
        else:
            links_dict = list(super(RemoteParsleySpider, self).parse_links(response))
            dump.dump(links_dict)
        for i in range(len(links_dict)):
            url = links_dict[i]['url']
            yield {'url': url, 'callback': self.parse_items}
