import os
import sys
import numpy as np
import pandas as pd
import matplotlib
import matplotlib.pyplot as plt

# Parse f3, f4
target_funcs = [
    'parse_block_or_stmt', 'mjs_bcode_insert_offset'
]

# To avoid type-3 font error
matplotlib.rcParams['pdf.fonttype'] = 42
matplotlib.rcParams['ps.fonttype'] = 42
plt.rcParams['font.size'] = 16


def min_max_norm(min_val, max_val, val):
    return (val - min_val) / (max_val - min_val)


def parse_static_fs(fs_file: str) -> dict:
    _max_fs = 0
    _min_fs = 99999999999999999
    # Record target normalized fs
    _target_fs_dict = {}
    with open(fs_file, 'r') as f:
        for line in f.readlines():
            _parts = line.split(',')
            _func_name = _parts[1]
            if _func_name == 'main' or _func_name == 'mjs_execute':
                continue
            _fs = float(_parts[-1])
            _max_fs = max(_fs, _max_fs)
            _min_fs = min(_fs, _min_fs)
            if _func_name in target_funcs:
                _target_fs_dict[_func_name] = _fs
    # Normalized
    for _k in _target_fs_dict:
        _target_fs_dict[_k] = min_max_norm(
            min_val=_min_fs, max_val=_max_fs, val=_target_fs_dict[_k])
    return _target_fs_dict


def parse_norm_for_each_row(all_data: np.ndarray, func_data: np.ndarray) -> np.ndarray:
    assert len(all_data) == len(func_data), 'Unequivalent data!'
    _norm_vals = []
    for _idx in range(len(all_data)):
        _row = all_data[_idx]
        _norm_val = min_max_norm(
            min_val=_row.min(), max_val=_row.max(), val=func_data[_idx])
        _norm_vals.append(_norm_val)
    return np.array(_norm_vals)


def draw_fs_curve(
        X: np.ndarray,
        static_val: float,
        dynamic_vals: np.ndarray,
        upper_time: int = 86400):
    if upper_time > 86400 or upper_time <= 0:
        raise RuntimeError(f'Invalid upper_time ({upper_time})!')
    elif upper_time < 86400:
        # Locate the index
        _upper_idx = -1
        for _idx in range(len(X)):
            _tp = X[_idx]
            if _tp >= upper_time:
                break
            _upper_idx = _idx
        # Splice data
        X = X[:_upper_idx]
        dynamic_vals = dynamic_vals[:_upper_idx]
    _figsize = (5, 4.5)
    _fig, _ax = plt.subplots(1, 1, figsize=_figsize)
    # Draw dynamic
    _ax.plot(X, dynamic_vals, color='red')
    # Draw static
    _ax.plot(X, [static_val]*len(dynamic_vals), color='black')
    # Set xticks and yticks
    # _ax.set_xlim(left=0, right=upper_time)
    # _ax.set(xlabel='Time (Seconds)', ylabel='Normalized FS Values', yticks=[_*0.05 for _ in range(10)])
    _ax.set(xlabel='Time (Seconds)', ylabel='Normalized FS Values', yticks=[_*0.1 for _ in range(6)])
    _ax.grid(color='gray', linestyle='--', linewidth=0.3)
    _fig.tight_layout()


if __name__ == '__main__':
    if len(sys.argv) != 2:
        print('Usage: python3 <script> <fs_dir>')
        sys.exit(-1)

    # Parse args
    fs_dir = os.path.abspath(sys.argv[1])

    # Locate static and dynamic fs
    sta_fs_file = os.path.join(fs_dir, 'debugFS')
    dyn_fs_file = os.path.join(fs_dir, 'dynamicFS.csv')

    # Parse normalized static FS for target functions
    norm_sta_fs_dict = parse_static_fs(fs_file=sta_fs_file)

    # Parse normalized dynamic FS vals
    df = pd.read_csv(dyn_fs_file, index_col=0)
    tp_X = df['time_elapsed'].to_numpy()
    fs_df = df.copy().drop('time_elapsed', axis=1)
    norm_dyn_fs_dict = {}
    for func in target_funcs:
        norm_dyn_fs_dict[func] = parse_norm_for_each_row(
            all_data=fs_df.to_numpy(), func_data=df[func].to_numpy())
    print(norm_sta_fs_dict)
    print(norm_dyn_fs_dict)

    # Draw plots
    for func in target_funcs:
        # Draw the first 10 minutes
        draw_fs_curve(X=tp_X, static_val=norm_sta_fs_dict[func],
                      dynamic_vals=norm_dyn_fs_dict[func], upper_time=600)
        # Output figure
        fig_path = os.path.join(fs_dir, f'fs-{func}.pdf')
        plt.savefig(fig_path)
        print('Output to:', fig_path)
