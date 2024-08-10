import os
import sys
from time import sleep
from showmap import calibrate_one, args_map

"""
Calibrate plot_data (for fairfuzz and afl_kscheduler) using afl++-showmap
Note that these scripts may require a resetting of AFL_MAP_SIZE if target 
(e.g. mutool) is large.
"""

if __name__ == '__main__':
    if len(sys.argv) != 4:
        print('Usage: python3 <script> <showmap_path> <aflpp_target> <fuzzdata_dir>')
        sys.exit(0)
    # Parse arguments
    showmap_path = os.path.abspath(sys.argv[1])
    target_path = os.path.abspath(sys.argv[2])
    fuzzdata_dir = os.path.abspath(sys.argv[3])

    # Prepare target args
    target_name = os.path.basename(target_path)
    target_args = [target_path] + args_map[target_name]
    print(f'Target args: {target_args}')
    sleep(3)  # Sleep to see log

    # Calibrate plot_data for one fuzz campaign
    calibrate_one(showmap_path, target_args, fuzzdata_dir)
