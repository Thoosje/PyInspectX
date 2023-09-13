import ast, astor, subprocess
import os

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
    
    def run_modified_code(self):
        # TODO: Function uses a temp file to run the code. Check if this is cross platform compatible and the best way to do this.
        script_directory = os.getcwd()
        script_path = os.path.join(script_directory, 'modified_code.temp.py')
        
        file = open(script_path, 'w', encoding='utf-8')
        file.write(self.get_modified_code())
        file.close()
        
        output = subprocess.check_output(['py', script_path], stderr=subprocess.STDOUT, universal_newlines=True)
        os.remove(script_path)
        
        return output