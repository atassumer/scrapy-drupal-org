import re
import string
import os

from scrapy_parsley.src.utils.file_system_adapter import FileSystemAdapter, Shell


class ProjectsRoot:
    """
    >>> path = '/home/ubuntu/Programs/drupal/files/git/drupal/modules'
    >>> obj = ProjectsRoot(path, 7, False)
    >>> files = obj.getModuleInfoFileObjects()
    >>> 'book' in [x.project for x in files]
    True
    """
    projects_root = ""
    major_version = ""
    is_core_project = None

    def __init__(self, projects_root, major_version, is_core_project):
        self.projects_root = projects_root
        self.major_version = major_version
        self.is_core_project = is_core_project

    def _getProjectObjects(self):
        fs = Shell()
        fs.chdir(self.projects_root)
        for project in fs.get_subdirectories_names():
            path = "%s/%s" % (self.projects_root, project)
            yield Project(project, path, self.major_version, self.is_core_project)

    def getModuleInfoFileObjects(self):
        for project in self._getProjectObjects():
            for info in project.getModuleInfoFileObjects():
                yield info


class Project:
    """
    >>> path = '/home/ubuntu/Programs/drupal/files/git/views/'
    >>> obj = Project('1225224', path, 7, False)
    >>> [x.module for x in obj.getModuleInfoFileObjects()]
    ['views', 'views_ui', 'views_export']
    """
    machine_name = ""
    path = ""
    major_version = ""
    is_core_project = None

    def __init__(self, machine_name, path, major_version, is_core_project):
        self.machine_name = machine_name
        self.path = path
        self.major_version = major_version
        self.is_core_project = is_core_project

    def getModuleInfoFileObjects(self):
        fs = FileSystemAdapter()
        fs.chdir(self.path)
        for filepath in fs.glob('*.info'):
            module = os.path.basename(filepath).split('.')[0]  # assume dot is not allowed for module filenames
            yield ModuleInfoFile(filepath, module, self.machine_name, self.major_version, self.is_core_project)


class ModuleInfoFile:
    """
    name = Iphone Push Notification through Easyapns
    description = "Provides a servive used to send Push Notifications using the device token."
    dependencies[] = content
    dependencies[] = content_profile
    package = Apple Push Notification Service Package

    version = "6.x-1.0"
    core = "6.x"
    project = "Easyapns"


    >>> from drupalorg.src.project_root.module_info_item import ModuleInfoItem
    >>> path = '/home/ubuntu/Programs/drupal/files/git/1225224/iphone_push_notification_through_easyapns.info'
    >>> obj = ModuleInfoFile(path, 'views_export', 'views', 7, False)
    >>> # meta
    >>> meta_constant = ModuleInfoItem.DRUPAL_MODULES_VERSIONS_UNION
    >>> item = ModuleInfoItem(meta_constant)
    >>> obj.processSingleParameters(item, ['name', 'description'])
    [{'description': 'Provides a servive used to send Push Notifications using the device token.',
     'is_core_project': False,
     'major_version': 7,
     'module': 'views_export',
     'name': 'Iphone Push Notification through Easyapns',
     'project': 'views'}]
    >>> # dependencies
    >>> meta_constant = ModuleInfoItem.DRUPAL_MODULE_DEPENDENCY
    >>> item = ModuleInfoItem(meta_constant)
    >>> [x['dependencies'] for x in obj.processMultipleParameter(item, 'dependencies')]
    ['content', 'content_profile']
    """
    path = ""
    module = ""
    project = ""
    major_version = ""
    is_core_project = ""

    supported_parameters = []

    def __init__(self, path, module, project, major_version, is_core_project):
        self.path = path
        self.module = module
        self.project = project
        self.major_version = major_version
        self.is_core_project = is_core_project

    def fillItemObject(self, item):
        item['module'] = self.module
        item['project'] = self.project
        item['major_version'] = self.major_version
        item['is_core_project'] = self.is_core_project  # todo: copy?
        return item

    def processSingleParameters(self, item, params):
        item = self.fillItemObject(item)
        for line in self._getFileAsLines():
            for param in params:
                occurrence = self.extractParameterFromLine(line, param)
                if occurrence:
                    item[param] = occurrence
        return [item]

    def processMultipleParameter(self, item, marker):
        for line in self._getFileAsLines():
            occurrence = self.extractParameterFromLine(line, marker)
            if occurrence:
                item = self.fillItemObject(item)
                item[marker] = occurrence
                yield item

    def _getFileAsLines(self):
        return open(self.path, 'r')

    def extractParameterFromLine(self, line, marker):
        return ModuleInfoFileLine(line, marker).getValue()


class ModuleInfoFileLine:
    """
    >>> name_line = 'name = Iphone Push Notification through Easyapns'
    >>> obj = ModuleInfoFileLine(name_line, 'name')  # simple case
    >>> obj.getValue()
    'Iphone Push Notification through Easyapns'
    >>> obj = ModuleInfoFileLine(name_line, 'NA')  # non-found case
    >>> obj.getValue()
    False
    >>> description_line = 'description = "Provides a servive used to send Push Notifications using the device token."'
    >>> obj = ModuleInfoFileLine(description_line, 'description')  # test double quotes
    >>> obj.getValue()
    'Provides a servive used to send Push Notifications using the device token.'
    >>> description_line = "description = 'Provides a servive used to send Push Notifications using the device token.'"
    >>> obj = ModuleInfoFileLine(description_line, 'description')  # test single quotes
    >>> obj.getValue()
    'Provides a servive used to send Push Notifications using the device token.'
    >>> dependencies_line = "dependencies[] = content_profile"
    >>> obj = ModuleInfoFileLine(dependencies_line, 'dependencies')  # test square brackets
    >>> obj.getValue()
    'content_profile'
    """

    def __init__(self, line, parameter_name):
        self.line = line
        self.parameter_name = parameter_name

    def getValue(self):
        if self.line[0:len(self.parameter_name)] == self.parameter_name and string.find(self.line, '=') != -1:
            value = re.search('=[\s\'"]*(.*?)[\s\'"]*$', self.line).group(1)
            return value if value != 'VERSION' else False
        return False
