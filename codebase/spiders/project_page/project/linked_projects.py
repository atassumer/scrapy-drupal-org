from scrapy.selector import HtmlXPathSelector

from codebase.items.project_page.project.linked_project import LinkedProject, linked_project_title_format
from codebase.items.project_page.project.project import project_title_format


# todo: table for projects, linked in description
from codebase.spiders.project_page import ProjectPageSpider


class ProjectPageLinkedProjectSpider(ProjectPageSpider):
    name = "linked_projects"

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
            return
        yield self.get_related_projects_rows(hxs, response.url)

    def get_related_projects_rows(self, hxs, url):
        related_projects = hxs.select("//div[@class='node-content']//a[contains(@href, 'http://drupal.org/project/') "
                                      "and not(contains(@href, '?'))]/@href").re("[\w\-_]+$")
        for rp in related_projects:
            item = LinkedProject()
            item['link_from'] = url
            item['link_from_reference'] = project_title_format % item['link_from']
            item['link_to'] = rp
            item['link_to_reference'] = project_title_format % item['link_to']
            item['description'] = 'NA'
            item['title'] = linked_project_title_format % (item['link_from'], item['link_to'])
            yield item
