from codebase.spiders.parsley.local import LocalParsleySpider
from codebase.utils.project_root.item_factory import ModuleMetaItemFactory, ModuleDependencyItemFactory
from codebase.shared.spiders.parsley_spider import ParsleySpider, overrides


class ModulesLocalParsleySpider(LocalParsleySpider):

    allowed_domains = ["localhost"]
    start_urls = [
        "http://localhost/",
    ]


class DependenciesModulesLocalParsleySpider(ModulesLocalParsleySpider):

    name = 'modules_dependencies'

    @overrides(ParsleySpider)
    def collect_items_manually(self, response):
        return (item for item in ModuleDependencyItemFactory().getItems())


class MetaModulesLocalParsleySpider(ModulesLocalParsleySpider):

    name = 'modules_meta'

    @overrides(ParsleySpider)
    def collect_items_manually(self, response):
        return (item for item in ModuleMetaItemFactory().getItems())
