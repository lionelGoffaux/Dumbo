from __future__ import annotations
from typing import Union
import dumboParser as dp
from visitors import Visitor
from data import data_parser
from collections import ChainMap
import argh


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


class BadReferenceError(Exception):
    def __init__(self, variable_name=''):
        super().__init__(f"Variable '{variable_name}' used before assignment")


class NotIterableError(Exception):
    def __init__(self, variable_name=''):
        super().__init__(f"Variable '{variable_name}' is not iterable")


class Interpreter(Visitor):

    def __init__(self, scope, verbose=False):
        self.scope = Scope(scope)
        self.result = ''
        self.verbose = verbose
        self.replacements = {
            bool: lambda x: 'true' if x else 'false',
            list: lambda x: str(x).replace('[', '(').replace(']', ')'),
            int: lambda x: str(x),
            str: lambda x: x
        }

    def visit_print_element(self, element: dp.PrintElement) -> None:
        tmp = element.str_expression
        if type(element.str_expression) not in dp.primitives:
            tmp = element.str_expression.accept(self)
        result = self.replacements[type(tmp)](tmp)
        self.result += result
        if self.verbose:
            print(result, end='')

    def visit_for_element(self, element: dp.ForElement) -> None:
        if type(element.iterator) is dp.VariableElement:
            iterator = element.iterator.accept(self)
        else:
            iterator = element.iterator
        if type(iterator) is not list:
            raise NotIterableError(element.iterator.name)
        for string in iterator:
            self.scope[element.iterator_var.name] = string
            self.scope = self.scope.new_child()
            element.expressions_list.accept(self)
            self.scope = self.scope.parents

    def visit_se_element(self, element: dp.SEElement) -> str:
        res = ''
        for e in element.subExpressions:
            if type(e) not in dp.primitives:
                e = e.accept(self)
            res += self.replacements[type(e)](e)
        return res

    def visit_ae_element(self, element: dp.AEElement) -> int:
        operations = {
            '+': lambda x, y: x + y,
            '-': lambda x, y: x - y,
            '*': lambda x, y: x * y,
            '/': lambda x, y: x // y
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
        if type(left) not in [bool, int]:
            left = left.accept(self)
        if type(right) not in [bool, int]:
            right = right.accept(self)
        return operations[element.op](left, right)

    def visit_expressions_list_element(self, element: dp.ExpressionsListElement) -> None:
        for exp in element.expressions_list:
            exp.accept(self)

    def visit_assign_element(self, element: dp.AssignElement) -> None:
        if type(element.value) in dp.primitives:
            self.scope[element.variable.name] = element.value
        else:
            self.scope[element.variable.name] = element.value.accept(self)

    def visit_program_element(self, element: dp.ProgramElement) -> None:
        for el in element.content:
            if type(el) is str:
                self.result += el
                if self.verbose:
                    print(el, end='')
            else:
                el.accept(self)
        if self.verbose:
            print()

    def visit_variable_element(self, element: dp.VariableElement) -> Union[int, str, bool, list[str]]:
        if element.name in self.scope:
            return self.scope[element.name]
        raise BadReferenceError(element.name)

    def visit_if_element(self, element: dp.IfElement) -> None:
        condition = element.boolean_expression if type(element.boolean_expression) is bool \
            else element.boolean_expression.accept(self)

        if condition:
            self.scope = self.scope.new_child()
            element.expressions_list.accept(self)
            self.scope = self.scope.parents


def main(data_file_name, src_file_name):
    with open(data_file_name) as data_file:
        data = data_file.read()
    scope = data_parser.parse(data)
    with open(src_file_name) as src_file:
        src = src_file.read()
    program = dp.dumbo_parser.parse(src)
    interpreter = Interpreter(scope, verbose=True)
    program.accept(interpreter)


if __name__ == '__main__':
    argh.dispatch_command(main)
