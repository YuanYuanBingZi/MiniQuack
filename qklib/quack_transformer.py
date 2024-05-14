from lark import Transformer
from quack_ast import (Add, Assign, Call, Div, Float, Mul, Number, String, Sub,
                       Var)


#将parser生成的parse tree转换成AST
class QuackTransformer(Transformer):
    def assignment(self, items):
        var = str(items[0])
        vartype = str(items[1])
        expr = items[2]
        return Assign(var, vartype, expr)
    
    def add(self, items):
        left = items[0]
        right =items[1]
        return Add(left, right)
    
    def sub(self, items):
        left = items[0]
        right =items[1]
        return Sub(left, right)
    
    def mul(self, items):
        left = items[0]
        right =items[1]
        return Mul(left, right)
    
    def div(self, items):
        left = items[0]
        right =items[1]
        return Div(left, right)
    
    def call(self,items):
        obj = items[0]
        method = str(items[1])
        args = items[2:]
        return Call(obj, method, args)
    
    def var(self, items):
        return Var(str(items[0]))
    
    def number(self, items):
        value = str(items[0])
        if '.' in value:
            return Float(float(value))
        else:
            return Number(int(value))
    
    def string(self, items):
        # 移除字符串周围的引号
        return String(str(items[0])[1:-1])
    
    def float(self, items):
        return Float(float(items[0]))
    
    def expr(self, items):
        return items[0]
