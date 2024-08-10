import sys
import os
import pandas as pd

"""
Gather the r2 score achieved at each fuzz targets
"""

if __name__ == '__main__':

    if len(sys.argv) != 2:
        print('Usage: <this_script> <root_dir>')
        sys.exit(1)

    # Parse arguments
    root_dir = os.path.abspath(sys.argv[1])

    # Prepare directory to output analysis results.
    total_res_dir = os.path.join(root_dir, '_results')
    if not os.path.exists(total_res_dir):
        os.mkdir(total_res_dir)

    # Start to extract data
    data_li = []
    for target in sorted(os.listdir(root_dir)):
        target_dir = os.path.join(root_dir, target)
        if target.startswith('.') or target.startswith('_') or (not os.path.isdir(target_dir)):
            continue
        # Locate each results
        results_dir = os.path.join(target_dir, '_results')
        if not os.path.exists(results_dir):
            print('Do not find result dir:', results_dir)
            continue
        # Locate PCC and r2 csv
        r2_csv = os.path.join(results_dir, 'r2.csv')
        pcc_csv = os.path.join(results_dir, 'pearson_sigdata.csv')
        # Read pcc
        pcc_df = pd.read_csv(pcc_csv, index_col=0)
        pcc_val = pcc_df['bitmap_size'].loc['sig_score']
        # Read r2. 2D
        r2_vals = pd.read_csv(r2_csv, index_col=0).to_numpy()
        vals = [target, pcc_val]
        vals.extend(r2_vals[0])
        # Append data
        data_li.append(vals)
    # To csv
    print(data_li)
    output_csv = os.path.join(total_res_dir, 'total_pcc_r2.csv')
    df = pd.DataFrame(data_li, columns=['target', 'PCC', 'norm_r2', 'r2'])
    df.to_csv(output_csv)
    print('Output to:', output_csv)
