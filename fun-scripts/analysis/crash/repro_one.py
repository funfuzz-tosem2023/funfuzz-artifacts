import os
import sys
from reproduce import reproduce_one_out

"""
Entry point for reproducing one out directory
"""

if __name__ == '__main__':
    if len(sys.argv) != 3:
        print('Usage: python3 <script> <asan_target> <out_dir>')
        sys.exit(-1)
    # Get arguments
    asan_target_path = os.path.abspath(sys.argv[1])
    out_dir = os.path.abspath(sys.argv[2])

    # Parse arguments
    target = os.path.basename(asan_target_path)
    fuzzdata_dir = os.path.join(out_dir, 'default')
    log_path = os.path.join(out_dir, 'repro-crash')
    # Create log file before starting
    if os.path.exists(log_path):
        os.remove(log_path)
    print(f'[LOG] Output crash log to `{log_path}`')

    # Reproduce
    reproduce_one_out(fuzzdata_dir, target, asan_target_path, log_path)

    print('============================================================')
    print(f'[LOG] Finished :-). Find log at `{log_path}`')
