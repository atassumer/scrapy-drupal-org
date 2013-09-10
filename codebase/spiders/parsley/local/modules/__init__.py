from codebase.spiders.parsley.local import LocalParsleySpider
from codebase.utils.project_root.item_factory import ModuleMetaItemFactory, ModuleDependencyItemFactory
from codebase.settings import C_CONTRIBUTED_PROJECTS_ROOT, C_CORE_PROJECTS_ROOT
from codebase.shared.spiders.parselet.parsley_spider import ParsleySpider, overrides


class ModulesLocalParsleySpider(LocalParsleySpider):
    """

    """
    allowed_domains = ["localhost"]
    start_urls = [
        "http://localhost/",
    ]

    projects_roots = (C_CONTRIBUTED_PROJECTS_ROOT, C_CORE_PROJECTS_ROOT, )


class DependenciesModulesLocalParsleySpider(ModulesLocalParsleySpider):

    name = 'modules_dependencies'

    @overrides(ParsleySpider)
    def collect_items_manually(self, response):
        return [item for item in ModuleDependencyItemFactory(self.projects_roots).getItems()]


class MetaModulesLocalParsleySpider(ModulesLocalParsleySpider):

    name = 'modules_meta'

    @overrides(ParsleySpider)
    def collect_items_manually(self, response):
        return [item for item in ModuleMetaItemFactory(self.projects_roots).getItems()]
