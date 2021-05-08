import unittest
import dumboParser as dp


class DumboParserTest(unittest.TestCase):

    def test_program(self) -> None:
        src = "<test>{{ print 'Hello World!'; }}</test>"
        program = dp.dumbo_parser.parse(src)
        self.assertIs(type(program), dp.ProgramElement)
        self.assertIs(type(program.content), list)
        self.assertEquals(len(program.content), 3)

    def test_txt(self) -> None:
        src = "<test>Hello World!</test>"
        program = dp.dumbo_parser.parse(src)
        self.assertIs(type(program.content[0]), str)

    def test_expressionList(self) -> None:
        src = "{{print 'Hello World!';}}"
        program = dp.dumbo_parser.parse(src)
        expr_list = program.content[0]
        self.assertIs(type(expr_list), dp.ExpressionsListElement)
        self.assertIs(type(expr_list.expressions_list), list)
        self.assertEquals(len(expr_list.expressions_list), 1)

    def test_printElement(self) -> None:
        src_list = ["{{print 'Hello World!';}}", "{{print 4;}}", "{{print true;}}", "{{print var;}}",
                    "{{print 12 + 5;}}", "{{print true or false;}}", "{{print 'Hello' . 'World';}}"]
        for src in src_list:
            program = dp.dumbo_parser.parse(src)
            print_element = program.content[0].expressions_list[0]
            self.assertIs(type(print_element), dp.PrintElement)
            self.assertIn(type(print_element.str_expression), dp.primitives + [dp.SEElement, dp.AEElement,
                                                                               dp.BEElement, dp.VariableElement])

    def test_variableElement(self) -> None:
        src = "{{print var;}}"
        program = dp.dumbo_parser.parse(src)
        var_element = program.content[0].expressions_list[0].str_expression
        self.assertIs(type(var_element), dp.VariableElement)
        self.assertEquals(var_element.name, "var")

    def test_assignElement(self) -> None:
        src_list = ["{{var := 42;}}", "{{var := True;}}", "{{var := 'Hello World!';}}", "{{var := 42 + 8;}}",
                    "{{var := true or false;}}", "{{var := var;}}", "{{var := 'Hello' . 'World';}}",
                    "{{var := ('Hello', 'World');}}"]

        for src in src_list:
            program = dp.dumbo_parser.parse(src)
            assign = program.content[0].expressions_list[0]
            self.assertIs(type(assign), dp.AssignElement)
            self.assertIs(type(assign.variable), dp.VariableElement)
            self.assertIn(type(assign.value), dp.primitives + [dp.SEElement, dp.AEElement,
                                                               dp.BEElement, dp.VariableElement])

    def test_ifElement(self) -> None:
        src_list = ["{{if true do print i; endif;}}",
                    "{{if true and true  do print i; endif;}}"]
        for src in src_list:
            program = dp.dumbo_parser.parse(src)
            if_element = program.content[0].expressions_list[0]
            self.assertIs(type(if_element), dp.IfElement)
            self.assertIn(type(if_element.boolean_expression), [dp.VariableElement, dp.BEElement, bool])
            self.assertIs(type(if_element.expressions_list), dp.ExpressionsListElement)

    def test_forElement(self) -> None:
        src = "{{for i in list do print i; endfor;}}"
        program = dp.dumbo_parser.parse(src)
        for_element = program.content[0].expressions_list[0]
        self.assertIs(type(for_element), dp.ForElement)
        self.assertIs(type(for_element.iterator_var), dp.VariableElement)
        self.assertIs(type(for_element.iterator), dp.VariableElement)
        self.assertIs(type(for_element.expressions_list), dp.ExpressionsListElement)

        src = "{{for i in ('Hello', 'World!') do print i; endfor;}}"
        program = dp.dumbo_parser.parse(src)
        for_element = program.content[0].expressions_list[0]
        self.assertIs(type(for_element.iterator), list)

    def test_booleanExpressionElement(self) -> None:
        src = "{{print true or false and 42 < 42 or 42 > 42 and 42 = 42 and 42 != 42;}}"
        program = dp.dumbo_parser.parse(src)
        bool_exp_element = program.content[0].expressions_list[0].str_expression
        self.assertIs(type(bool_exp_element), dp.BEElement)

    def test_arithmeticExpressionElement(self) -> None:
        src = "{{print 45 - 16 * (7 / 23);}}"
        program = dp.dumbo_parser.parse(src)
        arithmetic_exp_element = program.content[0].expressions_list[0].str_expression
        self.assertIs(type(arithmetic_exp_element), dp.AEElement)

    def test_stringExpressionElement(self) -> None:
        src = "{{print 'hello'.'world'.true.42;}}"
        program = dp.dumbo_parser.parse(src)
        string_exp_element = program.content[0].expressions_list[0].str_expression
        self.assertIs(type(string_exp_element), dp.SEElement)

    def test_intElement(self) -> None:
        src = "{{print 42;}}"
        program = dp.dumbo_parser.parse(src)
        int_element = program.content[0].expressions_list[0].str_expression
        self.assertIs(type(int_element), int)

    def test_strElement(self) -> None:
        src = "{{print 'Hello World!';}}"
        program = dp.dumbo_parser.parse(src)
        str_element = program.content[0].expressions_list[0].str_expression
        self.assertIs(type(str_element), str)

    def test_boolElement(self) -> None:
        src = "{{print true;}}"
        program = dp.dumbo_parser.parse(src)
        bool_element = program.content[0].expressions_list[0].str_expression
        self.assertIs(type(bool_element), bool)

    def test_listElement(self) -> None:
        src = "{{var := ('Hello', 'World!');}}"
        program = dp.dumbo_parser.parse(src)
        list_element = program.content[0].expressions_list[0].value
        self.assertIs(type(list_element), list)

    def test_example(self) -> None:
        with open('test.dumbo') as src_file:
            src = src_file.read()

        program = dp.dumbo_parser.parse(src)
        self.assertIs(type(program), dp.ProgramElement)
        self.assertEquals(len(program.content), 11)
        for element in program.content[0:11:2]:
            self.assertIs(type(element), str)
        for element in program.content[1:11:2]:
            self.assertIs(type(element), dp.ExpressionsListElement)

        for block in program.content[1:4:2] + program.content[7:10:2]:
            self.assertEquals(len(block.expressions_list), 1)
            self.assertIs(type(block.expressions_list[0]), dp.PrintElement)

        main_block = program.content[5]
        self.assertEquals(len(main_block.expressions_list), 2)
        self.assertIs(type(main_block.expressions_list[0]), dp.AssignElement)

        for_element = main_block.expressions_list[1]
        self.assertIs(type(for_element), dp.ForElement)
        self.assertIs(type(for_element.iterator_var), dp.VariableElement)
        self.assertIs(type(for_element.iterator), dp.VariableElement)

        for_instructions = for_element.expressions_list.expressions_list
        self.assertEquals(len(for_instructions), 3)
        self.assertIs(type(for_instructions[0]), dp.IfElement)
        self.assertEquals(len(for_instructions[0].expressions_list.expressions_list), 1)
        self.assertIs(type(for_instructions[0].expressions_list.expressions_list[0]), dp.PrintElement)
        self.assertIs(type(for_instructions[1]), dp.PrintElement)
        self.assertIs(type(for_instructions[2]), dp.AssignElement)


if __name__ == '__main__':
    unittest.main()
