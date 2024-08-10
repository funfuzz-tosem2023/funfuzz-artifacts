import os
import sys

import pandas as pd

import constants


"""
Gather average coverage into one csv.
"""

fuzzers = constants.fuzzers
targets = constants.targets

if __name__ == '__main__':

    if len(sys.argv) != 2:
        print('Usage: <this_script> <bench_dir>')
        sys.exit(1)

    # Directory puts fuzz data
    bench_dir = os.path.abspath(sys.argv[1])

    # Directory output analysis results
    res_dir = os.path.join(bench_dir, '_results')
    if not os.path.exists(res_dir):
        raise RuntimeError(f'Invalid result dir: {res_dir}')

    # Start to parse
    data_dict = {}
    for target in targets:
        row_dict = {}
        for fuzzer in fuzzers:
            csv_path = os.path.join(res_dir, f'{target}-{fuzzer}.csv')
            print(csv_path)
            # Get final ave edge
            df = pd.read_csv(csv_path)
            final_ave_edge = df['ave'].to_numpy()[-1]
            # Build each row
            row_dict[fuzzer] = final_ave_edge
            row_dict[f'{fuzzer}-inc'] = 100 * (final_ave_edge - row_dict['aflpp']) / row_dict['aflpp']  # in percentage
        # Build the whole dict
        data_dict[target] = row_dict
    # Output to local
    df = pd.DataFrame(data_dict)
    df.to_csv(os.path.join(res_dir, 'all-ave.csv'))
    df.T.to_csv(os.path.join(res_dir, 'all-ave-T.csv'))
    print('Output to:', res_dir)
    print('-----------------------------------------------')
    print('Finish all :-)')
    print('-----------------------------------------------')
