import dumboParser as dp
from dumboParser import *
from visitors import Visitor
from collections import ChainMap


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


class Interpreter(Visitor):

    def __init__(self):
        self.scope = Scope()

    def visit_print_element(self, element: dp.PrintElement) -> None:
        pass

    def visit_for_element(self, element: dp.ForElement) -> None:
        pass

    def visit_se_element(self, element: dp.SEElement) -> str:
        pass

    def visit_ae_element(self, element: dp.AEElement) -> int:
        operations = {
            '+': lambda x, y: x + y,
            '-': lambda x, y: x - y,
            '*': lambda x, y: x * y,
            '/': lambda x, y: x / y
        }
        left = element.left
        right = element.right
        if type(left) is not int:
            left = left.accept(self)
        if type(right) is not int:
            right = right.accept(self)
        return operations[element.op](left, right)

    def visit_be_element(self, element: dp.BEElement) -> bool:
        operations = {
            'and': lambda x, y: x and y,
            'or': lambda x, y: x or y,
            '<': lambda x, y: x < y,
            '>': lambda x, y: x > y,
            '=': lambda x, y: x == y,
            '!=': lambda x, y: x != y
        }
        left = element.left
        right = element.right
        if type(left) is not bool:
            left = left.accept(self)
        if type(right) is not bool:
            right = right.accept(self)
        return operations[element.op](left, right)

    def visit_expressions_list_element(self, element: dp.ExpressionsListElement) -> None:
        self.scope = self.scope.new_child()
        for exp in element.expressions_list:
            exp.accept(self)
        self.scope = self.scope.parents

    def visit_assign_element(self, element: dp.AssignElement) -> None:
        pass

    def visit_program_element(self, element: dp.ProgramElement) -> None:
        for el in element.content:
            if type(el) is str:
                print(el)
            else:
                el.accept(self)

    def visit_variable_element(self, element: dp.VariableElement) -> Union[int, str, bool, list[str]]:
        if element.name in self.scope:
            return self.scope[element.name]
        raise ValueError

    def visit_if_element(self, element: dp.IfElement) -> None:
        if element.boolean_expression.accept(self):
            element.expressions_list.accept(self)


with open('dumbo.lark', 'r') as f:
    grammar = f.read()
dumbo_parser = Lark(grammar, parser='lalr', transformer=DumboTransformer(), start='program')

with open('exemples/template3.dumbo', 'r') as text_file:
    text = text_file.read()

dumbo_parser.parse(text)
