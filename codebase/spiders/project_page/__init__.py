import re
from scrapy.http import Request
from scrapy.selector import HtmlXPathSelector
import math
from codebase.spiders import CodebaseBaseSpider


class ProjectPageSpider(CodebaseBaseSpider):
    allowed_domains = ["drupal.org"]
    start_urls = [
        "https://drupal.org/project/usage",
    ]

    def fill_rating(self, positions, length, current_percent, previous_percent):
        term = "top %s" % current_percent + "%"
        percent = current_percent - previous_percent
        count = int(math.floor(length * percent / 100))
        positions += [term] * count
        return positions

    def getProjectsRating(self, length):
        positions = []
        places = [0.1, 0.5, 1, 5, 10, 30, 50, 90]  # top 0.1% to top 90%
        previous_place = 0
        for place in places:
            self.fill_rating(positions, length, place, previous_place)
            previous_place = place
        positions += ['not in the top'] * (length - len(positions))  # because of math.floor
        return positions

    def parse(self, response):  # link extractor
        hxs = HtmlXPathSelector(response)
        table = hxs.select("id('project-usage-all-projects')")
        modules = table.select("id('project-usage-all-projects')//td/a/@href").re('[^/]+$')
        self.log("%s" % len(modules))
        top_positions = self.getProjectsRating(len(modules))
        self.log("%s" % (len(top_positions)))

        modules = modules[0:10]
        self.log("modules count: %s, first module: %s" % (len(modules), modules[0]))
        for i in range(len(modules)):
            url = 'https://drupal.org/project/%s' % modules[i]
            yield Request(url=url, callback=self.parse_project_page, meta={'top_position': top_positions[i]})

    def validated(self, hxs, url, visible_name):
        have_specific_field = hxs.select("//li[contains(.,'Maintenance status')]/span//text()")
        if not len(have_specific_field):  # or not have_specific_field[0].__nonzero__():
            message = "Can't parse: %s, %s, %s, %s" % (url, visible_name, have_specific_field, len(have_specific_field))
            self.log(message)
            return False
        else:
            return True

    def parse_project_page(self, response):
        """
        Should be implemented in descending classes
        """
        self.log('ERROR: ModulesSpider.parse_project_files() should be overridden')

    def get_project_ids(self, hxs, response):
        project_machine_name = re.search('[^/]+$', response.url).group()
        project_visible_name = hxs.select("id('page-subtitle')/text()").extract()
        if project_visible_name:
            project_visible_name = project_visible_name[0]
        return project_machine_name, project_visible_name