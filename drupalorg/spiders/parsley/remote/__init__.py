from scrapy_parsley.parsley_spider import ParsleyCrawlSpider
from scrapy_parsley.utils.file_system_adapter import FileSystemAdapter
from drupalorg.utils.dump import Dump


class RemoteParsleySpider(ParsleyCrawlSpider):
    allowed_domains = ["drupal.org"]
    start_urls = [
        "https://drupal.org/project/usage",
    ]

    def get_links_parselet_path(self):
        return FileSystemAdapter().get_full_path('spiders/parsley/remote/remote.links.json')

    def _apply_parselet(self, response):
        if response.url in self.start_urls:
            return []
        return super(RemoteParsleySpider, self)._apply_parselet(response)

    def parse_links(self, response):
        dump = Dump('drupalorg_projects')
        if dump.exists():  # todo: implement caching in other places?
            links_dict = dump.load()
        else:
            links_dict = list(super(RemoteParsleySpider, self).parse_links(response))
            dump.dump(links_dict)
        for i in range(len(links_dict)):
            url = links_dict[i]['url']
            yield {'url': url, 'callback': self._apply_parselet}

            # todo: profile classes to find bottlenecks