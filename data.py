from collections import ChainMap
from lark import Transformer, Lark


class Scope(ChainMap):
    """Variant of ChainMap that allows direct updates to inner scopes
    source : https://docs.python.org/3/library/collections.html#collections.ChainMap"""

    def __setitem__(self, key, value):
        for mapping in self.maps:
            if key in mapping:
                mapping[key] = value
                return
        self.maps[0][key] = value

    def __delitem__(self, key):
        for mapping in self.maps:
            if key in mapping:
                del mapping[key]
                return
        raise KeyError(key)


class DataTransformer(Transformer):

    def __init__(self):
        self.scope = Scope()
        super().__init__()

    def program(self, items):
        return self.scope

    def assign(self, items):
        # print(items[0])
        self.scope[items[0]] = items[1]
        return items

    def variable(self, items):
        return items[0]

    def string(self, items):
        # print(items[0])
        return items[0][1:-1]

    def true(self, items):
        return True

    def false(self, items):
        return False

    def integer(self, items):
        return int(items[0])

    def string_list(self, items):
        return items


with open('dumbo_data.lark', 'r') as f:
    grammar = f.read()

data_parser = Lark(grammar, parser='lalr', transformer=DataTransformer(), start='program')
