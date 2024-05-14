from lark import Lark, Transformer, v_args

#read grammar from quack_grammer.txt
with open('quack_grammar.txt', 'r') as file:
        grammar = file.read()

# build the parser
parser = Lark(grammar, start='start', parser='lalr');

def test_parser():
    code = """
    y: Int = 13;
    x: Int = 7;
    z: Int = x + y;
    w: Int = z - 5;
    """.strip()
    parse_tree = parser.parse(code)
    print(parse_tree.pretty())

test_parser()