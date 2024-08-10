import sys
import os
import constants
import numpy as np
import pandas as pd
from tqdm import tqdm

"""
Read in plot_data, average them, and draw fuzz curves.
"""

fuzzers = constants.fuzzers
targets = constants.targets
# fuzzers = ['fun-static']
# targets = ['cxxfilt', 'djpeg', 'mjs', 'nm-new', 'readpng']
time_upper = constants.time_upper

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
    for target in targets:
        for fuzzer in fuzzers:
            print(f'{target} {fuzzer}')
            # Locate outs dir
            outs_dir = os.path.join(bench_dir, fuzzer, target, 'outs')
            # Get number of fuzz camp
            outs = sorted([_ for _ in os.listdir(outs_dir) if _.startswith('out-')])
            n_fuzz_camp = len(outs)
            print(f'#camp {n_fuzz_camp}')
            # Locate each plot_data. Find min, max, average in every plot_data
            edge_data = dict(min=np.full(time_upper, 999999),
                             max=np.zeros(time_upper),
                             ave=np.zeros(time_upper))
            for out in outs:
                print(out)
                pd_path = os.path.join(outs_dir, out, 'default', 'plot_data')
                if fuzzer == 'fairfuzz':
                    pd_df = pd.read_csv(pd_path, engine='python')
                else:
                    pd_df = pd.read_csv(pd_path, delimiter=', ', engine='python')
                # print(pd_df)
                # Selectively read in plot data (focus on edge data in this script)
                last_edge_data = 0
                for idx in tqdm(range(time_upper), desc='Parsing time points'):
                    tp = idx + 1
                    # Get data for current tp
                    tp_data = pd_df[pd_df['# relative_time'] == tp]
                    # print(tp_data)
                    if not tp_data.empty:
                        # Not empty, update last edge data
                        last_edge_data = tp_data['edges_found'].to_numpy()[0]
                    # Update full data set
                    edge_data['min'][idx] = min(edge_data['min'][idx], last_edge_data)
                    edge_data['max'][idx] = max(edge_data['max'][idx], last_edge_data)
                    edge_data['ave'][idx] += last_edge_data
            # Average by number of campaigns
            edge_data['ave'] /= n_fuzz_camp
            edge_df = pd.DataFrame(data=edge_data)
            edge_df['time'] = [(_ + 1) for _ in range(time_upper)]
            # Store to local
            csv_path = os.path.join(res_dir, f'{target}-{fuzzer}.csv')
            edge_df.to_csv(csv_path)
            print(f'Save to local: `{csv_path}`')
            print('======================================================')
    print('Finish all :-)!')
