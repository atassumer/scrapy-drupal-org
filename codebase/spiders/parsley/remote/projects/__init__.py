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
