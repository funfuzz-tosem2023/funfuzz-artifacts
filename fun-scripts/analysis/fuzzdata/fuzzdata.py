import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.figure import Figure
from matplotlib.ticker import MultipleLocator, FormatStrFormatter


fuzzers = ['aflpp', 'fairfuzz', 'fun', 'fun-static']
targets = ['readpng', 'mjs', 'cxxfilt', 'nm-new', 'objdump', 'readelf',
           'djpeg', 'pngtest', 'tcpdump', 'mutool', 'xmllint']
fuzz_label = {
    'fun': 'FunFuzz',
    'fun-static': 'FunFuzz-static',
    'aflpp': 'AFL++',
    'fairfuzz': 'FairFuzz',
}
figsize = (5.0, 4.5)
shapes = {                                  # Shapes for lines in figures, each tuple is (<color>, <style>)
    'aflpp': ('#4169E1', (0, (1, 1))),               # RoyalBlue, Densely DashDotted
    'fairfuzz': ('#4EEE94', 'dashdot'),                 # Seagreen2, DashDot
    'fun': ('#FF3030', 'solid'),                   # Firebrick1, Solid
    'fun-static': ('#FFA500', 'dashed'),                  # Orange, Dashed
}
lab_map = {
    'time': 'Time (Hours)',
    'execution': '#Executions',
    'coverage': '#Edges',
    'crash': '#Crashes',
}

cline_width = 2.5                           # Line width for curve
plt.rcParams['font.family'] = 'Monospace'   # Set plot style. Use monospaced fonts
plt.rcParams['font.size'] = 16


def parse_x_data(df: pd.DataFrame, x_name: str):
    _X = None
    if x_name == 'time':
        _X = df.index / 3600  # Default in hours
    elif x_name == 'execution':
        _X = df['total_execs']
    return _X


def parse_y_data(df: pd.DataFrame, y_name: str):
    _Y = None
    if y_name == 'coverage':
        _Y = df['edges_found']
    elif y_name == 'crash':
        _Y = df['saved_crashes']
    return _Y


def draw_fuzz_plot(df_dict: dict, x_name: str = 'time', y_name: str = 'coverage') -> Figure:
    plt.clf()
    _fig, _ax = plt.subplots(1, 1, figsize=figsize)
    _y_min = 1000000000
    _y_max = 0
    _xy_dict = {}
    for _fuzzer in fuzzers:
        if _fuzzer not in df_dict:
            continue
        # Prepare data
        _X = parse_x_data(df_dict[_fuzzer], x_name)
        _Y = parse_y_data(df_dict[_fuzzer], y_name)
        _y_min = min(_y_min, _Y[_Y > 0].min())
        _y_max = max(_y_max, _Y.max())
        # if y_name == 'coverage':
        #     print(y_name, _y_min)
        # Add into xy dict. Later to replace 0 with global min value
        _xy_dict[_fuzzer] = (_X, _Y)
    for _fuzzer in _xy_dict:
        _X = _xy_dict[_fuzzer][0]
        _Y = _xy_dict[_fuzzer][1]
        # if y_name == 'coverage':
        #     print(_Y.replace(to_replace=0, value=_y_min))
        # Draw graph
        _ax.plot(_X, _Y.replace(to_replace=0, value=_y_min),
                 label=fuzz_label[_fuzzer], linewidth=cline_width,
                 color=shapes[_fuzzer][0], linestyle=shapes[_fuzzer][1])
    # Set axis
    _ax.set(xlabel=lab_map[x_name], ylabel=lab_map[y_name])
    _ax.legend(loc='lower right')
    if x_name == 'time':
        _ax.set_ylim([_y_min-50, _y_max+100])
        _x_major = MultipleLocator(4)
        _x_major_fmt = FormatStrFormatter('%d')
        _ax.xaxis.set_major_locator(_x_major)
        _ax.xaxis.set_major_formatter(_x_major_fmt)
    return _fig


def average_plot_data(outs_dir: str, delim: str = ', ', total_secs=86400):
    target_metrics = ['saved_crashes', 'saved_hangs', 'total_execs', 'edges_found']
    _pd_cnt = 0
    _sum_df = None
    for fn in os.listdir(outs_dir):
        out_dir = os.path.join(outs_dir, fn)
        if fn.startswith('.') or (not os.path.isdir(out_dir)):
            continue
        # Locate plot_data
        _pd_path = os.path.join(out_dir, 'default', 'plot_data')
        _df = pd.read_csv(_pd_path, index_col='# relative_time',
                          delimiter=delim, engine='python')[target_metrics]
        # Get relative end time point
        _end_tp = _df.index[-1]
        _all_tps = [_tp for _tp in range(_end_tp + 1)]
        # We fill up missing time point with the data of the last row.
        # Set the first row as all zeros.
        _last_row = np.zeros(len(_df.columns))
        # Create new data dict
        _new_data = []
        for _tp in range(total_secs + 1):
            if _tp in _df.index:
                # For existing tps, set to df data.
                _last_row = _df.loc[_tp].to_numpy()
            # For missing tps, set to last row
            _new_data.append(_last_row.tolist())
        _pd_df = pd.DataFrame(data=_new_data, columns=_df.columns)
        if _sum_df is None:
            _sum_df = _pd_df.copy()
        else:
            _sum_df += _pd_df.copy()
        _pd_cnt += 1
    _ave_df = _sum_df.copy() / _pd_cnt
    return _ave_df, _sum_df


def output_fig(figure: Figure, path: str, tight: bool = True):
    if tight:
        figure.tight_layout()
    figure.savefig(path)
    print('Output to:', path)
    plt.close()
