import sys
import os
from time import sleep

from fuzzdata import targets
from showmap import calibrate_one, args_map

"""
Note that these script may require a resetting
of AFL_MAP_SIZE if target (e.g. mutool) is large.
"""


if __name__ == '__main__':
    if len(sys.argv) != 4:
        print('Usage: python3 <script> <showmap_path> <aflpp_bench_dir> <bench_dir>')
        sys.exit(0)

    # Parse arguments
    showmap_path = os.path.abspath(sys.argv[1])
    aflpp_bench_dir = os.path.abspath(sys.argv[2])
    bench_dir = os.path.abspath(sys.argv[3])        # To calibrate it

    # Log failed bench
    failure_log_path = os.path.join(bench_dir, 'failed-calibrations.log')
    if os.path.exists(failure_log_path):
        os.remove(failure_log_path)

    # Calibrate for each target
    for target in targets:
        target_path = os.path.join(aflpp_bench_dir, target, target)
        target_args = [target_path] + args_map[target]
        print(f'Target args: {target_args}')
        sleep(3)    # Sleep to see log
        outs_dir = os.path.join(bench_dir, target, 'outs')
        if not os.path.exists(target_path):
            print(f'Does not exist: `{target_path}`')
            continue
        if not os.path.isdir(outs_dir):
            print(f'Is not dir: `{outs_dir}`')
            continue
        # Calibrate each fuzzdata dir
        for fn in os.listdir(outs_dir):
            if not fn.startswith('out-'):
                print(f'Invalid out fn: `{fn}`')
                continue
            fuzzdata_dir = os.path.join(outs_dir, fn, 'default')
            print('===========================================================')
            print(f'Calibrate fuzz data for: `{fuzzdata_dir}`')
            try:
                calibrate_one(showmap_path, target_args, fuzzdata_dir)
            except Exception:
                with open(failure_log_path, 'a') as flog:
                    flog.write(f'{fuzzdata_dir}\n')
                    print(f'Failed with: `{fuzzdata_dir}`!')
