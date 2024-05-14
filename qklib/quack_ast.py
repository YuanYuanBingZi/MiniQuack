#AST节点类用于表示抽象语法树（AST)的结构。每个节点类对应一种语法结构。
class Assign:
    # Assign表示赋值语句
    def __init__(self, var, vartype, expr):
        self.var = var
        self.vartype = vartype
        self.expr = expr
    
    def __repr__(self):
        return f"Assign({self.var}, {self.vartype}, {self.expr})"


class Add:
    def __init__(self, left, right):
        self.left = left
        self.right = right 
    
    def __repr__(self):
        return f"Add({self.left}, {self.right})"

class Sub:
    def __init__(self, left, right):
        self.left = left
        self.right = right 
    
    def __repr__(self):
        return f"Sub({self.left}, {self.right})"

class Mul:
    def __init__(self, left, right):
        self.left = left
        self.right = right 
    
    def __repr__(self):
        return f"Mul({self.left}, {self.right})"

class Div:
    def __init__(self, left, right):
        self.left = left
        self.right = right 
    
    def __repr__(self):
        return f"Div({self.left}, {self.right})"

class Var:
    #Var表示变量
    def __init__(self, name):
        self.name = name
    def __repr__(self):
        return f"Var({self.name})"

class Number:
    #Number表示整数常量
    def __init__(self, value):
        self.value = value
    
    def __repr__(self):
        return f"Number({self.value})"

class String:
    def __init__(self, value):
        self.value = value
    
    def __repr__(self):
        return f"String({self.value})"


class Call:
    def __init__(self, obj, method, args):
        self.obj = obj
        self.method = method
        self.args = args
    
    def __repr__(self):
        return f"Call({self.obj}, {self.method}, {self.args})"