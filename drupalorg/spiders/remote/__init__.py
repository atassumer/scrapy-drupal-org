from scrapy_parsley.source_code.parsley_wrappers.parser.implementations import ParserImplementations
from scrapy_parsley.source_code.scrapy_wrappers.spider import ParsleyCrawlSpider


class RemoteParsleySpider(ParsleyCrawlSpider):
    allowed_domains = ["drupal.org"]
    start_urls = [
        "https://drupal.org/project/usage",
    ]
    requests_parselet = {
        "links(id('project-usage-all-projects')//tbody/tr)": [
            {
                "link": "str:replace(td a @href, '/project/usage/', 'https://drupal.org/project/')",
                #"link": "//a/@href",
            }
        ]
    }

    _items_parselet_dict = None
    _links_parselet_dict = None

    def parse_start_url(self, response):
        return self.apply_requests_parselet(
            callback=self.parse_items,
            response=response,
            override_parser=ParserImplementations.FIZX,
            cache_key='drupalorg_projects'
        )

    def parse_items(self, response):
        return self.apply_items_parselet(response, override_parser=ParserImplementations.REDAPPLE)


# todo: profile classes to find bottlenecks
