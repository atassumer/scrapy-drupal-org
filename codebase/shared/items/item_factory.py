from scrapy.item import Item, Field
import json

from codebase.shared.utils.file_system_adapter import FileSystemAdapter


class ItemFactory():
    """
    Class for creation of Scrapy's Item object out of given parselet json file
    """
    spider_name = None
    root_path = None

    fs = None

    def __init__(self, spider_name, root_path='spiders/parsley'):
        """
        >>> factory = ItemFactory('tests_yelp', 'tests/yelp')
        >>> obj = factory.get_object()
        >>> obj
        <class 'scrapy.item.TestsYelpItem'>
        >>> obj()
        {}
        >>> # obj.phone  # todo
        """
        self.fs = FileSystemAdapter()
        self.spider_name = spider_name
        self.root_path = self.fs.get_full_path(root_path)

    def get_object(self):
        """
        # >>> load_item_object('tests_yelp', 'tests/yelp')
        # <class 'scrapy.item.TestsYelpItem'>
        """
        let_file_path = self.fs.glob("%s.items.json" % self.spider_name).next()
        content = json.loads(open(let_file_path).read())
        attributes = self._extract_attributes(content)
        return self._create_item_object(attributes)

    def _create_item_object(self, attributes):
        """
        # >>> obj = _create_item_object('tests_yelp', ['first', 'second', 'third'])
        # >>> obj
        # <class 'scrapy.item.TestsYelpItem'>
        # >>> instance = obj()
        # >>> instance
        # {}
        # >>> instance['first'] = 'something'
        # >>> instance
        # {'first': 'something'}
        """
        class_name = "%sItem" % "".join(map(str.capitalize, self.spider_name.split('_')))
        third_param = dict()
        for attr in attributes:
            third_param[attr] = Field()
        item = type(class_name, (Item, ), third_param)
        return item

    def _extract_attributes(self, let_file):
        """
        # >>> let_file = {
        # ... "name": "h1",
        # ... "phone": "#bizPhone",
        # ... "address": "address",
        # ... "reviews(.review)": [
        # ...    {
        # ...        "date": ".date",
        # ...        "user_name": ".user-name a",
        # ...        "comment": "with-newlines(.review_comment)"
        # ...    }
        # ... ]
        # ... }
        # >>> list(factory._extract_attributes(let_file))
        # ['phone', 'date', 'comment', 'user_name', 'name', 'address']
        """
        for key, value in let_file.iteritems():
            if type(value) is list:
                if type(value[0]) is not dict:
                    raise ParsleyItemFactoryException(type(value))
                for key in self._extract_attributes(value[0]):
                    yield self._clean_attribute(key)
            elif type(value) in (unicode, str):
                yield self._clean_attribute(key)

    def _clean_attribute(self, attribute):
        """
        >>> obj = ItemFactory('parsley_item_factory_test')
        >>> obj._clean_attribute('optional_key?')
        'optional_key'
        >>> obj._clean_attribute('mandatory_key')
        'mandatory_key'
        """
        if attribute[-1:] == '?':
            return attribute[:-1]
        else:
            return attribute


class ParsleyItemFactoryException(Exception):
    pass