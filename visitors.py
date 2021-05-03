from __future__ import annotations
from typing import Union
import dumboParser as dp
from abc import ABC, abstractmethod


class Visitor(ABC):

    @abstractmethod
    def visit_if_element(self, element: dp.IfElement) -> None:
        pass

    @abstractmethod
    def visit_print_element(self, element: dp.PrintElement) -> None:
        pass

    @abstractmethod
    def visit_for_element(self, element: dp.ForElement) -> None:
        pass

    @abstractmethod
    def visit_se_element(self, element: dp.SEElement) -> str:
        pass

    @abstractmethod
    def visit_ae_element(self, element: dp.AEElement) -> int:
        pass

    @abstractmethod
    def visit_be_element(self, element: dp.BEElement) -> bool:
        pass

    @abstractmethod
    def visit_expressions_list_element(self, element: dp.ExpressionsListElement) -> None:
        pass

    @abstractmethod
    def visit_assign_element(self, element: dp.AssignElement) -> None:
        pass

    @abstractmethod
    def visit_program_element(self, element: dp.ProgramElement) -> None:
        pass

    '''@abstractmethod
    def visit_txt_element(self, element: dp.TXTElement):
        pass'''

    @abstractmethod
    def visit_variable_element(self, element: dp.VariableElement) -> Union[int, str, bool, list[str]]:
        pass
