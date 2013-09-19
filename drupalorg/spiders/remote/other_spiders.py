from drupalorg.spiders.remote import RemoteParsleySpider


class OtherRemoteParsleySpider(RemoteParsleySpider):
    """
    
    """


class ContributorsOtherRemoteParsleySpider(OtherRemoteParsleySpider):
    """

    """
    name = 'other_contributors'
    parselet = {
        "name": "//div[@class='submitted']/a/text()",
        "link": "//div[@class='submitted']/a/@href",
        "uid": "regexp:match(//div[@class='submitted']/a/@href, '\\d+')"
    }


class TopOtherRemoteParsleySpider(OtherRemoteParsleySpider):
    """

    """
    name = "other_top"
    parselet = {
        "links(id('project-usage-all-projects')//tr)": [
            {
                "link": "str:replace(td a @href, '/project/usage/', 'https://drupal.org/project/')",
                "top": "str:replace(td, '/project/usage/', 'https://drupal.org/project/')"
            }
        ]
    }

    def parse_start_url(self, response):
        return super(TopOtherRemoteParsleySpider, self).parse_items(response)
