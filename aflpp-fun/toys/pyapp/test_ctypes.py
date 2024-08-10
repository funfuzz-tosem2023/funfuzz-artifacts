import ctypes

from ctypes import *    # Import CDLL, cdata_types, repr & pointer, create_string_bufferetc...
from ctypes.util import find_library

"""
Using ctypes, the foreign calls for C functions.
"""

if __name__ == '__main__':
    # Find dynamic link libraries (dll).
    print('find_library(\'m\'), ', find_library('m'))
    print('find_library(\'c\'), ', find_library('c'))
    print('find_library(\'bz2\'), ', find_library('bz2'))
    print('find_library(\'AGL\'), ', find_library('AGL'))

    # Load dll `libc`.
    libc = CDLL(find_library('c'))
    print(libc)

    # Accessing function from the loaded dll
    c_printf = libc.printf
    c_puts = libc.puts
    c_time = libc.time
    print(c_printf)
    print(c_puts)
    print(c_time)

    # Fundamental C types
    c_s = c_wchar_p("Hello world!")
    print(c_s, ', val=`%s`' % c_s.value)

    # Call the accessed c functions
    print('Call the accessed c functions')
    c_printf(b'Hello world!\n')             # Need binary string, or cannot show correct content.
    c_puts(b'puts')

    # Pointer types
    i = c_int()
    int_ptr = pointer(i)
    print(f'i={i}')
    print(f'i.value={i.value}')
    print(f'int_ptr={int_ptr}')
    print(f'int_ptr.contents={int_ptr.contents}')
    print(f'byref(int_ptr)={byref(int_ptr)}')

