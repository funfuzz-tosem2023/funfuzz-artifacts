import os
import sys
from time import sleep
from reproduce import reproduce_one_out

"""
Rerun test cases and record crash track for one target
"""

if __name__ == '__main__':
    if len(sys.argv) != 4:
        print('Usage: python3 <script> <target> <bench_dir> <asan_dir>')
        sys.exit(-1)
    # Get arguments
    target = sys.argv[1]
    bench_dir = os.path.abspath(sys.argv[2])
    asan_dir = os.path.abspath(sys.argv[3])

    # Iterate for all target
    log_path = os.path.join(bench_dir, target, f'repro-crash')
    # Create log file before starting
    if os.path.exists(log_path):
        os.remove(log_path)
    # Locate asan target
    target_path = os.path.join(asan_dir, target, target)
    # Locate outs dir and process each out
    outs_dir = os.path.join(bench_dir, target, 'outs')
    # Log
    print(f'[LOG] Crash log `{log_path}`')
    print(f'[LOG] Target path `{target_path}`')
    print(f'[LOG] Outs dir `{outs_dir}`')
    sleep(2)
    for fn in os.listdir(outs_dir):
        if not fn.startswith('out-'):
            continue
        fuzzdata_dir = os.path.join(outs_dir, fn, 'default')
        if not os.path.exists(fuzzdata_dir):
            fuzzdata_dir = os.path.join(outs_dir, fn)
        # Reproduce
        reproduce_one_out(fuzzdata_dir, target, target_path, log_path)
    # Seperator
    print('======================================================================')
