from drupalorg.spiders.parsley.local import LocalParsleySpider
from drupalorg.utils.project_root.item_factory import ModuleMetaItemFactory, ModuleDependencyItemFactory
from scrapy_parsley.parsley_spider import ParsleyCrawlSpider, overrides


class ModulesLocalParsleySpider(LocalParsleySpider):
    allowed_domains = ["localhost"]
    start_urls = [
        "http://localhost/",
    ]


class DependenciesModulesLocalParsleySpider(ModulesLocalParsleySpider):
    name = 'modules_dependencies'

    @overrides(ParsleyCrawlSpider)
    def collect_items_manually(self, response):
        return ModuleDependencyItemFactory().getItems()


class MetaModulesLocalParsleySpider(ModulesLocalParsleySpider):
    name = 'modules_meta'

    @overrides(ParsleyCrawlSpider)
    def collect_items_manually(self, response):
        return ModuleMetaItemFactory().getItems()
