import sys
import os
import numpy as np
import pandas as pd
from tqdm import tqdm

import constants


"""
Read in plot_data and calculate variance.
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
        os.mkdir(res_dir)

    # Start to parse
    data_dict = {}
    for target in targets:
        row_dict = {}
        for fuzzer in fuzzers:
            print(f'{target} {fuzzer}')

            # Locate outs dir
            outs_dir = os.path.join(bench_dir, fuzzer, target, 'outs')
            # Get number of fuzz camp
            outs = sorted([_ for _ in os.listdir(outs_dir) if _.startswith('out-')])
            n_fuzz_camp = len(outs)
            print(f'#camp {n_fuzz_camp}')

            # Collect covered edges for all fuzz camps
            final_edges = []
            for out in tqdm(outs, desc='Traverse outs'):
                pd_path = os.path.join(outs_dir, out, 'default', 'plot_data')
                if fuzzer == 'fairfuzz':
                    pd_df = pd.read_csv(pd_path, engine='python')
                else:
                    pd_df = pd.read_csv(pd_path, delimiter=', ', engine='python')
                # Read last line
                final_edges.append(pd_df['edges_found'].to_numpy()[-1])
            # Calculate variance
            # print(final_edges)
            # print(target, fuzzer, np.std(final_edges))
            row_dict[fuzzer] = np.std(final_edges)
        data_dict[target] = row_dict
    # Output to local
    df = pd.DataFrame(data_dict)
    df.to_csv(os.path.join(res_dir, 'all-std.csv'))
    df.T.to_csv(os.path.join(res_dir, 'all-std-T.csv'))
    print('Output to:', res_dir)
    print('-----------------------------------------------')
    print('Finish all :-)')
    print('-----------------------------------------------')
