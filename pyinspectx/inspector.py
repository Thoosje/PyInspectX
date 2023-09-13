import ast
import visitors

class Inspector():
    def __init__(self):
        self.parsed_code = None
        self.transformed_code = None
        
    def modify_code(self, code):
        self.parsed_code = ast.parse(code)
        self.transformed_code = visitors.VariablePrinter().visit(self.parsed_code)