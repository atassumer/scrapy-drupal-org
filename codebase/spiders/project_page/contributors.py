from scrapy.selector import HtmlXPathSelector

from codebase.items.project_page.contributor import Contributor, contributor_title_format
from codebase.spiders.project_page import ProjectPageSpider


class ProjectPageContributorsSpider(ProjectPageSpider):
    name = "contributors"

    # scrapy crawl myspider -a category=electronics
    def parse_project_page(self, response):
        """
        The lines below is a spider contract. For more info see:
        http://doc.scrapy.org/en/latest/topics/contracts.html

        @url http://localhost/scrapy-webpages/Follow-up%20_%20drupal.org.htm
        @returns items 1 16
        @scrapes description
        """

        hxs = HtmlXPathSelector(response)
        project_machine_name, project_visible_name = self.get_project_ids(hxs, response)
        if not self.validated(hxs, response.url, project_visible_name):
            return []
        return self.collect_user_data(hxs)

    def collect_user_data(self, hxs):
        item = Contributor()
        item['name'] = hxs.select("//div[@class='submitted']/a/text()").extract()  # merlinofchaos
        item['uid'] = hxs.select("//div[@class='submitted']/a/@href").extract()[0] \
            .replace('/user/', '')   # /user/26979
        item['link'] = "%s%s" % ("https://drupal.org/user/", item['uid'])
        item['description'] = 'NA'
        item['title'] = contributor_title_format % item['uid']
        yield item
