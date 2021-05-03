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

    def __init__(self, iterator_var: str, iterator: Union[str, list[str]],
                 expressions_list: ExpressionsListElement):
        self.iterator_var = iterator_var
        self.iterator = iterator
        self.expressions_list = expressions_list

    def accept(self, visitor: Visitor) -> None:
        visitor.visit_for_element(self)


class SEElement(DumboElement):

    def __init__(self, left: Union[str, AEElement, BEElement, SEElement],
                 right: Union[str, AEElement, BEElement, SEElement]):
        self.left = left
        self.right = right

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

    def __init__(self, op: str, boolean_expression: Union[list[BEElement], list[AEElement], bool]):
        self.boolean_expression = boolean_expression
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
        print('program', items)
        return items

    def expressions_list(self, items):
        print('expressions_list', items)
        return items

    def arithmetic_expression(self, items):
        print('arithmetic_expression', items)
        return items

    def boolean_expression(self, items):
        print('boolean_expression', items)
        return items

    def string_expression(self, items):
        print('string_expression', items)
        return items

    def print_statement(self, str_expression):
        print('print', str_expression)
        return str_expression
        return PrintElement(str_expression)

    def for_statement(self, items):
        print('for', items)
        return items

    def if_statement(self, items):
        print('if', items)
        return items

    def assign(self, pair):
        print('assign', pair)
        return pair

    def string_list(self, string_list):
        print('str list', string_list)
        return string_list

    def true(self, item):
        print('true', item)
        return item

    def false(self, item):
        print('false', item)
        return item

    def MULL_OP(self, mull_op):
        print(mull_op)
        return mull_op

    def LOG_OP(self, log_op):
        print(log_op)
        return log_op

    def COMP_OP(self, comp):
        print(comp)
        return comp

    def ADD_OP(self, add):
        print('Add', add)
        return add

    def STRING(self, string):
        print('string', string)
        return string

    def INT(self, item):
        print('item', item)
        return item

    def VARIABLE(self, name):
        print('variable', name)
        return name

    def TXT(self, text):
        print('Txt', text)
        return text
