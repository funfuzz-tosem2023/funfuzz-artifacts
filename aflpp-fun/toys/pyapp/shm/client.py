import os
import time

from ctypes import *
from ctypes.util import find_library

"""
A python application called by C parent.
"""

# Colors
cGRN = "\x1b[0;32m"
cRST = "\x1b[0m"

# ENV
SHM_ENV = '__SHM_ID'

if __name__ == '__main__':
    # Load dll `libc`
    libc = CDLL(find_library('c'))
    print(f'{cGRN}[PYAPP]{cRST} libc={libc}')

    # Prepare c_shmat
    c_shmat = libc.shmat
    c_shmat.restype = POINTER(c_int * 1)

    # Get shm_id from env
    shm_id = int(os.getenv(SHM_ENV))
    print(f'{cGRN}[PYAPP]{cRST} shm_id={shm_id}')

    # Attach to the shm
    # print(type(c_shmat(shm_id, None, 0)))
    # shm_ptr = pointer(c_int(c_shmat(shm_id, None, 0)))
    shm_ptr = c_shmat(shm_id, None, 0)
    print(f'{cGRN}[PYAPP]{cRST} shm_ptr={shm_ptr}')

    cnt = 6
    while cnt:
        cnt -= 1
        # First [0]: get the ptr; Second [0]: dereference the ptr to get the value
        print(f'{cGRN}[PYAPP]{cRST} shm_ptr[0]={shm_ptr[0][0]}')
        time.sleep(1)
