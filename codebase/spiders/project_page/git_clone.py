import os
from scrapy.selector import HtmlXPathSelector
from codebase.spiders.project_page import ProjectPageSpider
from codebase.spiders.project_page.project.releases import get_release_row


class GitCloneSpider(ProjectPageSpider):
    name = "clone"

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

        row = get_release_row(hxs, project_machine_name, self.target_quality, self.target_version)
        if not row:
            return None
        tag = row['version_visible']
        if tag and len(tag):
            tag = tag[0]
            self.log("tag: %s" % tag)
        else:
            self.log("tag with given parameters not found")
            return
        self.log("%s %s" % (project_machine_name, tag))
        if tag:
            self.clone(project_machine_name)
            self.checkout(project_machine_name, tag)

    def clone(self, project_machine_name):
        self.go_to_project_dir('/var/www/git/')
        os.system("git clone --no-checkout http://git.drupal.org/project/%s.git" % project_machine_name)
        # if it's already cloned it will print the following message:
        # *fatal: destination path 'views' already exists and is not an empty directory.*

    def checkout(self, project_machine_name, tag):
        self.go_to_project_dir('/var/www/git/', project_machine_name)
        os.system("git checkout %s" % tag)
