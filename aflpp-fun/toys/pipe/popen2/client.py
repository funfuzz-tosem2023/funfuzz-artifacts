import sys
import time
import signal

"""
Receive data passed from popen?
"""


# def sigterm_handler(_signo, _stack_frame):
    # Raises SystemExit(0):
    # sys.exit(0)


if __name__ == '__main__':

    # signal.signal(signal.SIGTERM, sigterm_handler)

    logpath = './data.log'
    # Clear first
    logfile = open(logpath, 'w')
    logfile.close()
    # To write
    logfile = open(logpath, 'a')
    cnt = 0
    try:
        while True:
            cnt += 1
            logfile.write(f'[PY] In loop({cnt}), going to read stdin...\n')
            logfile.flush()
            data = sys.stdin.readline().strip()
            logfile.write(f'[PY] {time.time()}, data=`{data}`, len(data)={len(data)}\n')
            logfile.flush()
            time.sleep(1)
    finally:
        logfile.close()
