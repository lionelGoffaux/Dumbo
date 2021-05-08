import unittest

from data import Scope
from dumboParser import dumbo_parser
from dumbo import Interpreter, BadReferenceError, NotIterableError


class InterpreterTest(unittest.TestCase):

    def setUp(self) -> None:
        self.interpreter = Interpreter(Scope(), verbose=False)

    def assertExecutionResult(self, src, expected):
        program = dumbo_parser.parse(src)
        program.accept(self.interpreter)
        self.assertEquals(self.interpreter.result, expected)

    def test_textBlock(self) -> None:
        src = "text block"
        self.assertExecutionResult(src, src)

    def test_print_str(self) -> None:
        src = "text{{print ' ok ';}}text"
        expected = 'text ok text'
        self.assertExecutionResult(src, expected)

    def test_print_int(self) -> None:
        src = "{{print 42;}}"
        expected = '42'
        self.assertExecutionResult(src, expected)

    def test_print_bool(self) -> None:
        src = "{{print true;}}"
        expected = 'true'
        self.assertExecutionResult(src, expected)

    def test_variable(self) -> None:
        src = """{{
                 a := 42;
                 b := 'Hello World!';
                 c := true;
                 d := false;
                 e := ('Hello', 'World!');
                 print a;
                 print b;
                 print c;
                 print d;
                 print e;
                 }}"""
        expected = "42Hello World!truefalse('Hello', 'World!')"
        self.assertExecutionResult(src, expected)

    def test_arithmetic(self) -> None:
        src = "{{a:=7; print ((42 + 8)/a - 2) * 2 ;}}"
        expected = '10'
        self.assertExecutionResult(src, expected)

    def test_boolean(self) -> None:
        src = "{{print true and false or 1 < 2 and 2 > 1 and 42 = 42;}}"
        expected = 'true'
        self.assertExecutionResult(src, expected)

    def test_strExpression(self) -> None:
        src = "{{print 'Hello '.'World!';}}"
        expected = 'Hello World!'
        self.assertExecutionResult(src, expected)

    def test_if(self) -> None:
        src = """{{if true do print 'ok'; endif;
                   if false do print ' ko'; endif;
                 }}"""
        expected = 'ok'
        self.assertExecutionResult(src, expected)

    def test_for(self) -> None:
        src = """{{list := ('Hello', 'World!');
                   for i in ('Hello', 'World!') do 
                       print i;
                   endfor;
                   for i in list do 
                       print i;
                   endfor;
                 }}"""
        expected = 'HelloWorld!HelloWorld!'
        self.assertExecutionResult(src, expected)

    def test_ifScope(self) -> None:
        src = "{{if true do a := 42; endif; print a;}}"
        program = dumbo_parser.parse(src)
        with self.assertRaises(BadReferenceError):
            program.accept(self.interpreter)

    def test_forScope(self) -> None:
        src = "{{for i in ('Hello', 'World!') do a := 42; endfor; print a;}}"
        program = dumbo_parser.parse(src)
        with self.assertRaises(BadReferenceError):
            program.accept(self.interpreter)

    def test_forVarScope(self) -> None:
        src = "{{for i in ('Hello', 'World!') do a := 42; endfor; print i;}}"
        expected = 'World!'
        self.assertExecutionResult(src, expected)

    def test_badRefError(self) -> None:
        src = "{{print a;}}"
        program = dumbo_parser.parse(src)
        with self.assertRaises(BadReferenceError):
            program.accept(self.interpreter)

    def test_notIterError(self) -> None:
        src = "{{list := 42; for i in list do print 'ok'; endfor;}}"
        program = dumbo_parser.parse(src)
        with self.assertRaises(NotIterableError):
            program.accept(self.interpreter)


if __name__ == '__main__':
    unittest.main()
