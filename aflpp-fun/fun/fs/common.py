import os

"""
Constants and utilities used by the FS calculator.
"""


# ------------- #
#   Constants   #
# ------------- #


# Filenames
CALL_SITES = 'bbCalls'
FUNC_INFO = 'funcInfo'
CALL_GRAPH = 'callGraph'
DEBUG_CG = 'debugCG'
STATIC_FS = 'staticFS'
DEBUG_FS = 'debugFS'
DYNAMIC_FS = 'dynamicFS.csv'

# Colors
cGRN = "\x1b[0;32m"
cRST = "\x1b[0m"

# Debug constants
FSLOG = 'dcclog'
FUN_DEBUG_STD = 'FUN_DEBUG_STD'
LOG_H_FILE = '[FUN-FS]'
LOG_H_STD = f'{cGRN}{LOG_H_FILE}{cRST}'
LOG_FILE = f'/tmp/aflpp-fun/{FSLOG}'


# ------------- #
#   Utilities   #
# ------------- #


def fslog(mes):
    print(LOG_H_STD, mes)


def debug_fslog(mes, tostd: bool = True, logfile: str = LOG_FILE):
    if tostd:
        fslog(mes)
    else:
        # Print debug info into file.
        with open(logfile, 'a') as _f:
            _f.write(f'{LOG_H_FILE} {mes}\n')


def elapsed_time(start_time: float, cur_time: float) -> float:
    return cur_time - start_time


def empty_logfile(path: str):
    _f = open(path, 'w')
    _f.close()
