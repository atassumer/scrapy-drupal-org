from drupalorg import settings
from drupalorg.utils.git import Git
from drupalorg.utils.project_root.module_info_item import ModuleInfoItem
from drupalorg.utils.project_root.project_root_parser import ProjectsRoot
from scrapy_parsley.utils.overrides_decorator import overrides, can_be_overridden


class ItemFactory:
    attributes_constant = -1  # should be overridden

    def __init__(self, projects_roots=False):
        if not projects_roots:
            projects_roots = (settings.PARSLEY_CONTRIBUTED_PROJECTS_ROOT,
                              settings.PARSLEY_CORE_PROJECTS_ROOT, )
        self.projects_roots = projects_roots
        self._createItemClass()

    def _createItemClass(self):
        if self.attributes_constant <= -1:
            raise Exception("Item Factory fields should be overridden")
        self.item = ModuleInfoItem(self.attributes_constant)
        self.supported_parameters = self.item.getSupportedParameters(self.attributes_constant)

    def _getModulesInfoFileObjects(self):
        for major_version in settings.PARSLEY_SUPPORTED_MAJOR_VERSIONS:
            Git().checkout_all_projects(major_version)
            for projects_root in self.projects_roots:
                is_core_project = projects_root == settings.PARSLEY_CORE_PROJECTS_ROOT
                projects = ProjectsRoot(projects_root, major_version, is_core_project)
                for obj in projects.getModuleInfoFileObjects():
                    yield obj

    def getItems(self):
        for info in self._getModulesInfoFileObjects():
            for item in self.getItemsFromInfoFileObject(info):
                yield item

    @can_be_overridden()
    def getItemsFromInfoFileObject(self, info):
        raise NotImplementedError('ItemFactory.extractItems() should be implemented')


class ModuleMetaItemFactory(ItemFactory):
    """
    >>> projects_roots = (settings.PARSLEY_CORE_PROJECTS_ROOT, )
    >>> obj = ModuleMetaItemFactory(projects_roots)
    >>> len([item['description'] for item in obj.getItems()]) > 50
    True
    """
    attributes_constant = ModuleInfoItem.DRUPAL_MODULES_VERSIONS_INTERSECTION

    @overrides(ItemFactory)
    def getItemsFromInfoFileObject(self, info):
        return info.processSingleParameters(self.item, self.supported_parameters)


class ModuleDependencyItemFactory(ItemFactory):
    """
    >>> projects_roots = (settings.PARSLEY_CORE_PROJECTS_ROOT, )
    >>> obj = ModuleDependencyItemFactory(projects_roots)
    >>> 'comment' in [item['dependencies'] for item in obj.getItems()]
    True
    """
    attributes_constant = ModuleInfoItem.DRUPAL_MODULE_DEPENDENCY

    @overrides(ItemFactory)
    def getItemsFromInfoFileObject(self, info):
        return info.processMultipleParameter(self.item, 'dependencies')
