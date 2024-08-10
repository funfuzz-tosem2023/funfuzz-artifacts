from ctypes import *
from ctypes.util import find_library

"""
To invoke C shm family in python 
"""

# Mode bits
IPC_CREAT = 0o1000          # Create entry if key does not exist */
IPC_EXCL = 0o2000           # Fail if key exists
# Keys
IPC_PRIVATE = 0             # Private key
DEFAULT_PERMISSION = 0o600  # Default file permission umode when creating files

if __name__ == '__main__':
    # Load dll `libc`
    libc = CDLL(find_library('c'))
    print(libc)

    # Access shm functions
    c_shmget = libc.shmget
    c_shmat = libc.shmat

    # Start to build shm
    shm_size = 8        # in bits
    shm_id = c_shmget(IPC_PRIVATE, shm_size, IPC_CREAT | IPC_EXCL | DEFAULT_PERMISSION)
    shm_ptr = c_shmat(shm_id, None, 0)
    print(shm_ptr, f'type={type(shm_ptr)}')
