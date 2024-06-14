from lark import Transformer
from quack_ast import (Add, And, Assign, Block, Boolean, Div, Equal, Float,
                       FuncCall, FuncDef, GreaterThan, GreaterThanOrEqual, If,
                       Int, LessThan, LessThanOrEqual, MethodCall, Mul, Not,
                       NotEqual, Or, Print, Return, String, Sub, Var, While)


#将parser生成的parse tree转换成AST
class QuackTransformer(Transformer):
    def __init__(self):
        self.symbols = {}

    def assignment(self, items):
        var = str(items[0])
        vartype = str(items[1])
        expr = items[2]
        self.symbols[var] = vartype
        return Assign(var, vartype, expr)
    
    def add(self, items):
        left = items[0]
        right =items[1]
        left_type = self.get_type(left)
        right_type = self.get_type(right)
        if left_type == right_type and left_type in ('Int', 'Float', 'String'):
            return Add(left, right)
        else:
            raise TypeError(f"Type mismatch in add operation: {left_type} and {right_type}")
    
    def sub(self, items):
        left = items[0]
        right =items[1]
        self.check_types(left, right, ('Int', 'Float'))
        return Sub(left, right)
    
    def mul(self, items):
        left = items[0]
        right =items[1]
        self.check_types(left, right, ('Int', 'Float'))
        return Mul(left, right)
    
    def div(self, items):
        left = items[0]
        right =items[1]
        self.check_types(left, right, ('Int', 'Float'))
        return Div(left, right)
    
    def and_op(self, items):
        left = items[0]
        right = items[1]
        self.check_types(left, right, ('Bool',))
        return And(left, right)
    
    def or_op(self, items):
        left = items[0]
        right = items[1]
        self.check_types(left, right, ('Bool',))
        return Or(left, right)
    
    def not_op(self, items):
        expr = items[0]
        expr_type = self.get_type(expr)
        if expr_type != 'Bool':
            raise TypeError(f"Type mismatch in not operation: expected Bool, got {expr_type}")
        return Not(expr)
    
    def check_types(self, left, right, expected_types):
        left_type = self.get_type(left)
        right_type = self.get_type(right)
        if left_type != right_type or left_type not in expected_types:
            raise TypeError(f"Type mismatch: expected {expected_types}, got{left_type} and {right_type}")
    
    def get_type(self, node):
        if isinstance(node, Var):
            return self.symbols.get(node.name, 'Unknown')
        elif isinstance(node, Int):
            return 'Int'
        elif isinstance(node, Float):
            return 'Float'
        elif isinstance(node, String):
            return 'String'
        elif isinstance(node, Boolean):
            return 'Bool'
        elif isinstance(node, FuncCall):
            return self.symbols.get(node.func_name, {}).get('return_type', 'Unknown')
        elif isinstance(node, MethodCall):
            return 'Obj'  # 暂时处理
        elif isinstance(node, (Add, Sub, Mul, Div)):
            left_type = self.get_type(node.left)
            right_type = self.get_type(node.right)
            if left_type == right_type:
                return left_type
            else:
                return 'Obj'
        elif isinstance(node, (And, Or, Not)):
            return 'Bool'
        elif isinstance(node, (LessThan, GreaterThan, LessThanOrEqual, GreaterThanOrEqual, Equal, NotEqual)):
            return 'Bool'
        else:
            return 'Unknown'

    def lt(self, items):
        left = items[0]
        right = items[1]
        self.check_types(left, right, ('Int', 'Float'))
        return LessThan(left, right)
    
    def gt(self, items):
        left = items[0]
        right = items[1]
        self.check_types(left, right, ('Int', 'Float'))
        return GreaterThan(left, right)
    
    def lte(self, items):
        left = items[0]
        right = items[1]
        self.check_types(left, right, ('Int', 'Float'))
        return LessThanOrEqual(left, right)
    
    def gte(self, items):
        left = items[0]
        right = items[1]
        self.check_types(left, right, ('Int', 'Float'))
        return GreaterThanOrEqual(left, right)
    
    def eq(self, items):
        left = items[0]
        right = items[1]
        self.check_types(left, right, ('Int', 'Float', 'String', 'Bool'))
        return Equal(left, right)
    
    def neq(self, items):
        left = items[0]
        right = items[1]
        self.check_types(left, right, ('Int', 'Float', 'String', 'Bool'))
        return NotEqual(left, right)
    
    def true(self, items):
        return Boolean(True)
    
    def false(self, items):
        return Boolean(False)
    
    def func_call(self, items):
        func_name = str(items[0])
        args = items[1:] 
        if func_name not in self.symbols:
            raise NameError(f"Function '{func_name}' is not defined")
        # 检查参数数量和类型
        func_info = self.symbols[func_name]
        if len(args) != len(func_info['params']):
            raise TypeError(f"Expected {len(func_info['params'])} arguments, got {len(args)}")
        for arg, param in zip(args, func_info['params']):
            self.check_types(arg, param[1], (param[1],))
        return FuncCall(func_name, args)
    
    def method_call(self, items):
        obj = items[0]
        method_name = str(items[1])
        args = items[2:]
        return MethodCall(obj, method_name, args)
    
    def if_statement(self, items):
        condition = items[0]
        if(self.get_type(condition) != 'Bool'):
            raise TypeError(f"The condition should be a Bool Type")
        then_body = items[1]
        else_body = items[2] if len(items) > 2 else Block([])
        return If(condition, then_body, else_body)
    
    def while_statement(self, items):
        condition = items[0]
        if(self.get_type(condition) != 'Bool'):
            raise TypeError(f"The condition should be a Bool Type")
        body = items[1]
        return While(condition, body)
    
    def var(self, items):
        var_name = str(items[0])
        if var_name not in self.symbols:
            raise NameError(f"Variable '{var_name}' is not defined")
        return Var(var_name)
    
    def int(self, items):
        return Int(int(items[0]))
        
    def string(self, items):
        # 移除字符串周围的引号
        return String(str(items[0])[1:-1])
    
    def float(self, items):
        return Float(float(items[0]))
    
    def expr(self, items):
        return items[0]
    
    def func_def(self, items):
        func_name = str(items[0])
        params = items[1:-2]
        return_type = str(items[-2])
        body = items[-1]
        self.symbols[func_name] = {'type': 'function', 'params': params, 'return_type': return_type}
        for param_name, param_type in params:
            self.symbols[param_name] = param_type
        return FuncDef(func_name, params, return_type, body)
    
    def param(self, items):
        param_name = str(items[0])
        param_type = str(items[1])
        return (param_name, param_type)
    
    def return_statement(self, items):
        expr = items[0]
        return Return(expr)
    
    def print_statement(self, items):
        expr = items[0]
        return Print(expr)

    def block(self, items):
        return Block(items)
    
    def statement(self, items):
        return items[0]
    
    def start(self, items):
        return Block(items) 
