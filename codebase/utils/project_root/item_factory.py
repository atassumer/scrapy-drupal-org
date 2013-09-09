from codebase.settings import C_SUPPORTED_MAJOR_VERSIONS, C_CONTRIBUTED_PROJECTS_ROOT, C_CORE_PROJECTS_ROOT
from codebase.utils.git import Git
from codebase.utils.project_root.item_class_factory import ModuleInfoItemClassFactory
from codebase.utils.project_root.project_root_parser import ProjectsRoot


class ItemFactory:
    attributes_constant = []  # should be overridden
    itemClassName = ""  # should be overridden

    def __init__(self, attributes_constant, projects_roots):
        self.attributes_constant = attributes_constant
        self.projects_roots = projects_roots
        self._createItemClass()

    def _createItemClass(self):
        if self.attributes_constant == [] or self.itemClassName == "":
            raise Exception("Item Factory fields should be overridden")
        item_class_factory = ModuleInfoItemClassFactory(self.itemClassName, self.attributes_constant)
        self.item_class = item_class_factory.getItemClass()
        self.supported_parameters = item_class_factory.getSupportedParameters()

    def _getModulesInfoFileObjects(self):
        for major_version in C_SUPPORTED_MAJOR_VERSIONS:
            Git().checkout_all_projects(major_version)
            for projects_root in self.projects_roots:
                is_core_project = projects_root == C_CORE_PROJECTS_ROOT
                projects = ProjectsRoot(projects_root, major_version, is_core_project)
                for obj in projects.getModuleInfoFileObjects():
                    yield obj

    def extractItems(self):
        raise NotImplementedError('ItemFactory.extractItems() should be implemented')


class StringsItemFactory(ItemFactory):
    """
    # >>> projects_roots = (C_CONTRIBUTED_PROJECTS_ROOT, C_CORE_PROJECTS_ROOTS)

    >>> projects_roots = (C_CORE_PROJECTS_ROOT, )
    >>> obj = StringsItemFactory(ModuleInfoItemClassFactory.DRUPAL_MODULES_VERSIONS_UNION, projects_roots)
    >>> len([x['description'] for x in obj.extractItems()]) > 50
    True
    """
    itemClassName = "ModuleDependencyItem"
    attributes_constant = ModuleInfoItemClassFactory.DRUPAL_MODULE_DEPENDENCY

    def extractItems(self):
        for info in self._getModulesInfoFileObjects():
            yield info.processStringParameters(self.item_class, self.supported_parameters)


class ListItemFactory(ItemFactory):
    itemClassName = "ModuleMetaItem"
    attributes_constant = ModuleInfoItemClassFactory.DRUPAL_MODULES_VERSIONS_INTERSECTION

    def extractItems(self):
        for info in self._getModulesInfoFileObjects():
            yield info.processListParameter(self.item_class, 'dependencies')
