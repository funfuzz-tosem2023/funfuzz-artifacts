import os
import sys

import pandas as pd

from common import *

"""

Extract covered edges by given time gap. The style of the resultant csv file
is similar to FuzzBench's data.csv. This script focuses on the following
FuzzBench columns:  

  - 'fuzzer': the used fuzzer
  - 'benchmark': the name of the fuzz target
  - 'trial_id': the index of the campaign 
  - 'time': the time point record coverage
  - 'edges_covered': the coverage
   
"""


def locate_llvm_cov_csvs(root_dir: str) -> list:
    """
    Locate afl out dir recursively. An afl out dir must have a plot_data
    and a queue/ dir under it.
    """
    _csvs = set()
    _folder_stack = [root_dir]
    while len(_folder_stack) != 0:
        _dir = _folder_stack.pop()
        if 'llvm-cov.csv' in os.listdir(_dir):
            _csvs.add(os.path.join(_dir, 'llvm-cov.csv'))
        else:
            # Dig recursively
            for _fn in os.listdir(_dir):
                _path = os.path.join(_dir, _fn)
                if os.path.isdir(_path):
                    _folder_stack.append(_path)
    return sorted(list(_csvs))


def read_and_concat_csvs(csv_files: list) -> pd.DataFrame:
    _df_list = []
    # Add trial_id to match plot logics
    _trial_cnt = 1
    for _csv in csv_files:
        _df = pd.read_csv(_csv, index_col=0)
        _df['trial_id'] = _trial_cnt
        _trial_cnt += 1
        _df_list.append(_df)
    return pd.concat(_df_list)


if __name__ == '__main__':

    if len(sys.argv) != 2:
        print('python3 <this_script> <llvm_cov_data_dir>')
        exit(0)

    # Parse args.
    llvm_cov_data_dir = os.path.abspath(sys.argv[1])

    # Prepare _results dir
    res_dir = os.path.join(llvm_cov_data_dir, '_results')
    if not os.path.exists(res_dir):
        os.mkdir(res_dir)

    # Read in llvm-cov.csv and merge
    fuzzer_dfs = []
    for fn in sorted(os.listdir(llvm_cov_data_dir)):
        if fn not in fuzzers:
            continue
        fuzzer = fn
        fuzzer_dir = os.path.join(llvm_cov_data_dir, fn)
        # fuzzer x target -> campaign config
        for fn1 in sorted(os.listdir(fuzzer_dir)):
            if fn1 not in targets:
                continue
            target = fn1
            print(fuzzer, target)
            fuzzer_target_dir = os.path.join(fuzzer_dir, target, 'outs')
            llvm_cov_csvs = locate_llvm_cov_csvs(fuzzer_target_dir)
            fdf = read_and_concat_csvs(llvm_cov_csvs)
            # Turn into fuzzer df
            fdf['fuzzer'] = fuzzer
            fdf['benchmark'] = target
            fdf['edges_covered'] = fdf['region_cov']
            # fdf['edges_covered'] = fdf['region_rate']
            fuzzer_dfs.append(fdf)
            print('---------------------------------------')
    # Concat again
    df = pd.concat(fuzzer_dfs)
    # # Some weird strings may exist in the extracted data. Remove them.
    # # Turns out that there are bad data inside aflgo/cxxfilt/out-1
    # keep_rows = []
    # for row in df.to_numpy():
    #     # print(row[1], len(row))
    #     if row[0] != 'time':
    #         keep_rows.append(row)
    # # Output to local
    # df = pd.DataFrame(data=keep_rows,
    #                   columns=['time', 'region_total', 'region_miss',
    #                            'region_cov', 'region_rate', 'trial_id',
    #                            'fuzzer', 'benchmark', 'edges_covered'])
    csv_path = os.path.join(res_dir, 'data.csv')
    df.to_csv(csv_path)
    print(df)
    print('Output to:' + csv_path)
