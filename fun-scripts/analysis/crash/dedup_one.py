import sys
from deduplicate import *

if __name__ == '__main__':
    # Parse arg
    if len(sys.argv) != 2:
        print('Usage: python3 <script> <outs_dir> <target>')
        sys.exit(-1)
    outs_dir = os.path.abspath(sys.argv[1])
    target = sys.argv[2]
    # Parse log path
    crash_log = os.path.join(outs_dir, 'repro-crash')
    unique_crashes = parse_one_crash_log(path=crash_log, target=target)
    for crash in unique_crashes:
        print(crash)
    print(f'Find {len(unique_crashes)} unique crashes')
    pass
