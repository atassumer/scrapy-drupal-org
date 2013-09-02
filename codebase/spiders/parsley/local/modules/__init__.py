from codebase.spiders.parsley.local import LocalParsleySpider


class ModulesLocalParsleySpider(LocalParsleySpider):
    """

    """


class DependenciesModulesLocalParsleySpider(ModulesLocalParsleySpider):
    """

    """
    name = 'modules_dependencies'


class MetaModulesLocalParsleySpider(ModulesLocalParsleySpider):
    """

    """
    name = 'modules_meta'