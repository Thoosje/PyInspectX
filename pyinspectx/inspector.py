import ast, astor, subprocess
import os

from . import visitors

class Inspector():
    def __init__(self):
        self.parsed_code = None
        self.transformed_code = None
        
    def modify_code(self, code):
        """
        Modify the code by injecting the print statements.
        
        Args:
            code (str): The code that needs to be modified.
        """
        
        self.parsed_code = ast.parse(code)
        self.transformed_code = visitors.FunctionVisitor().visit(self.parsed_code)
        
    def get_modified_ast(self):
        """
        Injects one more print statement at the end of the code to print the global variables.
        Returns the modified ast.
        
        Returns:
            ast: The modified ast, cannot be run.
        """
        
        self.transformed_code.body.append(visitors.Utils.get_print_inject_code(nodeName='Program', inject_type='global'))
        return self.transformed_code
    
    def get_modified_code(self):
        """
        Get the readable modified code.
        
        Returns:
            str: The runnable modified code.
        """

        return astor.to_source(self.get_modified_ast())
    
    def run_modified_code(self):
        """
        Run the modified code in temp file (in working dir) and returns the output (Variables per scope).
        
        Returns:
            str: All the variables per scope.
        """
        
        script_directory = os.getcwd()
        script_path = os.path.join(script_directory, 'modified_code.temp.py')
        
        file = open(script_path, 'w', encoding='utf-8')
        file.write(self.get_modified_code())
        file.close()
        
        output = subprocess.check_output(['py', script_path], stderr=subprocess.STDOUT, universal_newlines=True)
        os.remove(script_path)
        
        return output