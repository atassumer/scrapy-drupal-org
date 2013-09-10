from scrapy.selector import HtmlXPathSelector

from codebase.items.project_page.project.related_project import RelatedProject, related_project_title_format
from codebase.items.project_page.project.project import project_title_format

from codebase.spiders.project_page import ProjectPageSpider


class ProjectPageRelatedProjectSpider(ProjectPageSpider):
    name = "related_projects"

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

        return self.get_related_projects_rows(hxs, response.url)

    def get_related_projects_rows(self, hxs, url):
        related_projects = hxs.select("//div[@class='block-inner' and contains(.,'Related projects')]//a/@href")
        for rp in related_projects:
            item = RelatedProject()
            item['linked_from'] = url
            item['linked_from_reference'] = project_title_format % item['linked_from']
            item['linked_to'] = rp.extract()
            item['linked_to_reference'] = project_title_format % item['linked_to']
            item['title'] = related_project_title_format % (item['linked_from'], item['linked_to'])
            item['description'] = 'NA'
            yield item