from pyparsley import PyParsley
import json

from codebase.shared.items.item_factory import ItemFactory
from codebase.shared.utils.json_results import JsonResults


class Parselet():
    """
    Base class for ItemsParselet and LinksParselet
    """
    # todo: tests for each method
    response = ""
    parselet_path = ""
    json_results = ""

    def __init__(self, response, parselet_path):
        self.response = response
        self.parselet_path = parselet_path
        self.json_results = self._apply_parselet(self.parselet_path, self.response.body)

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
        factory = ItemFactory(name)
        return factory.get_object()


class ItemsParselet(Parselet):
    """
    Applies the parselet to the page. Returns scraped Item objects
    """
    def collect(self, spider_name):
        json_results = JsonResults(self.json_results)
        for result in json_results.getInCsvFormat():
            item = self._get_item_object(spider_name)()
            for key, value in result.iteritems():
                item[key] = value
            yield item


class LinksParselet(Parselet):
    """
    Applies the parselet to the page. Returns scraped links
    """
    def collect(self):
        for dictionary in self.json_results['links']:
            yield dictionary['link']


class ParseletException(Exception):
    pass