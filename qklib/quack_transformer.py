from lark import Transformer
from quack_ast import (Add, Assign, Block, Call, Div, Equal, Float,
                       GreaterThan, GreaterThanOrEqual, If, Int, LessThan,
                       LessThanOrEqual, Mul, NotEqual, String, Sub, Var, While)


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
    
    def lt(self, items):
        left = items[0]
        right = items[1]
        return LessThan(left, right)
    
    def gt(self, items):
        left = items[0]
        right = items[1]
        return GreaterThan(left, right)
    
    def lte(self, items):
        left = items[0]
        right = items[1]
        return LessThanOrEqual(left, right)
    
    def gte(self, items):
        left = items[0]
        right = items[1]
        return GreaterThanOrEqual(left, right)
    
    def eq(self, items):
        left = items[0]
        right = items[1]
        return Equal(left, right)
    
    def neq(self, items):
        left = items[0]
        right = items[1]
        return NotEqual(left, right)
    
    def call(self,items):
        obj = items[0]
        method = str(items[1])
        args = items[2:]
        return Call(obj, method, args)
    
    def if_statement(self, items):
        condition = items[0]
        then_body = items[1]
        else_body = items[2] if len(items) > 2 else Block([])
        return If(condition, then_body, else_body)
    
    def while_statement(self, items):
        condition = items[0]
        body = items[1]
        return While(condition, body)
    
    def var(self, items):
        return Var(str(items[0]))
    
    def int(self, items):
        return Int(int(items[0]))
        
    def string(self, items):
        # 移除字符串周围的引号
        return String(str(items[0])[1:-1])
    
    def float(self, items):
        return Float(float(items[0]))
    
    def expr(self, items):
        return items[0]
    
    def block(self, items):
        return Block(items)
