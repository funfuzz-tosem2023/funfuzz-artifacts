import os.path
import sys

"""
Relative path is computed from the folder it given. 
So tha abspath of path is computed from `../` (where a.out is).
"""


if __name__ == '__main__':
    path1 = os.path.abspath(sys.argv[1])
    path2 = os.path.abspath(sys.argv[2])
    path3 = os.path.abspath(sys.argv[3])
    print(f'[PY] We get abs-relative-path0 like: `{path1}`')
    print(f'[PY] We get abs-relative-path1 like: `{path2}`')
    print(f'[PY] We get abs-absolute-path like: `{path3}`')

