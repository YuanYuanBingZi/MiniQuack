from quack_ast import Add, Assign, Block, FuncDef, Int, Return, Sub, Var


class QuackCodeGenerator:
    def __init__(self):
        self.code = []
        self.var_mapping = {}
        self.var_counter = 0
    
    def generate(self, node):
        if isinstance(node, list):
            for item in node:
                item.gen_code(self)
        else:
            node.gen_code(self)
    
    def generate_error(self, node):
        raise Exception(f'No generator found for{type(node).__name__}')
    
    def get_var_index(self, var_name):
        if var_name not in self.var_mapping:
            self.var_mapping[var_name] = self.var_counter
            self.var_counter += 1
        return self.var_mapping[var_name]

    

   
    
    def gen_funcDef(self,node):
        self.code.append(f'.method{node.name}')
        if node.params:
            self.code.append(f'.args {", ".join(param[0] for param in node.params)}')
        self.code.append('enter')
        self.generate(node.body)
        self.code.appebd(f'return {1 if node.return_type != "void" else 0}\n')

    def gen_block(self, node):
        for stmt in node.statements:
            self.generate(stmt)
    
    def gen_return(self, node):
        self.generate(node.expr)
        self.code.append('return 1')
    
    def gen_if(self, node):
        self.generate(node.condition)  
        label_else = self.new_label()  
        label_end = self.new_label() 
        self.code.append(f' jump_ifnot {label_else}')  
        self.generate(node.then_body) 
        self.code.append(f'jump {label_end}')  
        self.code.append(f'{label_else}:') 
        if node.else_body:
            self.generate(node.else_body)  
        self.code.append(f'{label_end}:') 
    
    def new_label(self):
        label = f'label_{self.label_counter}'
        self.label_counter += 1
        return label
    
    def get_code(self):
        self.code.insert(0, f'alloc {len(self.var_mapping)}')
        return '\n'.join(self.code)
