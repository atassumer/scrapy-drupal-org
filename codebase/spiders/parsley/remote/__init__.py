from codebase.shared.spiders.parselet.parsley_spiders import ParsleySpider
from codebase.shared.utils.filesystem import FileSystemAdapter
from codebase.utils.dump import Dump


class RemoteParsleySpider(ParsleySpider):
    """
    
    """
    allowed_domains = ["drupal.org"]
    start_urls = [
        "https://drupal.org/project/usage",
    ]

    def get_links_parselet_path(self):
        return FileSystemAdapter().get_full_path('spiders/parsley/remote/remote.links.json')

    def parse_items(self, response):  # todo: should this behaviour be moved to the root_node class?
        if response.url in self.start_urls:
            return
        for item in super(RemoteParsleySpider, self).parse_items(response):
            yield item

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
