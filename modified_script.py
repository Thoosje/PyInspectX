var1 = 1


def print_local_vars(scope_dict):
    print(f'\nLocal Variables in scope Program:')
    for var_name, var_value in scope_dict.items():
        if var_name[0:2] == '__' and var_name[-2:] == '__':
            continue
        if var_name == 'print_local_vars':
            continue
        print('%s: %s' % (var_name, var_value))


print_local_vars(locals())
