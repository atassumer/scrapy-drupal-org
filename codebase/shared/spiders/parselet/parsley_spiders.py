from scrapy.http import Request
from scrapy.spider import BaseSpider

from codebase import settings  # todo: get rid of external dependencies like this
from codebase.shared.utils.filesystem import FileSystemAdapter
from codebase.shared.utils.parselets import ItemsParselet, LinksParselet


class ParsleySpider(BaseSpider):
    """
    Any method of this class may be redefined in descending classes
    Path attributed may be relative

    >>> # the same operations as in the class
    >>> from pyparsley import PyParsley
    >>> fs = FileSystemAdapter()
    >>> let_file = open(fs.get_full_path('tests/yelp/tests_yelp.items.json')).read()
    >>> html_file = open(fs.get_full_path('tests/yelp/yelp.html')).read()
    >>> parselet = PyParsley(let_file)
    >>> parselet.parse(string=html_file, allow_net=False, allow_local=False)['reviews'][0]['date']
    '7/5/2013'
    """
    # name = "tests"
    # allowed_domains = ["drupal.org"]
    # start_urls = ["http://drupal.org/project/views"]

    def parse(self, response):
        print 'PARSE'
        # raise NotImplementedError("Should have implemented this")
        # todo: implement post-validation as a pipeline
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

    def parse_items(self, response):
        for item in self.collect_items_manually(response):
            yield item
        parselet = ItemsParselet(response, self.get_items_parselet_path())
        for item in parselet.collect(self.name):
            yield item

    def parse_links(self, response):
        for link in self.collect_links_manually(response):
            yield {'url': link}

        links_parselet_file = self.get_links_parselet_path()
        if links_parselet_file:
            parselet = LinksParselet(response, links_parselet_file)
            for link in parselet.collect():
                yield {'url': link}

    def get_items_parselet_path(self):
        fs = FileSystemAdapter()
        fs.chdir(fs.get_full_path('.'))
        return fs.glob("%s.items.json" % self.name).next()

    def get_links_parselet_path(self):
        return None

    def collect_items_manually(self, response):
        return []

    def collect_links_manually(self, response):
        return []