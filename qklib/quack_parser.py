from lark import Lark
from quack_transformer import QuackTransformer
from quack_code_generator import QuackCodeGenerator
#read grammar from quack_grammer.txt
with open('qklib/quack_grammar.txt', 'r') as file:
        grammar = file.read()

# build the parser
parser = Lark(grammar, start='start', parser='lalr', transformer=QuackTransformer());

# strip()
def parse_code(code):
    return parser.parse(code)

if __name__ == "__main__":
    import sys 
    code = open(sys.argv[1]).read()
    tree = parse_code(code)
    #print(f'AST Tree: {tree}\n')
    codegen = QuackCodeGenerator()
    codegen.generate(tree)
    print(f'Code Generation: \n{codegen.get_code()}')
    
