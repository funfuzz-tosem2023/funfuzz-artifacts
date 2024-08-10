import os
import sys

"""
Check whether call_cnts[0][0] stores the number of all happened call.
"""

cGRN = "\x1b[0;32m"
cRST = "\x1b[0m"

if __name__ == '__main__':
    # Get call_cnts prints
    log_path = os.path.abspath(sys.argv[1])
    print(f'Check log: `{log_path}`...')

    # Parse logs like: [FUN] fsrv->call_cnts[0]=1326
    all_cnt = 0
    sum_cnt = 0
    prefix = '[FUN] '
    with open(log_path, 'r') as f:
        for line in f.readlines():
            if not (line.startswith(prefix) and '=' in line):
                continue
            content = line.replace(prefix, '')
            cnt_val = int(content.split('=')[-1])
            if '[0]' in content:
                all_cnt = cnt_val
            else:
                sum_cnt += cnt_val

    # Check: we count for (1-all, 2-caller, 3-call_relation), so all_cnt need to `*2`
    assert (all_cnt != 0 and all_cnt*2 == sum_cnt), f'all_cnt={all_cnt}, sum_cnt={sum_cnt}! :-('

    print(f'{cGRN}[SUCCESS]{cRST} Everything looks fine! :-)')
