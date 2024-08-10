import os

if __name__ == '__main__':

    c_macro = 'FUN_FUNC_NUM'

    # Find afl debug.h
    if not os.getenv('FUN_HOME'):
        raise RuntimeError(f'Load {c_macro} failed! Please set FUN_HOME first!')
    _debug_h_path = os.path.join(os.getenv('FUN_HOME'), 'include', 'config.h')
    print(f"@FUN, _debug_h_path={_debug_h_path}")

    # Parse debug.h
    with open(_debug_h_path, 'r') as f:
        for line in f.readlines():
            if not line.startswith(f'#define {c_macro}'):
                continue
            print(line)
    # print(num_expr)



