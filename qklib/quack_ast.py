#AST节点类用于表示抽象语法树（AST)的结构。每个节点类对应一种语法结构。

class ASTNode:
    def gen_code(self, generator):
        raise NotImplementedError("gen_code not implemented in base class")

class Assign(ASTNode):
    # Assign表示赋值语句
    def __init__(self, var, vartype, expr):
        if isinstance(var, str):
            self.var = Var(var)  # Convert string to Var object if necessary
        else:
            self.var = var
        self.vartype = vartype
        self.expr = expr
    
    def __repr__(self):
        return f"Assign({self.var}, {self.vartype}, {self.expr})"
    
    def gen_code(self, generator):
        self.expr.gen_code(generator)
        var_index = generator.get_var_index(self.var.name)
        generator.code.append(f'store {var_index}')


class Add(ASTNode):
    def __init__(self, left, right):
        self.left = left
        self.right = right 
    
    def __repr__(self):
        return f"Add({self.left}, {self.right})"
    
    def gen_code(self, generator):
        self.left.gen_code(generator)
        self.right.gen_code(generator)
        generator.code.append('call Int: plus')

class Sub(ASTNode):
    def __init__(self, left, right):
        self.left = left
        self.right = right 
    
    def __repr__(self):
        return f"Sub({self.left}, {self.right})"
    
    def gen_code(self, generator):
        self.left.gen_code(generator)
        self.right.gen_code(generator)
        generator.code.append('call Int: minus')

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

class Var(ASTNode):
    #Var表示变量
    def __init__(self, name):
        self.name = name
    
    def __repr__(self):
        return f"Var({self.name})"
    
    def gen_code(self, generator):
        var_index = generator.get_var_index(self.name)
        generator.code.append(f'load {var_index}')

class Int(ASTNode):
    #Number表示整数常量
    def __init__(self, value):
        self.value = value
    
    def __repr__(self):
        return f"Int({self.value})"
    
    def gen_code(self, generator):
        generator.code.append(f'const {self.value}')

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


class FuncCall:
    def __init__(self, func_name, args):
        self.func_name = func_name
        self.args = args

    def __repr__(self):
        return f"FuncCall({self.func_name}, {self.args})"

class MethodCall:
    def __init__(self, obj, method_name, args):
        self.obj = obj
        self.method_name = method_name
        self.args = args

    def __repr__(self):
        return f"MethodCall({self.obj}, {self.method_name}, {self.args})"

class FuncDef:
    def __init__(self, name, params, return_type, body):
        self.name = name
        self.params = params 
        self.return_type = return_type
        self.body = body 
    
    def __repr__(self):
        return f"FuncDef({self.name}, {self.params}, {self.return_type}, {self.body})"

class Return:
    def __init__(self, expr):
        self.expr = expr 
    
    def __repr__(self):
        return f"Return({self.expr})"

class Block(ASTNode):
    def __init__(self, statements):
        self.statements = statements

    def __repr__(self):
        return f"Block({self.statements})"
    
    def gen_code(self, generator):
        for stmt in self.statements:
            stmt.gen_code(generator)

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

class Print:
    def __init__(self, expr):
        self.expr = expr

    def __repr__(self):
        return f"Print({self.expr})"

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