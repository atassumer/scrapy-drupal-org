from pyparsley import PyParsley
import json

from codebase.shared.items.load_item_objects import ParseletItemFactory
from codebase.shared.utils.json_like_structures import flatten_nested_structure


class Parselet():

    response = ""
    parselet_path = ""
    structure = ""

    def __init__(self, response, parselet_path):
        self.response = response
        self.parselet_path = parselet_path
        self.structure = self._apply_parselet(self.parselet_path, self.response.body)

    def _apply_parselet(self, parselet_path, body):
        parser = PyParsley(self._json_load(parselet_path))
        try:
            structure = parser.parse(string=body)
            return structure
        except RuntimeError:
            raise ParseletException('Xpath found nothing for this queries set')

    def _json_load(self, path):
        return json.load(open(path, 'r'))

    def _get_item_object(self, name):
        factory = ParseletItemFactory(name)
        return factory.get_object()


class ItemsParselet(Parselet):

    def collect(self, spider_name):
        for result in flatten_nested_structure(self.structure):
            item = self._get_item_object(spider_name)()
            for key, value in result.iteritems():
                item[key] = value
            yield item


class LinksParselet(Parselet):

    def collect(self):
        for dictionary in self.structure['links']:
            yield dictionary['link']


class ParseletException(Exception):
    pass