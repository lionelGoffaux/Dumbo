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

    def __init__(self, subExpressions: list[Union[str, AEElement, BEElement, SEElement]]):
        self.subExpressions = subExpressions

    def accept(self, visitor: Visitor) -> str:
        return visitor.visit_se_element(self)


class AEElement(DumboElement):

    def __init__(self, op: 'str', left: Union[int, VariableElement, AEElement],
                 right: Union[int, VariableElement, AEElement]):
        self.left = left
        self.right = right
        self.op = op

    def accept(self, visitor: Visitor) -> int:
        return visitor.visit_ae_element(self)


class BEElement(DumboElement):

    def __init__(self, op: str, left: Union[BEElement, AEElement, bool],
                 right: Union[BEElement, AEElement, bool]):
        self.left = left
        self.right = right
        self.op = op

    def accept(self, visitor: Visitor) -> bool:
        return visitor.visit_be_element(self)


class AssignElement(ExpressionElement):

    def __init__(self, variable: str, value: Union[SEElement, list[str]]):
        self.variable = variable
        self.value = value

    def accept(self, visitor: Visitor) -> None:
        visitor.visit_assign_element(self)


class VariableElement(DumboElement):

    def __init__(self, name: str):
        self.name = name

    def accept(self, visitor: Visitor) -> Union[int, str, bool, list[str]]:
        return visitor.visit_variable_element(self)


'''class TXTElement(DumboElement):
    def __init__(self, text: str):
        self.text = text

    def accept(self, visitor: Visitor) -> None:
        visitor.visit_txt_element(self)'''


class ProgramElement(DumboElement):

    def __init__(self, content: list[Union[str, ExpressionsListElement]]):
        self.content = content

    def accept(self, visitor: Visitor) -> None:
        visitor.visit_program_element(self)


class DumboTransformer(Transformer):

    def program(self, items):
        program = ProgramElement(items)
        #print('program', program)
        return program

    def expressions_list(self, items):
        expression_list = ExpressionsListElement(items)
        #print('expressions_list', expression_list)
        return expression_list

    def arithmetic_expression(self, items):
        arithmetic_expression = AEElement(str(items[1]), items[0], items[2])
        #print('arithmetic_expression', arithmetic_expression)
        return arithmetic_expression

    def boolean_expression(self, items):
        print('boolean_expression', items)
        return items

    def string_expression(self, items):
        string_expression = SEElement(items)
        #print('string_expression', string_expression)
        return string_expression

    def print_statement(self, str_expression):
        print_statement = PrintElement(str_expression)
        #print('print', print_statement)
        return print_statement

    def for_statement(self, items):
        for_state = ForElement(*items)
        #print('for', for_state)
        return for_state

    def if_statement(self, items):
        if_state = IfElement(*items)
        #print('if', if_state)
        return if_state

    def assign(self, pair):
        assignation = AssignElement(*pair)
        #print('assign', assignation)
        return pair

    def string_list(self, string_list):
        #print('str list', string_list)
        return string_list

    def string(self, string):
        string = string[0][1:-1]
        #print('string', string)
        return string

    def integer(self, integer):
        integer = int(integer[0])
        #print('integer', integer)
        return int(integer)

    def variable(self, name):
        name = name[0]
        variable = VariableElement(name)
        #print('variable', variable)
        return variable

    def true(self, item):
        item = bool(item)
        #print('bool', item)
        return item

    def false(self, item):
        item =bool(item)
        #print('bool', item)
        return item

    def txt(self, text):
        text = str(text[0])
        #print('Txt', text)
        return text
