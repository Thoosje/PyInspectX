import json
inspect_blacklist_6596899 = ['__builtins__', '__doc__', '__file__',        
    '__name__', '__package__', '__loader__', '__spec__', '__annotations__',
    '__cached__', 'inspect_storage_8305705', 'inspect_debug_141318',       
    'inspect_blacklist_6596899']
inspect_storage_8305705 = {}


def inspect_debug_141318(node_name, local_variables_copy):
    for var_name, var_value in local_variables_copy.items():
        if str(type(var_value)) == "<class 'function'>":
            return
        if var_name in inspect_blacklist_6596899:
            continue
        elif node_name not in inspect_storage_8305705:
            inspect_storage_8305705[node_name] = {var_name: var_value}     
        else:
            inspect_storage_8305705[node_name][var_name] = var_value       


def func1(var1):

    def func2(test):
        var3 = 'vvv' + test
        inspect_debug_141318('func2', locals().copy())
    func2(var1)
    inspect_debug_141318('func1', locals().copy())


func1('hi')
print(json.dumps(inspect_storage_8305705))