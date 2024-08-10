import sys
from sigdata import *

"""
Data analysis and visualizations around sig_score
"""

if __name__ == '__main__':

    if len(sys.argv) != 2:
        print('Usage: <this_script> <root_dir>')
        sys.exit(1)

    # Parse arguments
    root_dir = os.path.abspath(sys.argv[1])

    # Prepare directory to output analysis results.
    res_dir = os.path.join(root_dir, '_results')
    if not os.path.exists(res_dir):
        os.mkdir(res_dir)

    # Read in csv. Use normalized df
    df_li = []
    for fn in sorted(os.listdir(root_dir)):
        target_dir = os.path.join(root_dir, fn)
        if fn.startswith('.') or fn.startswith('_') or (not os.path.isdir(target_dir)):
            continue
        # sd_path = os.path.join(target_dir, 'q_sigdata')
        sd_path = os.path.join(target_dir, 'outs', 'out-1', 'default', 'q_sigdata')
        print(sd_path)
        df = normalize_sig_score(pd.read_csv(sd_path, index_col='id'))
        df_li.append(df)
    sd_df = pd.concat(df_li, ignore_index=True)

    # ---------- #
    #  Analysis  #
    # ---------- #

    # Save pearson correlations
    pearson_df = sd_df[["sig_score", "bitmap_size"]].corr(method='pearson')
    print('Pearson')
    print(pearson_df)
    csv_path = os.path.join(res_dir, 'pearson_sigdata.csv')
    pearson_df.to_csv(csv_path)
    print(f'Save sigdata PCC to `{csv_path}`')

    # Collect r2
    r2_data = {}

    # Scatter chart: How sig_score correlates with bitmap_size (coverage)?
    # And how favored and unfavored points distribute.
    a, b, ave_a, r2 = draw_sig_score_cov_scatter_and_output(sd_df, res_dir, 'norm-sigscore-cov-scatter', True,
                                                            True)
    print(f'[Norm] Estimate parameter: a {a}, b {b}, ave_a {ave_a}, r2 {r2}')
    r2_data['norm'] = r2

    # How many favored seeds are below/above the estimation line?
    csv_path = os.path.join(res_dir, 'norm-favored-est-a-b.csv')
    favored_est_analysis(data=sd_df, path=csv_path, p_a=a, p_b=b, use_norm=True)

    # Approximate with ave_a?
    csv_path = os.path.join(res_dir, 'norm-favored-est-ave_a.csv')
    favored_est_analysis(data=sd_df, path=csv_path, p_a=ave_a, use_norm=True)

    a, b = draw_sig_score_cov_scatter_and_output(sd_df, res_dir, 'sigscore-cov-scatter')
    print(f'[Non-norm] Estimate parameter: a {a}, b {b}')

    a, b, ave_a, r2 = draw_sig_score_cov_scatter_and_output(sd_df, res_dir, 'ave_a-sigscore-cov-scatter', True)
    print(f'[Non-norm] Estimate parameter: a {a}, b {b}, ave_a {ave_a}, r2 {r2}')
    r2_data['non-norm'] = r2

    # Save r2
    r2_df = pd.DataFrame(data=r2_data, index=['r2-score'])
    csv_path = os.path.join(res_dir, 'r2.csv')
    print(r2_df)
    r2_df.to_csv(csv_path)

    # How many favored seeds are below/above the estimation line?
    csv_path = os.path.join(res_dir, 'favored-est-a-b.csv')
    favored_est_analysis(data=sd_df, path=csv_path, p_a=a, p_b=b)

    # Approximate with ave_a?
    csv_path = os.path.join(res_dir, 'favored-est-ave_a.csv')
    favored_est_analysis(data=sd_df, path=csv_path, p_a=ave_a)

    # Violin plot: How normalized sig_scores distribute?
    draw_sig_score_violin_and_output(sd_df, res_dir, 'sigscore-violin')
