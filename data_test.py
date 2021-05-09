import unittest

from data import data_parser


class DataTest(unittest.TestCase):
    def test_data(self):
        src = """{{
             a := 42;
             b := 'Hello World!';
             c := true;
             d := false;
             e := ('Hello', 'World!');
        }}"""
        expected = {'a': 42, 'b': 'Hello World!', 'c': True, 'd': False,
                    'e': ['Hello', 'World!']}
        scope = data_parser.parse(src)
        self.assertEqual(scope, expected)


if __name__ == '__main__':
    unittest.main()
