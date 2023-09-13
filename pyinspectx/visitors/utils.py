import ast

# TODO: Add regex support for blacklist
# TODO: Blacklist all __ variables
# Variables need to be in global scope so they can be accessed inside static methods
BLACKLIST = ['__builtins__', '__doc__', '__file__', '__name__', '__package__']


class Utils():
    def __init__(self):
        pass

    @staticmethod
    def get_print_inject_code(nodeName='Program', inject_type='local'):
        """
        Get the AST node of the print statement that needs to be injected.
        
        Args:
            nodeName (str): The name of the node that is being injected.
            inject_type (str): The type of injection, can be 'local' or 'global'.
            
        Returns:
            ast.Module: The AST node of the print statement that needs to be injected.
        """
        
        if inject_type == 'local':
            inject_func = 'locals'
            print_str = '\nLocal Variables in scope {}:'.format(nodeName)
        else:
            inject_func = 'globals'
            print_str = '\nGlobal Variables in scope {}:'.format(nodeName)
            
        inject_node = ast.Module([
            ast.Assign(
                targets=[
                    ast.Name(id='local_vars', ctx=ast.Store())
                ],
                value=ast.Call(
                    func=ast.Attribute(
                        value=ast.Call(
                            func=ast.Name(id=inject_func, ctx=ast.Load()),
                            args=[],
                            keywords=[]
                        ),
                        attr='copy',
                        ctx=ast.Load()
                    ),
                    args=[],
                    keywords=[]
                )
            ),
            ast.Expr(
                ast.Call(
                    func=ast.Name(id='print', ctx=ast.Load()),
                    args=[
                        ast.Str(print_str),
                    ],
                    keywords=[]
                )
            ),
            ast.For(
                target=ast.Tuple(
                    elts=[
                        ast.Name(id='var_name', ctx=ast.Store()),
                        ast.Name(id='var_value', ctx=ast.Store())
                    ],
                    ctx=ast.Store()
                ),
                iter=ast.Call(
                    func=ast.Attribute(
                        value=ast.Name(id='local_vars', ctx=ast.Load()),
                        attr='items',
                        ctx=ast.Load()
                    ),
                    args=[],
                    keywords=[]
                ),
                body=[
                    ast.If(
                        test=ast.Compare(
                            left=ast.Name(id='var_name', ctx=ast.Load()),
                            ops=[ast.In()],
                            comparators=[
                                ast.List(
                                    elts=[ast.Constant(value=item) for item in BLACKLIST],
                                    ctx=ast.Load()
                                )
                            ]
                        ),
                        body=[
                            ast.Continue()
                        ],
                        orelse=[]
                    ),
                    ast.Expr(
                        ast.Call(
                            func=ast.Name(id='print', ctx=ast.Load()),
                            args=[
                                ast.BinOp(
                                    left=ast.Str('%s: %s'),
                                    op=ast.Mod(),
                                    right=ast.Tuple(
                                        elts=[
                                            ast.Name(id='var_name',
                                                     ctx=ast.Load()),
                                            ast.Name(id='var_value',
                                                     ctx=ast.Load())
                                        ],
                                        ctx=ast.Load()
                                    )
                                )
                            ],
                            keywords=[]
                        )
                    )
                ],
                orelse=[]
            )
        ])

        return inject_node
