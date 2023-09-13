import ast
import astor

def get_locals_print_code(nodeName):
    print_code = ast.parse('''
        local_vars = locals()
        print("\\nLocal Variables in scope {}:")
        for var_name, var_value in local_vars.items():
            print("%s: %s" % (var_name, var_value))
        '''.format(nodeName)
    )
    
    return print_code

class Visitor(ast.NodeTransformer):
    def visit_FunctionDef(self, node):
        print(node)