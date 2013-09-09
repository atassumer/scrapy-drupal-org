from codebase.spiders.parsley.local import LocalParsleySpider
from codebase.utils.project_root.item_factory import StringsItemFactory, ListItemFactory
from codebase.utils.project_root.item_class_factory import ModuleInfoItemClassFactory
from codebase.settings import C_CONTRIBUTED_PROJECTS_ROOT, C_CORE_PROJECTS_ROOT


class ModulesLocalParsleySpider(LocalParsleySpider):
    """

    """
    allowed_domains = ["localhost"]
    start_urls = [
        "http://localhost/",
    ]

    # projects_roots = (C_CONTRIBUTED_PROJECTS_ROOT, C_CORE_PROJECTS_ROOT, )
    projects_roots = (C_CONTRIBUTED_PROJECTS_ROOT, )
    attributes_constant = ModuleInfoItemClassFactory.DRUPAL_MODULES_VERSIONS_UNION


class DependenciesModulesLocalParsleySpider(ModulesLocalParsleySpider):
    """

    """
    name = 'modules_dependencies'

    def collect_items_manually(self, response):
        self.log('collect_manually')
        obj = ListItemFactory(self.attributes_constant, self.projects_roots)
        for item in obj.extractItems():
            yield item


class MetaModulesLocalParsleySpider(ModulesLocalParsleySpider):
    """

    """
    name = 'modules_meta'

    def collect_items_manually(self, response):
        obj = StringsItemFactory(self.attributes_constant, self.projects_roots)
        return [item for item in obj.extractItems()]
