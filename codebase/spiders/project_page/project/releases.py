from scrapy.selector import HtmlXPathSelector

from codebase.items.project_page.project.release import Release, release_title_format
from codebase.spiders.project_page import ProjectPageSpider
from codebase.items.project_page.project.project import project_title_format


class ProjectPageProjectReleasesSpider(ProjectPageSpider):
    name = "releases"

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

        return self.get_releases_rows(hxs, project_machine_name)

    def get_release_row(self, hxs, project_machine_name, quality, version):
        return get_release_row(hxs, project_machine_name, quality, version)  # see below

    def get_releases_rows(self, hxs, project_machine_name):
        supported_qualities = ['ok', 'warning', 'error']
        supported_versions = [5, 6, 7, 8]
        for quality in supported_qualities:
            for version_major in supported_versions:
                item = self.get_release_row(hxs, project_machine_name, quality, version_major)
                if item:
                    yield item


release_row_xpath = "//div[@class='download-table download-table-%s']//tr[contains(.,'%s.x')]/td"


# utility function outside of the class
def get_release_row(hxs, project_machine_name, quality, version):
    cells = hxs.select(release_row_xpath % (quality, version))
    if len(cells) != 4:
        return False
    item = Release()
    item['project_machine_name'] = project_machine_name
    item['project_machine_name_reference'] = project_title_format % project_machine_name
    item['quality'] = quality
    version_visible = cells[0].select('a/text()')
    item['version_visible'] = version_visible.extract()
    item['version_major'] = version
    item['version_minor'] = version_visible.re('\-(\d)\.')
    item['version_patch_level'] = version_visible.re('\-\d\.(\w)')
    item['is_created_manually'] = not (bool(version_visible.re('dev')))
    item['zip_filesize_visible'] = cells[1].select('a[1]/span/text()').re('\((.*?)\)')
    # todo: add calculated fields
    item['date_visible'] = cells[2].select('text()').re('[\w-]+')
    # todo: add calculated fields
    item['notes_link'] = cells[3].select('a/@href').extract()
    item['description'] = 'NA'
    item['title'] = release_title_format % (item['project_machine_name'], item['version_major'], item['quality'])
    return item
