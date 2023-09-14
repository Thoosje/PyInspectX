import ast
import random

# TODO: Add regex support for blacklist
# TODO: Blacklist all __ variables
# Variables need to be in global scope so they can be accessed inside static methods
BLACKLIST = [
    "__builtins__",
    "__doc__",
    "__file__",
    "__name__",
    "__package__",
    "__loader__",
    "__spec__",
    "__annotations__",
    "__cached__",
]


class Utils:
    def __init__(self):
        pass

    @staticmethod
    def get_storage_node():
        """
        Creates the AST node where the variables will be stored.

        Returns:
            ast.Module: The AST node where the variables will be stored.
            str: The name of the dictionary where the variables will be stored.
        """
        
        storage_dict_name = "inspect_storage_%s" % random.randint(1000, 10000000)
        BLACKLIST.append(storage_dict_name)

        storage_node = ast.Module(
            [
                ast.Assign(
                    targets=[ast.Name(id=storage_dict_name, ctx=ast.Store())],
                    value=ast.Dict(keys=[], values=[]),
                )
            ]
        )

        return (storage_node, storage_dict_name)

    @staticmethod
    def get_print_storage_node(storage_dict_name):
        """
        Creates the AST node that logs the storage in JSON format.

        Returns:
            ast.Module: The print storage node
        """

        print_node = ast.Module(
            [
                ast.Expr(value=ast.Import(names=[ast.alias(name="json", asname=None)])),
                ast.Expr(
                    value=ast.Call(
                        func=ast.Name(id="print", ctx=ast.Load()),
                        args=[
                            ast.Call(
                                func=ast.Attribute(
                                    value=ast.Name(id="json", ctx=ast.Load()),
                                    attr="dumps",
                                    ctx=ast.Load(),
                                ),
                                args=[ast.Name(id=storage_dict_name, ctx=ast.Load())],
                                keywords=[],
                            )
                        ],
                        keywords=[],
                    )
                ),
            ]
        )

        return print_node

    @staticmethod
    def get_inject_node(storage_dict_name, nodeName="Program", inject_type="local"):
        """
        Creates the AST node of the print statement that needs to be injected.

        Args:
            nodeName (str): The name of the node that is being injected.
            inject_type (str): The type of injection, can be 'local' or 'global'.

        Returns:
            ast.Module: The AST node of the print statement that needs to be injected.
        """

        if inject_type == "local":
            inject_func = "locals"
        else:
            inject_func = "globals"

        # Generate random variable names for the local variables so they do not interfere with the user their code.
        local_vars_varname = "local_vars_%s" % random.randint(1000, 10000000)
        var_name_varname = "var_name_%s" % random.randint(1000, 10000000)
        var_value_varname = "var_value_%s" % random.randint(1000, 10000000)

        # Generate the inject AST node
        inject_node = ast.Module(
            [
                ast.Assign(
                    targets=[ast.Name(id=local_vars_varname, ctx=ast.Store())],
                    value=ast.Call(
                        func=ast.Attribute(
                            value=ast.Call(
                                func=ast.Name(id=inject_func, ctx=ast.Load()),
                                args=[],
                                keywords=[],
                            ),
                            attr="copy",
                            ctx=ast.Load(),
                        ),
                        args=[],
                        keywords=[],
                    ),
                ),
                ast.For(
                    target=ast.Tuple(
                        elts=[
                            ast.Name(id=var_name_varname, ctx=ast.Store()),
                            ast.Name(id=var_value_varname, ctx=ast.Store()),
                        ],
                        ctx=ast.Store(),
                    ),
                    iter=ast.Call(
                        func=ast.Attribute(
                            value=ast.Name(id=local_vars_varname, ctx=ast.Load()),
                            attr="items",
                            ctx=ast.Load(),
                        ),
                        args=[],
                        keywords=[],
                    ),
                    body=[
                        ast.If(
                            test=ast.Compare(
                                left=ast.Name(id=var_name_varname, ctx=ast.Load()),
                                ops=[ast.In()],
                                comparators=[
                                    ast.List(
                                        elts=[
                                            ast.Constant(value=item)
                                            for item in BLACKLIST
                                        ],
                                        ctx=ast.Load(),
                                    )
                                ],
                            ),
                            body=[ast.Continue()],
                            orelse=[
                                ast.Module(
                                    [
                                        ast.If(
                                            test=ast.Compare(
                                                left=ast.Str(s=nodeName),
                                                ops=[ast.NotIn()],
                                                comparators=[
                                                    ast.Name(
                                                        id=storage_dict_name,
                                                        ctx=ast.Load(),
                                                    )
                                                ],
                                            ),
                                            body=[
                                                ast.Assign(
                                                    targets=[
                                                        ast.Subscript(
                                                            value=ast.Name(
                                                                id=storage_dict_name,
                                                                ctx=ast.Load(),
                                                            ),
                                                            slice=ast.Index(
                                                                value=ast.Str(
                                                                    s=nodeName
                                                                )
                                                            ),
                                                            ctx=ast.Store(),
                                                        )
                                                    ],
                                                    value=ast.Dict(
                                                        keys=[
                                                            ast.Name(
                                                                id=var_name_varname,
                                                                ctx=ast.Load(),
                                                            )
                                                        ],
                                                        values=[
                                                            ast.Name(
                                                                id=var_value_varname,
                                                                ctx=ast.Load(),
                                                            )
                                                        ],
                                                    ),
                                                )
                                            ],
                                            orelse=[
                                                ast.Assign(
                                                    targets=[
                                                        ast.Subscript(
                                                            value=ast.Subscript(
                                                                value=ast.Name(
                                                                    id=storage_dict_name,
                                                                    ctx=ast.Load(),
                                                                ),
                                                                slice=ast.Index(
                                                                    value=ast.Str(
                                                                        s=nodeName
                                                                    )
                                                                ),
                                                                ctx=ast.Load(),
                                                            ),
                                                            slice=ast.Index(
                                                                value=ast.Name(
                                                                    id=var_name_varname,
                                                                    ctx=ast.Load(),
                                                                )
                                                            ),
                                                            ctx=ast.Store(),
                                                        )
                                                    ],
                                                    value=ast.Name(
                                                        id=var_value_varname,
                                                        ctx=ast.Load(),
                                                    ),
                                                )
                                            ],
                                        )
                                    ]
                                )
                            ],
                        )
                    ],
                    orelse=[],
                ),
            ]
        )

        return inject_node
