from scrapy.http import Request
from scrapy.spider import BaseSpider

from codebase import settings  # todo: get rid of external dependencies like this
from codebase.shared.utils.file_system_adapter import FileSystemAdapter
from codebase.shared.utils.parselet import ItemsParselet, LinksParselet
from codebase.shared.utils.overrides_decorator import overrides, can_be_overridden


class ParsleySpider(BaseSpider):
    """
    Scrapy's BaseSpider have only one parsing callback: BaseSpider.parse()
    ParsleySpider adds six others:
    .parse_items() and .parse_links()
    .get_items_parselet_path() and .get_links_parselet_path()
    .collect_items_manually() and .collect_links_manually()

    To ensure you spelled callback name correctly, you can use the following decorator notation:

    `from codebase.shared.utils.overrides_decorator import ParsleySpider, overrides
    @overrides(ParsleySpider)
    def parse_items(self):
        return []`

    >>> # the same operations as in the class
    >>> from pyparsley import PyParsley
    >>> fs = FileSystemAdapter()
    >>> let_file = open(fs.get_full_path('tests/yelp/tests_yelp.items.json')).read()
    >>> html_file = open(fs.get_full_path('tests/yelp/yelp.html')).read()
    >>> parselet = PyParsley(let_file)
    >>> parselet.parse(string=html_file, allow_net=False, allow_local=False)['reviews'][0]['date']
    '7/5/2013'
    """
    # todo: class methods should accept relative paths. Make tests for that?
    # todo: make tests for each method?

    @overrides(BaseSpider)
    def parse(self, response):
        for item in self.parse_items(response):
            yield item

        try:
            counter = settings.C_PAGES_LIMIT
        except AttributeError:
            counter = -1

        for link_dict in self.parse_links(response):
            counter -= 1
            if counter == 0:
                return
            url = link_dict['url']
            callback = link_dict['callback'] or self.parse
            yield Request(url=url, callback=callback)

    @can_be_overridden()
    def parse_items(self, response):
        for item in self.collect_items_manually(response):
            yield item
        parselet = ItemsParselet(response, self.get_items_parselet_path())
        for item in parselet.collect(self.name):
            yield item

    @can_be_overridden()
    def parse_links(self, response):
        for link in self.collect_links_manually(response):
            yield {'url': link}

        links_parselet_file = self.get_links_parselet_path()
        if links_parselet_file:
            parselet = LinksParselet(response, links_parselet_file)
            for link in parselet.collect():
                yield {'url': link}

    @can_be_overridden()
    def get_items_parselet_path(self):
        fs = FileSystemAdapter()
        fs.chdir(fs.get_full_path('.'))
        return fs.glob("%s.items.json" % self.name).next()

    @can_be_overridden()
    def get_links_parselet_path(self):
        """
        Should have the following structure: ['links']['link']
        """
        return None

    @can_be_overridden()
    def collect_items_manually(self, response):
        return []

    @can_be_overridden()
    def collect_links_manually(self, response):
        return []
