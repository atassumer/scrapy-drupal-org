

class JsonResults:
    """
    Convert results from JSON-like array to CSV-like array
    """
    def __init__(self, results_in_json):
        self.results_in_json = results_in_json

    def _separate_nodes_by_levels(self, dictionary):
        """
        >>> # simple format
        >>> two_level_dict = dict()
        >>> two_level_dict['key'] = 'value'
        >>> two_level_dict['string'] = 'string value'
        >>> two_level_dict['nested_item'] = [
        ...     {'nested_key': 'nested_value1', 'nk': 'nv2'},
        ...     {'nested_key': 'nested_value2', 'nk': 'nv2'}
        ... ]
        >>> obj = JsonResults(two_level_dict)
        >>> obj._separate_nodes_by_levels(two_level_dict)
        ({'string': 'string value', 'key': 'value'}, [[{'nested_key': 'nested_value1', 'nk': 'nv2'}, {'nested_key': 'nested_value2', 'nk': 'nv2'}]])
        """
        this_level_items = {}
        next_level_items = []
        for key, value in dictionary.iteritems():
            if type(value) is str:
                this_level_items[key] = value
            elif type(value) in (dict, list):
                next_level_items.append(value)
        return this_level_items, next_level_items

    def get_flattened_structure(self, structure):
        """JSON-like structure to CSV-like structure
        Only one nested level supported at the moment
        Assumes that keys are unique in the file scope

        >>> obj = JsonResults(None)
        >>> # one level
        >>>
        >>> structure = {
        ...     'from': '/project/views',
        ...     'to': '/project/followup'
        ... }
        >>> list(obj.get_flattened_structure(structure))
        [{'to': '/project/followup', 'from': '/project/views'}]

        >>> # two levels
        >>> structure = {
        ... 'from': '/project/views',
        ... 'to_block': [{'to': '/project/panels_everywhere'},
        ...               {'to': '/project/panels'},
        ...               {'to': '/project/calendar'},
        ...               {'to': '/project/views_cloud'},
        ...               {'to': '/project/followup'}]}
        >>> flattened = list(obj.get_flattened_structure(structure))
        >>> len(flattened)
        5
        >>> flattened[0]
        {'to': '/project/panels_everywhere', 'from': '/project/views'}
        """
        if type(structure) not in (dict, list):
            raise JsonLikeStructuresException('unexpected input')
        this_level_items, next_level_items = self._separate_nodes_by_levels(structure)
        if next_level_items:
            for nl_items in next_level_items:
                for nl_item in nl_items:
                    # yields one item per loop iteration
                    yield dict(this_level_items.items() + nl_item.items())
        else:
            yield this_level_items

    def getInCsvFormat(self):
        return self.get_flattened_structure(self.results_in_json)


class JsonLikeStructuresException(Exception):
    pass
