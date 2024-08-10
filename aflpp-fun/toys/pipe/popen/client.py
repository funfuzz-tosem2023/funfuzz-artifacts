import sys
import time

"""
Receive data passed from popen?
"""


if __name__ == '__main__':
    logpath = './data.log'
    # Clear first
    logfile = open(logpath, 'w')
    logfile.close()
    # To write
    logfile = open(logpath, 'a')
    cnt = 10
    while cnt:
        cnt -= 1
        # Will this read operation waits?
        data = sys.stdin.readline().strip()
        logfile.write(f'[PY] {time.time()}, data={data}, len(data)={len(data)}\n')
        logfile.flush()
        time.sleep(1)

    logfile.close()
