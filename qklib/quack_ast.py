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

class Int:
    #Number表示整数常量
    def __init__(self, value):
        self.value = value
    
    def __repr__(self):
        return f"Int({self.value})"

class String:
    def __init__(self, value):
        self.value = value
    
    def __repr__(self):
        return f"String({self.value})"

class Float:
    def __init__(self, value):
        self.value = value
    
    def __repr__(self):
        return f"Float({self.value})"

class Boolean:
    def __init__(self, value):
        self.value = value
    
    def __repr__(self):
        return f"Boolean({self.value})"


class Call:
    def __init__(self, obj, method, args):
        self.obj = obj
        self.method = method
        self.args = args
    
    def __repr__(self):
        return f"Call({self.obj}, {self.method}, {self.args})"

class Block:
    def __init__(self, statements):
        self.statements = statements

    def __repr__(self):
        return f"Block({self.statements})"

class If:
    def __init__(self, condition, then_body, else_body):
        self.condition = condition
        self.then_body = then_body
        self.else_body = else_body
    
    def __repr__(self):
        return f"If({self.condition}, {self.then_body}, {self.else_body})"

class While:
    def __init__(self, condition, body):
        self.condition = condition
        self.body = body
    
    def __repr__(self):
        return f"While({self.condition}, {self.body})"

class LessThan:
    def __init__(self, left, right):
        self.left = left
        self.right = right 
    
    def __repr__(self):
        return f"LessThan({self.left}, {self.right})"

class GreaterThan:
    def __init__(self, left, right):
        self.left = left
        self.right = right 
    
    def __repr__(self):
        return f"GreaterThan({self.left}, {self.right})"

class LessThanOrEqual:
    def __init__(self, left, right):
        self.left = left
        self.right = right 
    
    def __repr__(self):
        return f"LessThanOrEqual({self.left}, {self.right})"

class GreaterThanOrEqual:
    def __init__(self, left, right):
        self.left = left
        self.right = right 
    
    def __repr__(self):
        return f"GreaterThanOrEqual({self.left}, {self.right})"

class Equal:
    def __init__(self, left, right):
        self.left = left
        self.right = right 
    
    def __repr__(self):
        return f"Equal({self.left}, {self.right})"


class NotEqual:
    def __init__(self, left, right):
        self.left = left
        self.right = right 
    
    def __repr__(self):
        return f"NotEqual({self.left}, {self.right})"

class And:
    def __init__(self, left, right):
        self.left = left
        self.right = right

    def __repr__(self):
        return f"And({self.left}, {self.right})"

class Or:
    def __init__(self, left, right):
        self.left = left
        self.right = right

    def __repr__(self):
        return f"Or({self.left}, {self.right})"

class Not:
    def __init__(self, expr):
        self.expr = expr

    def __repr__(self):
        return f"Not({self.expr})"