import os
import sys
from ctypes import *
from ctypes.util import find_library

# Constants from ipc.h and afl-fuzz config.h.
IPC_CREAT           = 0o1000          
IPC_EXCL            = 0o2000          
IPC_NOWAIT          = 0o4000          
IPC_PRIVATE         = 0
IPC_RMID	        = 0	
DEFAULT_PERMISSION  = 0o600

# POC relevant string consants.
TOG_PAT     = 'POC_TOG_'
CMD_DELIM   = '--'
FILEIN_LOC  = '@@'
LOG         = '[LOG]'
LOG_DELIM   = '=================================================='

def load_c_shmat():
    return CDLL(find_library('c')).shmat


def load_c_shmget():
    return CDLL(find_library('c')).shmget


def load_c_shmctl():
    return CDLL(find_library('c')).shmctl


def load_c_shmdt():
    return CDLL(find_library('c')).shmdt


def load_shm(cshmat, cdtype, shmid: int, shmlen: int):
    """
    Attach to shm and return a ptr to this shm. As ctypes treat
    return type as c_int by default, We need to set proper return
    type before invoking a function.

    :param cshmat: the c shmat function to be called
    :param cdtype: the C type of the elements stored in the shm
    :param shmid: id of the shm to load
    :param shmlen: the number of elements assigned for the shm
    :return: a C pointer to the shm
    """
    cshmat.restype = POINTER(cdtype * shmlen)
    return cshmat(shmid, None, 0)


def parse_target_cmd() -> tuple:
    """
    Extract the part of running target binary from sys.argv.
    Also decide the type of input, i.e, use_stdin or use_file.
    """
    if CMD_DELIM not in sys.argv:
        print(f'{os.path.basename(__file__)}: Cannot work without a target binary!')
        print(f'Usage: {os.path.basename(__file__)} ... -- target_bin bin_opts... [@@]')
        exit(0)
    # Split argv and targt_cmd
    _idx = sys.argv.index(CMD_DELIM)
    _argv = sys.argv[1:_idx]
    _target_cmd = sys.argv[_idx+1:]
    # Determine input type, i.e., use_stdin or not.
    _use_stdin = False
    if FILEIN_LOC not in _target_cmd:
        _use_stdin = True
    return _argv, _target_cmd, _use_stdin
