from drupalorg.spiders.local import LocalSpider
from drupalorg.utils.project_root.item_factory import ModuleMetaItemFactory, ModuleDependencyItemFactory
from scrapy_parsley.scrapy_parsley2.parsley_spider import ParsleyCrawlSpider
from scrapy_parsley.scrapy_parsley2.overrides_decorator import overrides


class ModulesLocalSpider(LocalSpider):
    allowed_domains = ["localhost"]
    start_urls = [
        "http://localhost/",
    ]


class DependenciesModulesLocalSpider(ModulesLocalSpider):
    name = 'modules_dependencies'

    @overrides(ParsleyCrawlSpider)
    def parse_start_url(self, response):
        return ModuleDependencyItemFactory().getItems()


class MetaModulesLocalSpider(ModulesLocalSpider):
    name = 'modules_meta'

    @overrides(ParsleyCrawlSpider)
    def parse_start_url(self, response):
        return ModuleMetaItemFactory().getItems()
