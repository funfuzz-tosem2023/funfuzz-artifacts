import sys
import os
import pandas as pd

from common import *

"""
Create table for final region coverage.
"""

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("Usage: <this_script.py> <data_dir>")
        exit(0)
    data_dir = os.path.abspath(sys.argv[1])
    res_dir = os.path.join(data_dir, '_results')
    data_csv = os.path.join(res_dir, 'data.csv')

    # Start to process.
    data_df = pd.read_csv(data_csv, index_col=0)
    final_cov_df = data_df.loc[data_df['time'] == 86400]

    # Collect avg final region coverage
    avg_reg_dict = {}
    for fuzzer in fuzzers:
        fuzzer_df = final_cov_df.loc[final_cov_df['fuzzer'] == fuzzer]
        if fuzzer_df.empty:
            print('No such fuzzer, skip:', fuzzer)
            continue
        fuzzer_dict = {}
        for target in targets:
            print(fuzzer, target)
            camp_df = final_cov_df.loc[(final_cov_df['fuzzer'] == fuzzer) &
                                       (final_cov_df['benchmark'] == target)]
            if camp_df.empty:
                print('Cannot find camp_df, skip')
                continue
            avg_region = camp_df['region_cov'].mean()
            # print(avg_region)
            fuzzer_dict[target] = avg_region
        avg_reg_dict[fuzzer] = fuzzer_dict
    # Compute delta
    avg_reg_df = pd.DataFrame(data=avg_reg_dict)
    # print(avg_reg_df)
    delta_df = pd.DataFrame()
    for col in avg_reg_df.columns:
        # Delta in percentage
        delta_col = (avg_reg_df[col] - avg_reg_df['aflpp']) / avg_reg_df['aflpp'] * 100
        delta_df[col] = avg_reg_df[col].round(2)
        if col != 'aflpp':
            # No need to computate delta for afl++
            delta_df[f'{col}-delta'] = delta_col.round(2)
    print(delta_df)
    # Output to local
    delta_csv = os.path.join(res_dir, 'final_cov.csv')
    delta_df.to_csv(delta_csv)
    print('Output to:', delta_csv)
