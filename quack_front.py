"""Front end for Quack"""

from lark import Lark, Transformer
import argparse
import json
import sys

from typing import List,  Callable

import logging
logging.basicConfig()
log = logging.getLogger(__name__)
log.setLevel(logging.INFO)

def cli():
    cli_parser = argparse.ArgumentParser()
    cli_parser.add_argument("source", type=argparse.FileType("r"),
                            nargs="?", default=sys.stdin)
    args = cli_parser.parse_args()
    return args


quack_grammar = r"""
?start: program

?program: classes block
classes: clazz*

clazz: _class_sig  "{" methods block "}"
_class_sig: "class" name "("  formals ")" [ "extends" name ] 
methods: method*

formals: formal ("," formal)*
formal: name ":" name

?constructor: block

name: IDENT -> ident
block: BLAH*

method: "def" name "(" formals ")" returns "{" block "}"
returns: (":"  name)?

BLAH: "blah;"
IDENT: /[_a-zA-Z][_a-zA-Z0-9]*/

%import common.WS 
%ignore WS
"""

def cli():
    cli_parser = argparse.ArgumentParser()
    cli_parser.add_argument("source", type=argparse.FileType("r"),
                            nargs="?", default=sys.stdin)
    args = cli_parser.parse_args()
    return args

LB = "{"
RB = "}"

def ignore(node: "ASTNode", visit_state):
    log.debug(f"No visitor action at {node.__class__.__name__} node")
    return

def flatten(m: list):
    """Flatten nested lists into a single level of list"""
    flat = []
    for item in m:
        if isinstance(item, list):
            flat += flatten(item)
        else:
            flat.append(item)
    return flat


class ASTNode:
    """Abstract base class"""
    def __init__(self):
        self.children = []    # Internal nodes should set this to list of child nodes

    # Visitor-like functionality for walking over the AST. Define default methods in ASTNode
    # and specific overrides in node types in which the visitor should do something
    def walk(self, visit_state, pre_visit: Callable =ignore, post_visit: Callable=ignore):
        pre_visit(self, visit_state)
        for child in flatten(self.children):
            log.debug(f"Visiting ASTNode of class {child.__class__.__name__}")
            child.walk(visit_state, pre_visit, post_visit)
        post_visit(self, visit_state)

    # Example walk to gather method signatures
    def method_table_visit(self, visit_state: dict):
        ignore(self, visit_state)

    def r_eval(self) -> List[str]:
        """Evaluate for value"""
        raise NotImplementedError(f"r_eval not implemented for node type {self.__class__.__name__}")

    def c_eval(self, true_branch: str, false_branch: str) -> List[str]:
        raise NotImplementedError(f"c_eval not implemented for node type {self.__class__.__name__}")

    def json(self) -> str:
        return f"No json method defined for {self.__class__.__name__}"


class ProgramNode(ASTNode):
    def __init__(self, classes: List[ASTNode], main_block: ASTNode):
        self.classes = classes
        main_class = ClassNode("$Main", [], "Obj", [], main_block)
        self.classes.append(main_class)
        self.children = self.classes

    def __str__(self) -> str:
        return "\n".join([str(c) for c in self.classes])


class ClassNode(ASTNode):
    def __init__(self, name: str, formals: List[ASTNode],
                 super_class: str,
                 methods: List[ASTNode],
                 block: ASTNode):
        self.name = name
        self.super_class = super_class
        self.methods = methods
        self.constructor = MethodNode("$constructor", formals, name, block)
        self.children = methods +  [self.constructor]

    def __str__(self):
        formals_str = ", ".join([str(fm) for fm in self.constructor.formals])
        methods_str = "\n".join([f"{method}\n" for method in self.methods])
        return f"""
        class {self.name}({formals_str}){LB}
        /* methods go here */
        {methods_str}
        /* statements */
        {self.constructor}
        {RB}
        """

    # Example walk to gather method signatures
    def method_table_visit(self, visit_state: dict):
        """Create class entry in symbol table (as a preorder visit)"""
        if self.name in visit_state:
            raise Exception(f"Shadowing class {self.name} is not permitted")
        visit_state["current_class"] = self.name
        visit_state[self.name] = {
            "super": self.super_class,
            "fields": [],
            "methods": {}
        }



class MethodNode(ASTNode):
    def __init__(self, name: str, formals: List[ASTNode],
                 returns: str, body: ASTNode):
        self.name = name
        self.formals = formals
        self.returns = returns
        self.body = body
        self.children = [formals, body]

    def __str__(self):
        formals_str = ", ".join([str(fm) for fm in self.formals])
        return f"""
        /* method */ 
        def {self.name}({formals_str}): {self.returns} {LB}
        {self.body}
        {RB}
        """

    # Add this method to the symbol table
    def method_table_visit(self, visit_state: dict):
        clazz = visit_state["current_class"]
        if self.name in visit_state[clazz]["methods"]:
            raise Exception(f"Redeclaration of method {self.name} not permitted")
        params = [formal.var_type for formal in self.formals]
        visit_state[clazz]["methods"][self.name] = { "params": params, "ret": self.returns }


class FormalNode(ASTNode):
    def __init__(self, var_name: str, var_type: str):
        self.var_name = var_name
        self.var_type = var_type
        self.children = []

    def __str__(self):
        return f"{self.var_name}: {self.var_type}"

class BlockNode(ASTNode):
    def __init__(self, blahblah: str):
        self.blahblah = blahblah
        self.children = []

    def __str__(self):
        return f"{self.blahblah}"



class ASTBuilder(Transformer):
    """Translate Lark tree into my AST structure"""

    def program(self, e):
        log.debug("->program")
        classes, main_block = e
        return ProgramNode(classes, main_block)

    def classes(self, e):
        return e

    def clazz(self, e):
        log.debug("->clazz")
        name, formals, super, methods, constructor = e
        return ClassNode(name, formals, super, methods, constructor)

    def methods(self, e):
        return e

    def method(self, e):
        log.debug("->method")
        name, formals, returns, body = e
        return MethodNode(name, formals, returns, body)

    def returns(self, e):
        if not e:
            return "Nothing"
        return e

    def formals(self, e):
        return e

    def formal(self, e):
        log.debug("->formal")
        var_name, var_type = e
        return FormalNode(var_name, var_type)

    def ident(self, e):
        """A terminal symbol """
        log.debug("->ident")
        return e[0]

    def block(self, e) -> ASTNode:
        log.debug("->block")
        blahs = [str(id) for id in e]
        return BlockNode("\n".join(blahs))

def method_table_walk(node: ASTNode, visit_state: dict):
        node.method_table_visit(visit_state)

def main():
    args = cli()
    quack_parser = Lark(quack_grammar)
    text = "".join(args.source.readlines())
    tree = quack_parser.parse(text)
    # print(tree.pretty("   "))
    ast: ASTNode = ASTBuilder().transform(tree)
    print(ast)
    # Build symbol table, starting with the hard-coded json table
    # provided by Pranav.  We'll follow that structure for the rest
    builtins = open("lib/builtin_methods.json")
    symtab = json.load(builtins)
    ast.walk(symtab, method_table_walk)
    print(json.dumps(symtab,indent=4))


if __name__ == "__main__":
    main()








