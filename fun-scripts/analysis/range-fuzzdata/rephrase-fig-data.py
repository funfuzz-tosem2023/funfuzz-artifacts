import os
import sys
import pandas as pd

"""
Rephrase the data to do not to draw plot from zero.
To this end, this script find the first row of all-non-zero to replace
rows with zero.  
"""

if __name__ == '__main__':

    if len(sys.argv) != 2:
        print('Usage: <this_script> <bench_dir>')
        sys.exit(1)

    # Directory puts fuzz data
    bench_dir = os.path.abspath(sys.argv[1])

    # Directory output analysis results
    res_dir = os.path.join(bench_dir, '_results')
    if not os.path.exists(res_dir):
        raise RuntimeError(f'Cannot find results data at: {res_dir}')

    # Rephrase each
    for fn in sorted(os.listdir(res_dir)):
        if not fn.endswith('.csv'):
            continue
        csv_file = os.path.join(res_dir, fn)
        print('[LOG] Rephrase:', csv_file)
        df = pd.read_csv(csv_file, index_col=0)
        # Turn data
        csv_data = df.to_numpy()
        first_all_non_zero_row = None
        for row in csv_data:
            # Find the first all-non-zero row
            if row[0] != 0 and row[1] != 0 and row[2] != 0:
                first_non_all_zero_row = row
                break
        # Rephrase data
        for row in csv_data:
            # Replace with-zero row with the first all-non-zero
            if row[0] == 0 or row[1] == 0 or row[2] == 0:
                row[0] = first_non_all_zero_row[0]
                row[1] = first_non_all_zero_row[1]
                row[2] = first_non_all_zero_row[2]
        df = pd.DataFrame(csv_data, columns=df.columns)
        # print(df)
        df.to_csv(csv_file)

    print('[LOG] -----------------------------------------')
    print('[LOG] Finish all :-)')
    print('[LOG] -----------------------------------------')
