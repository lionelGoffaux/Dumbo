from dumboParser import *

with open('dumbo.lark', 'r') as f:
    grammar = f.read()
dumbo_parser = Lark(grammar, parser='lalr', transformer=DumboTransformer(), start='program')

with open('exemples/template3.dumbo', 'r') as text_file:
    text = text_file.read()

dumbo_parser.parse(text)
