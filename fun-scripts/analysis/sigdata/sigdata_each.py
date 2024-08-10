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

    for fn in os.listdir(root_dir):
        target_dir = os.path.join(root_dir, fn)
        if fn.startswith('.') or fn.startswith('_') or (not os.path.isdir(target_dir)):
            continue

        # Prepare directory to output analysis results.
        res_dir = os.path.join(target_dir, '_results')
        if not os.path.exists(res_dir):
            os.mkdir(res_dir)

        print('--------------------------------------------------')
        print('Target:', fn)

        # Load as sigdata as dataframe
        # sd_path = os.path.join(target_dir, 'q_sigdata')
        sd_path = os.path.join(target_dir, 'outs', 'out-1', 'default', 'q_sigdata')
        sd_df = pd.read_csv(sd_path)

        # Normalize sig_score
        norm_sd_df = normalize_sig_score(data=sd_df)
        csv_path = os.path.join(res_dir, 'norm_q_sigdata.csv')
        print(f'Save norm sigdata to `{csv_path}`')

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
        a, b, ave_a, r2 = draw_sig_score_cov_scatter_and_output(norm_sd_df, res_dir, 'norm-sigscore-cov-scatter',
                                                                True, True)
        print(f'[Norm] Estimate parameter: a {a}, b {b}, ave_a {ave_a}, r2 {r2}')
        r2_data['norm'] = r2

        # How many favored seeds are below/above the estimation line?
        csv_path = os.path.join(res_dir, 'norm-favored-est-a-b.csv')
        favored_est_analysis(data=norm_sd_df, path=csv_path, p_a=a, p_b=b, use_norm=True)

        # Approximate with ave_a?
        csv_path = os.path.join(res_dir, 'norm-favored-est-ave_a.csv')
        favored_est_analysis(data=norm_sd_df, path=csv_path, p_a=ave_a, use_norm=True)

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

        # Box plot: How normalized sig_scores distribute?
        draw_sig_score_box_and_output(norm_sd_df, res_dir, 'sigscore-box')

        # Violin plot: How normalized sig_scores distribute?
        draw_sig_score_violin_and_output(norm_sd_df, res_dir, 'sigscore-violin')

        # Scatter for paper: how feasible of our method? What is our motivation?
        draw_scatter_paper_method(norm_sd_df, res_dir, target=fn)
        draw_scatter_paper_method(norm_sd_df, res_dir, target=fn, use_norm=True)
        draw_scatter_paper_motivation(norm_sd_df, res_dir, target=fn)
