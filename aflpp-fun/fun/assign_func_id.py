import os
import sys

"""
Assign unique id for each function.
"""

if __name__ == '__main__':
    # Read in temp directory path from CLI.
    temp_dir = os.path.abspath(sys.argv[1])

    # Prepare file paths.
    in_file = os.path.join(temp_dir, 'funcNames')
    out_file = os.path.join(temp_dir, 'funcInfo')

    # Read in function names.
    print(f'Read function names from `{in_file}`')
    with open(in_file, 'r') as f:
        func_names = [_.strip() for _ in f.readlines()]

    # Sort and deduplicate.
    func_names = sorted(list(set(func_names)))

    # Output funcName-funcID pair.
    print(f'Output name-id pairs to `{out_file}`')
    with open(out_file, 'w') as f:
        cnt = 1
        for func_name in func_names:
            f.write(f'{func_name},{cnt}\n')
            cnt += 1
