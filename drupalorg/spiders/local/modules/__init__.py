from drupalorg.spiders.local import LocalSpider
from drupalorg.utils.project_root.item_factory import ModuleMetaItemFactory, ModuleDependencyItemFactory


class ModulesLocalSpider(LocalSpider):
    allowed_domains = ["localhost"]
    start_urls = [
        "http://localhost/",
    ]


class DependenciesModulesLocalSpider(ModulesLocalSpider):
    name = 'modules_dependencies'

    def parse_start_url(self, response):
        return ModuleDependencyItemFactory().get_items()


class MetaModulesLocalSpider(ModulesLocalSpider):
    name = 'modules_meta'

    def parse_start_url(self, response):
        return ModuleMetaItemFactory().get_items()
