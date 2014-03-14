"""Dependencies between dumps in RDBMS

Layer 0: *other_contributors
Layer 1: *projects_contributed, *projects_core
Layer 2: projects_linked, projects_related, projects_releases, other_top, *modules_meta
Layer 3: modules_dependencies

* - required for the next level
"""

from drupalorg.spiders.remote import RemoteParsleySpider
from scrapy_parsley.src.parsley_wrappers.parser.implementations import ParserImplementations
from scrapy_parsley.src.scrapy_wrappers.item import ParsletScrapyItem


# extractors
EXTRACTOR_MACHINE_NAME_COINTAINER = "ul.primary li:nth-of-type(1) a @href"  # '/project/entityreference_prepopulate'
EXTRACTOR_NID_COINTAINER = "id('block-project-development')//ul/li[contains(.,'commits')]/a/@href"  # '/node/3238/commits'
EXTRACTOR_UID_COINTAINER = "div.submitted a @href"  # '/user/227'

# regexps. should always use the first found group
REGEXP_MACHINE_NAME = '([^/]+)/?$'
REGEXP_DIGITS_GROUP = '(\\d+)'


class ContributedProjectsRemoteParsleySpider(RemoteParsleySpider):
    name = 'projects_contributed'

    items_parselet = {
        "_id": EXTRACTOR_NID_COINTAINER,
        "project_url": EXTRACTOR_MACHINE_NAME_COINTAINER,
        "project_machine_name": EXTRACTOR_MACHINE_NAME_COINTAINER,
        "project_visible_name": "#page-subtitle",
        "project_uid": EXTRACTOR_UID_COINTAINER,
        "project_description?": ".field-items", # "(//div[@class='field-items'])[last()]"  // todo: make it work
        "project_image_url?": "a.imagecache @href",
        "info(.project-info)": [
            {
                # # all `Maintenance` and `Development` statuses except for `Unknown` wrapped into `a` tag
                "project_maintenance_status": "//li[contains(.,'Maintenance')]/span",
                "project_development_status": "//li[contains(.,'Development')]/span",
                "project_reported_installs?": "//li[strong and contains(.,'Reported installs')]/strong",
                "project_downloads_count?": "//li[contains(.,'Downloads')]",
                "project_automated_tests_status?": "//li[contains(.,'Automated tests: Enabled')]",
                "project_modified": "li.modified",
            }
        ],
        "issues(.issue-cockpit-categories)": [
            {
                "project_issues_open_count": ".issue-cockpit-totals a:nth-of-type(1)",
                "project_issues_total_count": ".issue-cockpit-totals a:nth-of-type(2)",
                "project_bugreports_open_count": ".issue-cockpit-bug a:nth-of-type(1)",
                "project_bugreports_total_count": ".issue-cockpit-bug a:nth-of-type(2)",
            }
        ],
    }

    def parse_items(self, response):
        """ Returns one and only one item

        @url https://drupal.org/project/views
        @returns items 1 1
        @returns requests 0 0
        """
        for item in self.apply_items_parselet(response, override_parser=ParserImplementations.REDAPPLE):
            item.extract('_id', REGEXP_DIGITS_GROUP, 1)
            item.replace('project_url', '^/', 'https://drupal.org/')
            item.extract('project_machine_name', REGEXP_MACHINE_NAME, 1)
            item.extract('project_uid', REGEXP_DIGITS_GROUP, 1)
            item.replace('project_downloads_count', '\D', '')  # todo: check
            item.replace('project_automated_tests_status', '^.*?Automated tests: Enabled.*?$', 'Enabled')
            item.replace('project_automated_tests_status', '^$', 'Disabled')  # todo check
            item.extract('project_modified', '^Last modified: (.*?)$', 1)
            item.replace('project_modified', ',', '')
            item.extract('project_issues_open_count', REGEXP_DIGITS_GROUP, 1)
            item.extract('project_issues_total_count', REGEXP_DIGITS_GROUP, 1)
            item.extract('project_bugreports_open_count', REGEXP_DIGITS_GROUP, 1)
            item.extract('project_bugreports_total_count', REGEXP_DIGITS_GROUP, 1)
            yield item


class LinkedProjectsRemoteParsleySpider(RemoteParsleySpider):
    name = 'projects_linked'
    items_parselet = {
        "linked_from?": EXTRACTOR_MACHINE_NAME_COINTAINER,
        "to_links(//div[@class='node-content']"  # todo: optimize string length
        + "//a[contains(@href, 'drupal.org/project/') and not(contains(@href, '?'))])": [
            {
                "linked_to": "@href"
            }
        ]
    }  # works with both parsers

    def parse_items(self, response):
        """ VIEWS linked to CTOOLS and ADVANCED_HELP

        @url https://drupal.org/project/views
        @returns items 2 2
        @returns requests 0 0
        """
        for item in self.apply_items_parselet(response, override_parser=ParserImplementations.REDAPPLE):
            item.extract('linked_from', REGEXP_MACHINE_NAME, 1)
            item.extract('linked_to', REGEXP_MACHINE_NAME, 1)
            yield item


class RelatedProjectsRemoteParsleySpider(RemoteParsleySpider):
    name = 'projects_related'
    items_parselet = {
        "related_from": EXTRACTOR_MACHINE_NAME_COINTAINER,
        "to_block(id('block-pivots_block-0')//li/a)": [
            {
                "related_to": "@href"
            }
        ]
    }  # works with both parsers

    def parse_items(self, response):
        """ Assume the block always contains five items. todo: check

        @url https://drupal.org/project/views
        @returns items 5 5
        @returns requests 0 0
        """
        for item in self.apply_items_parselet(response, override_parser=ParserImplementations.REDAPPLE):
            item.extract('related_from', REGEXP_MACHINE_NAME, 1)
            item.extract('related_to', REGEXP_MACHINE_NAME, 1)
            yield item

# todo: inherit from scrapy.spider.Spider, not BaseSpider


class ReleasesProjectsRemoteParsleySpider(RemoteParsleySpider):
    name = 'projects_releases'  # todo: requires Git
    items_parselet = {
        "release_project_machine_name": EXTRACTOR_MACHINE_NAME_COINTAINER,
        "recommended(tr.release-update-status-0)": [
            {
                "release_quality": "'recommended'",
                "release_version_full": "a",
                "release_version_major": "a",
                "release_is_created_manually": "'True'",
                "release_zip_filesize_visible": "span",
                "release_date_visible": "td.views-field-file-timestamp",
                "release_notes_link": "td.views-field-view-node a @href"
            }
        ]
    }  # works with both parsers

    def parse_items(self, response):
        """
        Recommended VIEWS versions at the moment are 6 and 7
        Throws parslepy.base.NonMatchingNonOptionalKey: key "release_project_machine_name" is required but yield nothing
        in IMCE_WYSIWYG and IP_LIST

        @url https://drupal.org/project/views
        @returns items 2 2
        @returns requests 0 0
        """
        for item in self.apply_items_parselet(response, override_parser=ParserImplementations.REDAPPLE):
            item.extract('release_project_machine_name', REGEXP_MACHINE_NAME, 1)
            item.extract('release_version_major', '^(\\d)', 1)
            item.extract('release_zip_filesize_visible', '[^(].+[^)]', 0)
            item.extract('release_date_visible', '\\S+', 0)
            yield item


class ContributorsOtherRemoteParsleySpider(RemoteParsleySpider):
    name = 'other_contributors'
    items_parselet = {
        "contributor_name": "div.submitted a", # `Drupal on`  (getting unexpected suffix)
        "contributor_uid": EXTRACTOR_UID_COINTAINER
    }
    # 'spider_exceptions/NonMatchingNonOptionalKey': 2 (imce_wysiwyg, ip_list)
    # time: 3 minutes

    def parse_items(self, response):
        """
        @url https://drupal.org/project/views
        @returns items 2 2
        @returns requests 0 0
        """
        if response.url == "https://drupal.org/project/views":  # don't run on every page
            core_user_item = ParsletScrapyItem(self.items_parselet)
            core_user_item['contributor_name'] = 'Core projects'
            core_user_item['contributor_uid'] = 0
            yield core_user_item

        for item in self.apply_items_parselet(response, override_parser=ParserImplementations.REDAPPLE):
            item.extract('contributor_name', '^(.*?)( on)?$', 1)
            item.extract('contributor_uid', REGEXP_DIGITS_GROUP, 1)
            yield item


class ProjectsCategoriesRemoteParsleySpider(RemoteParsleySpider):
    name = 'projects_categories'
    items_parselet = {
        "categories_project_machine_name": EXTRACTOR_MACHINE_NAME_COINTAINER,
        "categories(span.terms a)": [
            {
                "categories_category_visible_name": "."
            }
        ]
    }

    def parse_items(self, response):
        """
        @url https://drupal.org/project/flag
        @returns items 100 100
        @returns requests 0 0
        """
        for item in self.apply_items_parselet(response, override_parser=ParserImplementations.REDAPPLE):
            item.extract('categories_project_machine_name', REGEXP_MACHINE_NAME, 1)
            item.extract('categories_category_visible_name', "^(.*?),?$", 1)  # todo: extract with xpath only
            yield item


class TopOtherRemoteParsleySpider(RemoteParsleySpider):
    name = "other_top"
    items_parselet = {
        "links(id('project-usage-all-projects')/tbody/tr)": [
            {
                "top_machine_name": "td:nth-of-type(2)",
                "top_place": "td:nth-of-type(1)",
                "top_category?": "not in the top"  # should be redefined in the pipeline
            }
        ]
    }

    def parse_start_url(self, response):
        """
        @url https://drupal.org/project/usage
        @returns items 12700 12700
        @returns requests 0 0
        """
        for item in self.apply_items_parselet(response, override_parser=ParserImplementations.REDAPPLE):
            item.extract('top_machine_name', REGEXP_MACHINE_NAME, 1)
            yield item
