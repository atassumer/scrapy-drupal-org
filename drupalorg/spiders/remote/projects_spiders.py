from drupalorg.spiders.remote import RemoteParsleySpider


class ProjectsRemoteParsleySpider(RemoteParsleySpider):
    """
    
    """


class ContributedProjectsRemoteParsleySpider(ProjectsRemoteParsleySpider):
    """

    """
    name = 'projects_contributed'
    parselet = {
        "url": "ul.primary li:nth-of-type(1) a @href",
        "machine_name": "regexp:match(ul.primary li:nth-of-type(1) a @href, '[^/]+$')",
        "visible_name": "#page-subtitle",
        "uid": "regexp:match(.submitted a @href, '\\d+')",
        "nid": "regexp:match(id('block-project-development')//ul/li[contains(.,'commits')]/a/@href, '\\d+')",
        "image_urls?": "a.imagecache @href",
        "info(.project-info)": [
            {
                "info_to": "ul"
            }
        ],
        "issues(.issue-cockpit-categories)?": [
            {
                "issues_open_count": "regexp:match(.issue-cockpit-totals a:nth-of-type(1), '\\d+')",
                "issues_total_count": "regexp:match(.issue-cockpit-totals a:nth-of-type(2), '\\d+')",
                "bugreports_open_count": "regexp:match(.issue-cockpit-bug a:nth-of-type(1), '\\d+')",
                "bugreports_total_count": "regexp:match(.issue-cockpit-bug a:nth-of-type(2), '\\d+')"
            }
        ]
    }


class LinkedProjectsRemoteParsleySpider(ProjectsRemoteParsleySpider):
    """

    """
    name = 'projects_linked'
    parselet = {
        "from?": "ul.primary li:nth-of-type(1) a @href",
        "to_links(//div[@class='node-content']//a)": [
            {
                "to?": "regexp:match(@href, '/project/[^\\/?]+$')"
            }
        ]
    }


class RelatedProjectsRemoteParsleySpider(ProjectsRemoteParsleySpider):
    """

    """
    name = 'projects_related'
    parselet = {
        "from": "ul.primary li:nth-of-type(1) a @href",
        "to_block(id('block-pivots_block-0')//li/a)": [
            {
                "to": "@href"
            }
        ]
    }


class ReleasesProjectsRemoteParsleySpider(ProjectsRemoteParsleySpider):
    """

    """
    name = 'projects_releases'
    parselet = {
        "project_machine_name": "regexp:match(ul.primary li:nth-of-type(1) a @href, '[^/]+$')",
        "releases_recommended(.download-table-ok tr)": [
            {
                "quality": "str:tokenize('recommended', '-')",
                "version_full": "a",
                "version_major": "regexp:match(a, '^\\d')",
                "is_created_manually": "str:tokenize('True', '-')",
                "zip_filesize_visible": "regexp:match(span, '[^(].+[^)]')",
                "date_visible": "regexp:match(td.views-field-file-timestamp, '\\S+')",
                "notes_link": "td.views-field-view-node a @href"
            }
        ]
    }
