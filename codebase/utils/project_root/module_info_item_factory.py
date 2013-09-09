from codebase.settings import C_SUPPORTED_MAJOR_VERSIONS, C_CONTRIBUTED_PROJECTS_ROOT, C_CORE_PROJECTS_ROOTS
from codebase.utils.git import Git
from codebase.utils.project_root.item_class_factory import ModuleInfoItemClassFactory
from codebase.utils.project_root.project_root_parser import ProjectsRoot


class ItemFactory:
    attributes_constant = []  # should be overridden
    itemClassName = ""  # should be overridden

    def __init__(self, attributes_constant):
        self.attributes_constant = attributes_constant

    def _getItemClass(self):
        if self.attributes_constant == [] or self.itemClassName == "":
            raise Exception("Item Factory fields should be overridden")
        self.item_class_factory = ModuleInfoItemClassFactory(self.itemClassName, self.attributes_constant)
        self.item_class = self.item_class_factory.getItemClass()
        # self.supported_parameters = item_class_factory.getSupportedStringParameters()  # todo: move down

    def _getModulesInfoFileObjects(self):
        for major_version in C_SUPPORTED_MAJOR_VERSIONS:
            Git().checkout_all_projects(major_version)
            for projects_root in (C_CONTRIBUTED_PROJECTS_ROOT, C_CORE_PROJECTS_ROOTS):
                is_core_project = projects_root == C_CORE_PROJECTS_ROOTS
                projects = ProjectsRoot(projects_root, major_version, is_core_project)
                for obj in projects.getModuleInfoFileObjects():
                    yield obj

    def extractItems(self):
        raise NotImplementedError('ItemFactory.extractItems() should be implemented')


class StringsItemFactory(ItemFactory):
    """
    """
    itemClassName = "ModuleDependencyItem"
    attributes_constant = ModuleInfoItemClassFactory.DRUPAL_MODULE_DEPENDENCY

    def _getModulesInfoFileObjects(self):
        pass


class ListItemFactory(ItemFactory):
    itemClassName = "ModuleMetaItem"
    attributes_constant = ModuleInfoItemClassFactory.DRUPAL_MODULES_VERSIONS_INTERSECTION

    def _getModulesInfoFileObjects(self):
        pass
