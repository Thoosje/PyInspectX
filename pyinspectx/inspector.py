import ast, astor
from . import visitors

class Inspector():
    def __init__(self):
        self.parsed_code = None
        self.transformed_code = None
        
    def modify_code(self, code):
        self.parsed_code = ast.parse(code)
        self.transformed_code = visitors.FunctionVisitor().visit(self.parsed_code)
        
    def get_modified_code(self):
        self.transformed_code.body.append(visitors.Utils.get_print_inject_code(nodeName='Program', inject_type='global'))
        return astor.to_source(self.transformed_code)
    