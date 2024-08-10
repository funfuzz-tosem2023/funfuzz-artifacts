import sys
import os
import pandas as pd

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print('Usage: <this_script> <afl_pd_path>')
        exit()
    # Read in path.
    pd_path = os.path.abspath(sys.argv[1])
    df = pd.read_csv(pd_path, delimiter=', ', engine='python')

    # Calculate time range.
    unix_tps = df['# unix_time'].to_numpy()
    camp_dura = unix_tps[-1] - unix_tps[0]
    print('Relative Campaign duration:', camp_dura)
