import ast
from .utils import Utils

class Visitor(ast.NodeTransformer):
    def visit_FunctionDef(self, node):
        inject_node = Utils.get_print_inject_code(nodeName=node.name, inject_type='local')
        
        # Loop over all the subnodes of the function and see if one of them is a return function. If so, inject the code before the return statement.
        for i, subnode in enumerate(node.body):
            if isinstance(subnode, ast.Return):
                node.body.insert(i, inject_node)
                return node

        # If no return statement was found, just append the code to the end of the function.
        node.body = node.body + inject_node.body
        return node
