import sys
import os
import numpy as np
import pandas as pd
from scipy.stats import mannwhitneyu, ttest_ind
from commons import periods

if __name__ == '__main__':
    data_dir = os.path.abspath(sys.argv[1])
    execs_csv = os.path.join(data_dir, 'execs.csv')
    # Read in execs data. Remove the last average data row.
    execs_df = pd.read_csv(execs_csv, index_col=0).iloc[:-1, :]
    # print(execs_df)
    pval_dict = {}
    # Calculate Mann-Whitney
    for period1 in execs_df.columns:
        period_dict = {}
        for period2 in execs_df.columns:
            print(period1, period2)
            stats, p_val = mannwhitneyu(execs_df[period1], execs_df[period2])
            # stats, p_val = ttest_ind(execs_df[period1], execs_df[period2])
            sig = 'Insignificantly'
            if p_val < 0.05:
                sig = 'Significantly'
            print(f'stats={stats}', f'p_val={p_val}', f'{sig}-Different')
            period_dict[period2] = np.round(p_val, 4)
        pval_dict[period1] = period_dict
    # print(pval_dict)
    # Output to local
    out_csv = os.path.join(data_dir, 'mannwhitney-upval.csv')
    upval_df = pd.DataFrame(data=pval_dict)
    print(upval_df)
    upval_df.to_csv(out_csv)
    print('[LOG] Write to:', out_csv)
    # Concentrate on the average row
    ave_execs_df = pd.read_csv(execs_csv, index_col=0).T
    ave_execs_df['periods'] = periods
    pcc = ave_execs_df[['periods', 'ave_total_execs']].corr(method='pearson')
    print(pcc)
