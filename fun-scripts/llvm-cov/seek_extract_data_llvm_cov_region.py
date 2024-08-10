import os
import sys
import pandas as pd
from common import *
from extract_data_llvm_cov_region import locate_llvm_cov_csvs, read_and_concat_csvs


def cutoff_prefix(prefix_to_cutoff: str, target_str: str) -> str:
    return target_str.replace(prefix_to_cutoff, '')


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

    # Locate all llvm-cov.csv
    all_cov_csvs = locate_llvm_cov_csvs(llvm_cov_data_dir)

    # Filter by fuzzer x target
    fuzzer_dfs = []
    for fuzzer in fuzzers:
        for target in targets:
            camp_csvs = [_ for _ in all_cov_csvs if (fuzzer in cutoff_prefix(llvm_cov_data_dir, _))
                         and (target in cutoff_prefix(llvm_cov_data_dir, _))]
            if len(camp_csvs) == 0:
                print(f'[WARN] Skip as no CSV is found for: {fuzzer}*{target}')
                continue
            print(f'[LOG] CSVs for {fuzzer}*{target}:', camp_csvs)
            print(f'[LOG] Find {len(camp_csvs)} CSVs.')
            fdf = read_and_concat_csvs(camp_csvs)
            # Turn into fuzzer df
            fdf['fuzzer'] = fuzzer
            fdf['benchmark'] = target
            fdf['edges_covered'] = fdf['region_cov']
            # fdf['edges_covered'] = fdf['region_rate']
            fuzzer_dfs.append(fdf)
            print('---------------------------------------')
    # Concat further
    df = pd.concat(fuzzer_dfs)
    csv_path = os.path.join(res_dir, 'data.csv')
    df.to_csv(csv_path)
    print(df)
    print('Output to:' + csv_path)
