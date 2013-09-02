from codebase.spiders.parsley.remote import RemoteParsleySpider


class ProjectsRemoteParsleySpider(RemoteParsleySpider):
    """
    
    """


class ContributedProjectsRemoteParsleySpider(ProjectsRemoteParsleySpider):
    """

    """
    name = 'projects_contributed'


class LinkedProjectsRemoteParsleySpider(ProjectsRemoteParsleySpider):
    """

    """
    name = 'projects_linked'


class RelatedProjectsRemoteParsleySpider(ProjectsRemoteParsleySpider):
    """

    """
    name = 'projects_related'


class ReleasesProjectsRemoteParsleySpider(ProjectsRemoteParsleySpider):
    """

    """
    name = 'projects_releases'

# {
#     "url": "ul.primary li:nth-of-type(1) a @href",
#     "machine_name": "regexp:match(ul.primary li:nth-of-type(1) a @href, '[^/]+$')",
#     "visible_name": "id('page-subtitle')/text()",
#     "uid": "//div[@class='submitted']/a/@href",
#     "nid": "id('block-project-development')//ul/li[contains(.,'commits')]/a/@href",
#     "image_urls": "id('content')//a[img and contains(@href, 'files/images/')]/@href",
#     "info(.project-info ul)": [{
#           "to": "@href"
#         }],
#     "issues(.issue-cockpit-categories a)": [{
#           "to": "@href"
#         }]
# }