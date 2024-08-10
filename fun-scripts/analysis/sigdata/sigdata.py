import os
import numpy as np
import pandas as pd
import matplotlib
import matplotlib.pyplot as plt
from sklearn.metrics import r2_score
from matplotlib.ticker import MultipleLocator, FormatStrFormatter

"""
Data analysis and visualizations around sig_score
"""

# To avoid type-3 font error
matplotlib.rcParams['pdf.fonttype'] = 42
matplotlib.rcParams['ps.fonttype'] = 42
plt.rcParams['font.size'] = 14
gline_width = 0.2


def normalize_sig_score(data: pd.DataFrame) -> pd.DataFrame:
    _norm_data = data.copy()
    for _col in ['sig_score', 'bitmap_size']:
        _diff = data[_col].max() - data[_col].min()
        _norm_data[f'norm_{_col}'] = (data[_col] - data[_col].min()) / _diff
    return _norm_data


def draw_scatter_paper_motivation(data: pd.DataFrame, dpath: str, target: str):
    """
    To illustrate motivation for paper OOPSLA'23. Figure with scatter and grids
    """
    _size = (5.5, 4.5)
    _alpha = 0.75
    _fig, _ax = plt.subplots(1, 1, figsize=_size)
    _xlabel = 'Edge Coverage'
    _ylabel = 'Significance Score'
    # Scatter
    _ax.scatter(x=data['bitmap_size'],
                y=data['sig_score'],
                label='Seed', s=8, marker='o', alpha=_alpha, c='blue')
    # Set x-axis and y-axis
    _ax.set(xlabel=_xlabel, ylabel=_ylabel)
    _xinterval = 100
    _x_major = MultipleLocator(_xinterval)
    _x_major_fmt = FormatStrFormatter('%d')
    _ax.xaxis.set_major_locator(_x_major)
    _ax.xaxis.set_major_formatter(_x_major_fmt)
    _ax.set_xlim([data['bitmap_size'].min()-_xinterval, data['bitmap_size'].max()+_xinterval/2])
    _yinterval = 0.25
    _y_major = MultipleLocator(_yinterval)
    _y_major_fmt = FormatStrFormatter('%.2f')
    _ax.yaxis.set_major_locator(_y_major)
    _ax.yaxis.set_major_formatter(_y_major_fmt)
    _ax.set_ylim([data['sig_score'].min()-_yinterval, data['sig_score'].max()+_yinterval])
    # General figure properties
    _ax.legend()
    _ax.grid(color='gray', linestyle='--', linewidth=gline_width)
    _fig.tight_layout()
    # Output
    output_fig(dpath, f'{target}-scatter-grid')


def draw_scatter_paper_method(data: pd.DataFrame, dpath: str, target: str, use_norm: bool = False):
    """
    To illustrate method for paper OOPSLA'23. Figures with scatters and estimation lines.
    """
    _size = (4.5, 4.5)
    _alpha = 0.75
    _fig, _ax = plt.subplots(1, 1, figsize=_size)
    _prefix = ''
    _xlabel = 'Edge Coverage'
    _ylabel = 'Significance Score'
    if use_norm:
        _prefix = 'norm_'
        _xlabel = 'Normalized Edge Coverage'
        _ylabel = 'Normalized Significance Score'
        _ax.set_xlim([-0.1, 1.1])
        _ax.set_ylim([-0.1, 1.1])
    _ax.scatter(x=data[f'{_prefix}bitmap_size'],
                y=data[f'{_prefix}sig_score'],
                label='Seed', s=8, marker='o', alpha=_alpha, c='blue')
    # Draw OLS linear model
    _a, _b = np.polyfit(x=data[f'{_prefix}bitmap_size'], y=data[f'{_prefix}sig_score'], deg=1)
    _ols_model = _a * data[f'{_prefix}bitmap_size'] + _b
    _ax.plot(data[f'{_prefix}bitmap_size'], _ols_model, '-', color='black')
    # Draw y=ax
    _ave_a = data[f'{_prefix}sig_score'].mean() / data[f'{_prefix}bitmap_size'].mean()
    _model = _ave_a * data[f'{_prefix}bitmap_size']
    _ax.plot(data[f'{_prefix}bitmap_size'], _model, '-', color='red')
    # General figure properties
    _ax.set(xlabel=_xlabel, ylabel=_ylabel)
    _ax.legend()
    _ax.grid(color='gray', linestyle='--', linewidth=gline_width)
    _fig.tight_layout()
    # Output
    output_fig(dpath, f'{_prefix}{target}-scatter-line')


def draw_sig_score_cov_scatter_and_output(
        data: pd.DataFrame, dpath: str, name: str, use_ave_a: bool = False, use_norm: bool = False):
    _size = (4.5, 4.5)
    _alpha = 0.75
    _fig, _ax = plt.subplots(1, 1, figsize=_size)
    _prefix = ''
    _xlabel = 'Edge Coverage'
    _ylabel = 'Significance Score'
    if use_norm:
        _prefix = 'norm_'
        _xlabel = 'Normalized Edge Coverage'
        _ylabel = 'Normalized Significance Score'
    _favored_data = data[data['favored'] == 1]
    _unfavored_data = data[data['favored'] == 0]
    # Draw scatter and output.
    _ax.scatter(x=_favored_data[f'{_prefix}bitmap_size'],
                y=_favored_data[f'{_prefix}sig_score'],
                label='favored', s=8, marker='^', alpha=_alpha, c='red')
    _ax.scatter(x=_unfavored_data[f'{_prefix}bitmap_size'],
                y=_unfavored_data[f'{_prefix}sig_score'],
                label='unfavored', s=8, marker='o', alpha=_alpha, c='blue')
    # Draw estimation lines
    _a, _b = np.polyfit(x=data[f'{_prefix}bitmap_size'], y=data[f'{_prefix}sig_score'], deg=1)
    _sigscore_est = _a * data[f'{_prefix}bitmap_size'] + _b
    _ax.plot(data[f'{_prefix}bitmap_size'], _sigscore_est, '-', color='black')
    _ave_a = None
    _r2 = None
    if use_ave_a:
        _ave_a = data[f'{_prefix}sig_score'].mean() / data[f'{_prefix}bitmap_size'].mean()
        _sigscore_est = _ave_a * data[f'{_prefix}bitmap_size']
        _r2 = r2_score(y_true=data[f'{_prefix}sig_score'], y_pred=_sigscore_est)
        _ax.plot(data[f'{_prefix}bitmap_size'], _sigscore_est, '-', color='magenta')
    _ax.set(xlabel=_xlabel, ylabel=_ylabel)
    if use_norm:
        _ax.set_xlim([-0.1, 1.1])
        _ax.set_ylim([-0.1, 1.1])
    # Show labels
    _ax.legend()
    _fig.tight_layout()
    _ax.grid(color='gray', linestyle='--', linewidth=gline_width)
    output_fig(dpath, name)
    if use_ave_a:
        return _a, _b, _ave_a, _r2
    return _a, _b


def draw_sig_score_box_and_output(data: pd.DataFrame, dpath: str, name: str):
    plt.boxplot(x=data['norm_sig_score'].to_numpy(), labels=['norm_sig_score'])
    plt.axis('square')
    plt.ylabel('normalized_sig_score')
    plt.legend('', frameon=False)
    output_fig(dpath, name)


def draw_sig_score_violin_and_output(data: pd.DataFrame, dpath: str, name: str):
    fig, axis = plt.subplots(nrows=1, ncols=1)
    axis.violinplot(dataset=data['norm_sig_score'].to_numpy(),
                    showmeans=True, showmedians=False)
    axis.set_xticks([1], labels=['norm_sig_score'])
    axis.yaxis.grid(True)
    output_fig(dpath, name)


def output_fig(dpath: str, name: str):
    # Shrink plot
    plt.tight_layout()
    fig_path = os.path.join(dpath, f'{name}.pdf')
    plt.savefig(fig_path)
    print(f'Draw figure: {fig_path}')
    plt.clf()


def favored_est_analysis(
        data: pd.DataFrame, path: str, p_a: float, p_b: float = 0., use_norm: bool = False):
    _prefix = ''
    if use_norm:
        _prefix = 'norm_'
    data[f'est_{_prefix}sig_score'] = p_a * data[f'{_prefix}bitmap_size'] + p_b
    data['above_est'] = np.where(data[f'{_prefix}sig_score'] > data[f'est_{_prefix}sig_score'], True, False)
    _df = data[data['favored'] == 1]['above_est'].value_counts()
    _df = _df.rename({True: 'above_est', False: 'below_est'})
    print('Favor-Est')
    print(_df)
    _df.to_csv(path)
    print(f'Save favored est stats to `{path}`')