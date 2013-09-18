from drupalorg.spiders.remote import RemoteParsleySpider


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

    def parse_start_url(self, response):
        return super(TopOtherRemoteParsleySpider, self).parse_items(response)
