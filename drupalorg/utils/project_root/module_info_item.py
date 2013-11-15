from scrapy.exceptions import CloseSpider

from scrapy_parsley.scrapy_parsley2.parsley_item import ScrapyItemListWrapper


class ModuleInfoItem(ScrapyItemListWrapper):
    """
    >>> ModuleInfoItem(ModuleInfoItem.DRUPAL_MODULES_VERSIONS_UNION)
    {}
    """
    DRUPAL_MODULES_VERSION_6 = 6
    DRUPAL_MODULES_VERSION_7 = 7
    DRUPAL_MODULES_VERSIONS_INTERSECTION = 0
    DRUPAL_MODULES_VERSIONS_UNION = 1
    DRUPAL_THEMES = 10
    DRUPAL_MODULE_DEPENDENCY = 20

    supported_parameters = {
        # `package` and `dependencies` are excluded
        # https://drupal.org/node/171205
        'themes': {'name', 'description', 'screenshot', 'version', 'core', 'engine', 'base_theme',
                   'regions', 'features', 'theme_settings', 'stylesheets', 'scripts', 'php'},
        # sets string literal
        # https://drupal.org/node/231036
        'modules_6': {'name', 'description', 'core', 'php', 'hidden', 'version', 'project'},
        # https://drupal.org/node/542202
        'modules_7': {'name', 'description', 'core', 'stylesheets', 'scripts', 'files',
                      'package', 'php', 'version', 'configure', 'required', 'hidden', 'project'},
        #
        'dependencies': {'dependencies'},
        # file meta data
        'meta': {'module', 'project', 'major_version', 'is_core_project'},
    }  # todo: does the dataset contains custom other parameters?
    # supported_list_parameters = ['dependencies']
    attributes_constant = None

    def __init__(self, attributes_constant):
        keys = self.getSupportedParameters(attributes_constant)
        super(ModuleInfoItem, self).__init__(keys)

    def getSupportedParameters(self, attributes_constant):
        """
        >>> constant = ModuleInfoItem.DRUPAL_MODULES_VERSIONS_UNION
        >>> obj = ModuleInfoItem(constant)
        >>> list(obj.getSupportedParameters(constant))[:5]
        ['core', 'description', 'major_version', 'module', 'is_core_project']
        """
        if attributes_constant == self.DRUPAL_MODULES_VERSION_6:
            params = self.supported_parameters['modules_6']
        elif attributes_constant == self.DRUPAL_MODULES_VERSION_7:
            params = self.supported_parameters['modules_7']
        elif attributes_constant == self.DRUPAL_THEMES:
            params = self.supported_parameters['themes']
        elif attributes_constant == self.DRUPAL_MODULES_VERSIONS_UNION:
            params = self.supported_parameters['modules_6'] & self.supported_parameters['modules_7']  # union
        elif attributes_constant == self.DRUPAL_MODULES_VERSIONS_INTERSECTION:
            params = self.supported_parameters['modules_6'] | self.supported_parameters['modules_7']  # intersection
        elif attributes_constant == self.DRUPAL_MODULE_DEPENDENCY:
            params = self.supported_parameters['dependencies']
        else:
            raise IncorrectAttributeConstant('Attribute constant %s is not correct' % self.attributes_constant)
        return params | self.supported_parameters['meta']


class IncorrectAttributeConstant(CloseSpider):
    """
    >>> ModuleInfoItem(6)
    {}
    >>> ModuleInfoItem('something weird')
    Traceback (most recent call last):
        ...
    IncorrectAttributeConstant: Attribute constant None is not correct
    """