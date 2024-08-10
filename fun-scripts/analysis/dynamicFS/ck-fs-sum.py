import os
import sys
import pandas as pd

if __name__ == '__main__':
    if len(sys.argv) != 2:
        print('Usage: python3 <script> <FS_FILE>')
        sys.exit(-1)

    # Parse args
    fs_file = os.path.abspath(sys.argv[1])
    fs_type = os.path.basename(fs_file)
    print('fs_file', fs_file)

    # Deal with fs values accordingly
    if fs_type == 'debugFS':
        print('Check static FS...')
        # Static fs, calculate all fs values
        sum_fs = 0
        with open(fs_file, 'r') as f:
            for line in f.readlines():
                each_fs = float(line.split(',')[-1])
                sum_fs += each_fs
        print('sum_fs', sum_fs)
    elif fs_type == 'dynamicFS.csv':
        print('Check dynamic FS...')
        # Dynamic fs, pandas operations, check each row
        df = pd.read_csv(fs_file, index_col=0).drop(['time_elapsed'], axis=1)
        # get f3, f4
        selected_df = df[['parse_block_or_stmt', 'mjs_bcode_insert_offset']]
        # To numpy
        df_arr = df.to_numpy()
        selected_df_arr = selected_df.to_numpy()
        for idx in range(len(df_arr)):
            print('orig:', selected_df_arr[idx])
            print('norm:',
                  (selected_df_arr[idx] - df_arr[idx].min()) / (df_arr[idx].max() - df_arr[idx].min()))
    else:
        raise RuntimeError('Unsupported FS file type:', fs_type)
