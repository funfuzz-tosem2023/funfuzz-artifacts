import time
import os

"""

A python application called by C parent.

"""

cGRN = "\x1b[0;32m"
cRST = "\x1b[0m"

if __name__ == '__main__':

    while 1:
        print(f'{cGRN}[PYAPP]{cRST} Hello! My pid is `{os.getpid()}` :-) ')
        time.sleep(1)
