from scrapy_parsley.parsley_spider import ParsleyCrawlSpider, CrawlSpider
from scrapy_parsley.utils.overrides_decorator import overrides


class RemoteParsleySpider(ParsleyCrawlSpider):
    allowed_domains = ["drupal.org"]
    start_urls = [
        "https://drupal.org/project/usage",
    ]
    links_parselet = {
        "links(id('project-usage-all-projects')//tr/td/a)": [
            {
                "link": "str:replace(@href, '/project/usage/', 'https://drupal.org/project/')"
            }
        ]
    }

    _items_parselet_dict = None
    _links_parselet_dict = None

    @overrides(CrawlSpider)
    def parse_start_url(self, response):
        return self.apply_links_parselet(response, self.parse_items)

    def parse_items(self, response):
        return self.apply_parselet(response)


# todo: profile classes to find bottlenecks
