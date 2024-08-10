import os
import sys
from time import sleep
from showmap import calibrate_one, args_map

"""
Calibrate plot_data (for fairfuzz) using afl++-showmap for
one target. Note that these script may require a resetting
of AFL_MAP_SIZE if target (e.g. mutool) is large.
"""

if __name__ == '__main__':
    if len(sys.argv) != 5:
        print('Usage: python3 <script> <showmap_path> <aflpp_bench> <fairfuzz_bench> <target>')
        sys.exit(0)
    # Parse arguments
    showmap_path = os.path.abspath(sys.argv[1])
    aflpp_bench = os.path.abspath(sys.argv[2])
    fairfuzz_bench = os.path.abspath(sys.argv[3])
    target = sys.argv[4]

    # Prepare target args
    target_path = os.path.join(aflpp_bench, target, target)
    target_args = [target_path] + args_map[target]
    print(f'Target args: {target_args}')
    print(f'Target path: {target_path}')
    sleep(3)  # Sleep to see log

    # Calibrate plot_data for one fuzz campaign
    outs_dir = os.path.join(fairfuzz_bench, target, 'outs')
    for fn in sorted(os.listdir(outs_dir)):
        if not fn.startswith('out-'):
            continue
        fuzzdata_dir = os.path.join(outs_dir, fn, 'default')
        calibrate_one(showmap_path, target_args, fuzzdata_dir)
