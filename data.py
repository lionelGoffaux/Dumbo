from lark import Transformer, Lark


class DataTransformer(Transformer):

    def __init__(self):
        self.scope = {}
        super().__init__()

    def program(self, items):
        return self.scope

    def assign(self, items):
        self.scope[items[0]] = items[1]
        return items

    def variable(self, items):
        return str(items[0])

    def string(self, items):
        return items[0][1:-1]

    def true(self, items):
        return True

    def false(self, items):
        return False

    def integer(self, items):
        return int(items[0])

    def string_list(self, items):
        return items


with open('grammar/dumbo_data.lark', 'r') as f:
    grammar = f.read()

data_parser = Lark(grammar, parser='lalr', transformer=DataTransformer(), start='program')
