from drupalorg.spiders.parsley.remote import RemoteParsleySpider
from scrapy_parsley.utils.parselet.parselet import ItemsParselet
from scrapy_parsley.parsley_spider import ParsleyCrawlSpider, overrides


class OtherRemoteParsleySpider(RemoteParsleySpider):
    """
    
    """


class ContributorsOtherRemoteParsleySpider(OtherRemoteParsleySpider):
    """

    """
    name = 'other_contributors'


class TopOtherRemoteParsleySpider(OtherRemoteParsleySpider):
    """

    """
    name = "other_top"

    @overrides(ParsleyCrawlSpider)
    def parse_links(self, response):  # overridden
        return []

    @overrides(ParsleyCrawlSpider)
    def _apply_parselet(self, response):  # overridden
        parselet = ItemsParselet(response, self.get_items_parselet_path())
        return [item for item in parselet.collect()]