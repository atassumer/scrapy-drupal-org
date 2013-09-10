import time

from scrapy.selector import HtmlXPathSelector

from codebase.items.project_page.project.project import Project, project_title_format
from codebase.spiders.project_page import ProjectPageSpider
from codebase.items.project_page.contributor import contributor_title_format


class ProjectPageProjectContributedSpider(ProjectPageSpider):
    name = "contributed_projects"

    def parse_project_page(self, response):
        """Usage: `scrapy crawl projects -t csv -o projects.csv`

        The lines below is a spider contract. For more info see:
        http://doc.scrapy.org/en/latest/topics/contracts.html

        @url http://localhost/scrapy-webpages/Follow-up%20_%20drupal.org.htm
        @returns items 1 16
        @scrapes description
        """
        hxs = HtmlXPathSelector(response)
        project_machine_name, project_visible_name = self.get_project_ids(hxs, response)
        if not self.validated(hxs, response.url, project_visible_name):
            return

        item = Project()
        self.append_metadata_fields(hxs, item, project_machine_name, project_visible_name)
        self.append_info_fields(hxs, item)
        self.append_issues_counts(hxs, item)
        item['top_position'] = response.meta['top_position']
        yield item

    def append_issues_counts(self, hxs, item):
        issues = hxs.select("//div[@class='issue-cockpit-categories']//a/text()")
        if len(issues) != 4:  # the block is missing on some pages. for example /project/cvs_deploy
            return
        sparks_format = "//div[@class='issue-cockpit-metrics']" \
                        "/div[contains(.,'%s')]//div[@class='spark-annotation']/text()"
        item['issues_open_count'] = issues[0].re('\d+')
        item['issues_total_count'] = issues[1].re('\d+')
        item['bugreports_open_count'] = issues[2].re('\d+')
        item['bugreports_total_count'] = issues[3].re('\d+')
        item['new_issues_count'] = hxs.select(sparks_format % 'New').extract()
        item['participants_count'] = hxs.select(sparks_format % 'Participants').extract()

    def append_info_fields(self, hxs, item):
        info = hxs.select("//div[@class='project-info item-list']/ul")
        item['uid'] = hxs.select("//div[@class='submitted']/a/@href").extract()[0] \
            .replace('/user/', '')   # /user/26979
        item['uid_reference'] = contributor_title_format % item['uid']
        item['maintenance_status'] = info.select("//li[contains(.,'Maintenance')]/span/a/text()").extract()
        item['development_status'] = info.select("//li[contains(.,'Development')]/span/a/text()").extract()
        item['reported_installs_count'] = info.select("//li[contains(.,'installs')]/strong/text()").extract()
        item['downloads_count'] = "".join(hxs.select("//li[contains(.,'Downloads')]/text()").re('\d+'))
        item['automated_tests_enabled'] = bool(hxs.select(
            "//li[contains(.,'tests')]/text()").re('Enabled'))  # Automated tests: Enabled

    def append_metadata_fields(self, hxs, item, machine_name, visible_name):
        item['visible_name'] = visible_name
        item['machine_name'] = machine_name
        item['node_alias'] = '%s/%s' % ('project', machine_name)
        item['title'] = project_title_format % machine_name
        item['description'] = hxs.select("id('content')").extract()
        item['url'] = hxs.select("id('tabs')/ul/li[1]/a/@href").extract()[0] \
            .replace('/project', 'https://drupal.org/project')  # /project/views
        item['nid'] = hxs.select(
            "id('block-project-development')//ul/li[contains(.,'commits')]/a/@href").re('\d+')
        item['project_created'] = hxs.select("//em/text()").extract()[0] \
            .replace('at', '-').replace(',', '')  # November 25, 2005 at 8:34pm
        item['project_modified'] = hxs.select("//ul/li[contains(.,'modified')]/text()").re('\: (.*?)$')[0] \
            .replace(',', '')  # Last modified: November 7, 2012
        item['latest_scraping_unixtime'] = int(time.time())

        item['image_urls'] = hxs.select("id('content')//a[img and contains(@href, 'files/images/')]/@href").extract()
        if item['image_urls']:
            item['image_urls'] = [item['image_urls'][0]]
