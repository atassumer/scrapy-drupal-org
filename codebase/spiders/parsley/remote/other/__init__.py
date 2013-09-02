from codebase.spiders.parsley.remote import RemoteParsleySpider
from codebase.shared.utils.parselets import ItemsParselet


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

    def parse_links(self, response):  # overridden
        return []

    def parse_items(self, response):  # overridden
        parselet = ItemsParselet(response, self.get_items_parselet_path())
        for item in parselet.collect(self.name):
            yield item
