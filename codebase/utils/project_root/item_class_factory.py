from scrapy.item import Field, Item


class ModuleInfoItemClassFactory:
    """
    >>> obj = ModuleInfoItemClassFactory(
    ...     'TestModuleInfoItemClassFactoryItem', ModuleInfoItemClassFactory.DRUPAL_MODULES_VERSIONS_UNION)
    >>> list(obj.getSupportedStringParameters())[0:10]
    ['core', 'description', 'major_version', 'module', 'is_core_project', 'project', 'version', 'hidden', 'php', 'name']
    >>> item_object = obj.getItemClass()
    >>> item_object
    <class 'scrapy.item.TestModuleInfoItemClassFactoryItem'>
    >>> item_object()
    {}
    >>> item_object().description
    Traceback (most recent call last):
        ...
    AttributeError: Use item['description'] to get field value
    >>> item_object().NA
    Traceback (most recent call last):
        ...
    AttributeError: NA
    """
    DRUPAL_MODULES_VERSION_6 = 6
    DRUPAL_MODULES_VERSION_7 = 7
    DRUPAL_MODULES_VERSIONS_INTERSECTION = 0
    DRUPAL_MODULES_VERSIONS_UNION = 1  # todo: find a better name
    DRUPAL_THEMES = 10
    DRUPAL_MODULE_DEPENDENCY = 20

    supported_string_parameters = {  # todo: does the dataset contains any other parameters?
        # `package` and `dependencies` are excluded
        # https://drupal.org/node/171205
        'themes': {'name', 'description', 'screenshot', 'version', 'core', 'engine', 'base_theme',
                   'regions', 'features', 'theme_settings', 'stylesheets', 'scripts', 'php'},  # sets string literal
        # https://drupal.org/node/231036
        'modules_6': {'name', 'description', 'core', 'php', 'hidden', 'version', 'project'},
        # https://drupal.org/node/542202
        'modules_7': {'name', 'description', 'core', 'stylesheets', 'scripts', 'files',
                      'package', 'php', 'version', 'configure', 'required', 'hidden', 'project'},
        #
        'dependencies': {'dependencies'},
        # file meta data
        'meta': {'module', 'project', 'major_version', 'is_core_project'},
    }
    # supported_list_parameters = ['dependencies']
    attributes_constant = None

    def __init__(self, item_class_name, attributes_constant):
        self.item_class_name = item_class_name
        self.attributes_constant = attributes_constant

    def getItemClass(self):  # todo: this method copied from parselet_item_factory. Should I make shared class?
        third_param = dict()
        for attr in self.getSupportedStringParameters():
            third_param[attr] = Field()
        item = type(self.item_class_name, (Item, ), third_param)
        return item

    def getSupportedStringParameters(self):
        if self.attributes_constant == self.DRUPAL_MODULES_VERSION_6:
            params = self.supported_string_parameters['modules_6']
        elif self.attributes_constant == self.DRUPAL_MODULES_VERSION_7:
            params = self.supported_string_parameters['modules_7']
        elif self.attributes_constant == self.DRUPAL_THEMES:
            params = self.supported_string_parameters['themes']
        elif self.attributes_constant == self.DRUPAL_MODULES_VERSIONS_UNION:
            params = self.supported_string_parameters['modules_6'] & self.supported_string_parameters['modules_7']  # union
        elif self.attributes_constant == self.DRUPAL_MODULES_VERSIONS_INTERSECTION:
            params = self.supported_string_parameters['modules_6'] | self.supported_string_parameters['modules_7']  # intersection
        elif self.attributes_constant == self.DRUPAL_MODULE_DEPENDENCY:
            params = self.supported_string_parameters['dependencies']
        else:
            raise ModuleInfoItemClassFactoryException('Attribute constant %s is not correct' % self.attributes_constant)
        return params | self.supported_string_parameters['meta']


class ModuleInfoItemClassFactoryException(Exception):
    pass