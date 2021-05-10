from __future__ import annotations
from typing import Union
from abc import ABC, abstractmethod
from lark import Lark, Transformer
from visitors import Visitor


class DumboElement(ABC):

    @abstractmethod
    def accept(self, visitor: Visitor) -> Union[str, bool, int, None]:
        pass


class ExpressionElement(DumboElement, ABC):
    pass


class IfElement(ExpressionElement):

    def __init__(self, boolean_expression: Union[BEElement, bool], expressions_list: ExpressionsListElement):
        self.boolean_expression = boolean_expression
        self.expressions_list = expressions_list

    def accept(self, visitor: Visitor) -> None:
        visitor.visit_if_element(self)


class ExpressionsListElement(ExpressionElement):

    def __init__(self, expressions_list: list[ExpressionElement]):
        self.expressions_list = expressions_list

    def accept(self, visitor: Visitor) -> None:
        visitor.visit_expressions_list_element(self)


class PrintElement(ExpressionElement):

    def __init__(self, str_expression: Union[SEElement, AEElement, BEElement, bool, int, str]):
        self.str_expression = str_expression

    def accept(self, visitor: Visitor) -> None:
        visitor.visit_print_element(self)


class ForElement(ExpressionElement):

    def __init__(self, iterator_var: VariableElement, iterator: Union[VariableElement, list[str]],
                 expressions_list: ExpressionsListElement):
        self.iterator_var = iterator_var
        self.iterator = iterator
        self.expressions_list = expressions_list

    def accept(self, visitor: Visitor) -> None:
        visitor.visit_for_element(self)


class SEElement(DumboElement):

    def __init__(self, sub_expressions: list[Union[str, AEElement, BEElement, SEElement]]):
        self.subExpressions = sub_expressions

    def accept(self, visitor: Visitor) -> str:
        return visitor.visit_se_element(self)


class AEElement(DumboElement):

    def __init__(self, left: Union[int, VariableElement, AEElement], op: str,
                 right: Union[int, VariableElement, AEElement]):
        self.left = left
        self.right = right
        self.op = op

    def accept(self, visitor: Visitor) -> int:
        return visitor.visit_ae_element(self)


class BEElement(DumboElement):

    def __init__(self, left: Union[BEElement, AEElement, bool], op: str,
                 right: Union[BEElement, AEElement, bool]):
        self.left = left
        self.right = right
        self.op = op

    def accept(self, visitor: Visitor) -> bool:
        return visitor.visit_be_element(self)


class AssignElement(ExpressionElement):

    def __init__(self, variable: VariableElement, value: Union[SEElement, AEElement, BEElement, list[str], int, str]):
        self.variable = variable
        self.value = value

    def accept(self, visitor: Visitor) -> None:
        visitor.visit_assign_element(self)


class VariableElement(DumboElement):

    def __init__(self, name: str):
        self.name = name

    def accept(self, visitor: Visitor) -> Union[int, str, bool, list[str]]:
        return visitor.visit_variable_element(self)


class ProgramElement(DumboElement):

    def __init__(self, content: list[Union[str, ExpressionsListElement]]):
        self.content = content

    def accept(self, visitor: Visitor) -> None:
        visitor.visit_program_element(self)


class DumboTransformer(Transformer):

    def program(self, items):
        return ProgramElement(items)

    def expressions_list(self, items):
        return ExpressionsListElement(items)

    def arithmetic_expression(self, items):
        items[1] = str(items[1])
        return AEElement(*items)

    def product(self, items):
        return self.arithmetic_expression(items)

    def boolean_expression(self, items):
        items[1] = str(items[1])
        return BEElement(*items)

    def string_expression(self, items):
        return SEElement(items)

    def print_statement(self, str_expression):
        return PrintElement(str_expression[0])

    def for_statement(self, items):
        return ForElement(*items)

    def if_statement(self, items):
        return IfElement(*items)

    def assign(self, pair):
        return AssignElement(*pair)

    def string_list(self, string_list):
        return string_list

    def string(self, string):
        return string[0][1:-1].replace('\\n', '\n').replace('\\t', '\t')

    def integer(self, integer):
        return int(integer[0])

    def variable(self, name):
        name = str(name[0])
        return VariableElement(name)

    def true(self, item):
        return True

    def false(self, item):
        return False

    def txt(self, text):
        return str(text[0])


primitives = [int, list, bool, str]

with open('grammar/dumbo.lark', 'r') as f:
    grammar = f.read()

dumbo_parser = Lark(grammar, parser='lalr', transformer=DumboTransformer(), start='program')
