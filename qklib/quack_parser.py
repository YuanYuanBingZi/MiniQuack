from lark import Lark
from quack_transformer import QuackTransformer

#read grammar from quack_grammer.txt
with open('quack_grammar.txt', 'r') as file:
        grammar = file.read()

# build the parser
parser = Lark(grammar, start='start', parser='lalr', transformer=QuackTransformer());

def test_parser():
    code = """
    a: Int = 13;
    b: Int = 7;
    c: Int = a + b;
    d: Int = c - 5;
    e: Int = c * 2;
    f: Int =  z / 3;
    g: Int = obj.method(a, b);
    h: String = "Why would you" + "do this?" - 3;
    i: Float = 3.14;
    j: Float = e * 2.0;
    k: Float = f / 3.0;
    """.strip()
    parse_tree = parser.parse(code)
    print(parse_tree.pretty())

test_parser()