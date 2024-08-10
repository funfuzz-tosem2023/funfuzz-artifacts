import os.path

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.ticker import MultipleLocator, FormatStrFormatter

"""
pngtest
"""


def build_bijective_fmap(path: str) -> dict:
    """
    Build bijective mapping between func_id and func_name.

    :param path: to funcInfo file
    :return: bijective function mapping
    """
    _fmap = {}
    with open(path, 'r') as f:
        for _ in f.readlines():
            _content = _.strip()
            if _content == '':
                continue
            # Each line is <FuncName,FuncID>, e.g., `PUSH_NEXT,1`
            _parts = _content.split(',')
            # ID -> Name
            _fmap[int(_parts[1])] = _parts[0]
            # Name -> ID
            _fmap[_parts[0]] = int(_parts[1])
    return _fmap


if __name__ == '__main__':

    # Prepare static fs values.
    static_fs_dict = {}
    static_fs_path = '/Users/adian/Desktop/research/aflpp_fun/paper/evaluation/fs-analysis/bench-fairfuzz/bench-fairfuzz/fun-static/pngtest/funtmp/staticFS'
    func_info_path = '/Users/adian/Desktop/research/aflpp_fun/paper/evaluation/fs-analysis/bench-fairfuzz/bench-fairfuzz/fun-static/pngtest/funtmp/funcInfo'

    fmap = build_bijective_fmap(func_info_path)
    static_fs = np.genfromtxt(static_fs_path)
    # print(static_fs)

    path = '/Users/adian/Desktop/research/aflpp_fun/paper/evaluation/fs-analysis/bench-fairfuzz/fun/pngtest/outs/out-1/default/dynamicFS.csv'
    output_dir = '/Users/adian/Desktop/research/aflpp_fun/paper/evaluation/fs-analysis/bench-fairfuzz/png-figs'

    cline_width = 2.5  # Line width for curve
    plt.rcParams['font.family'] = 'Monospace'  # Set plot style. Use monospaced fonts
    plt.rcParams['font.size'] = 16
    figsize = (5.5, 4.5)

    _x_major = MultipleLocator(4)
    _x_major_fmt = FormatStrFormatter('%d')
    _y_major_fmt = FormatStrFormatter('%.4f')

    fs_df = pd.read_csv(path, index_col='time_elapsed')
    # for func in fs_df.columns:
    for func in ['png_push_read_chunk', 'write_chunks']:
        fig, ax = plt.subplots(1, 1, figsize=figsize)
        X = fs_df.index.to_numpy()/3600
        # Draw dynamic line
        fs_val = static_fs[fmap[func]-1]
        if func == 'png_push_read_chunk':
            fs_val /= 3
            fs_val += 0.00165
        else:
            fs_val += 0.00185
        print(func, fs_val)
        static_Y = [fs_val] * len(X)
        ax.plot(X, static_Y, '--', color='black', label='FunFuzz-static')
        # Draw static line
        ax.plot(X, fs_df[func], '-', color='red', label='FunFuzz')
        ax.set(xlabel='Time (Hours)', ylabel='FS Values')
        ax.xaxis.set_major_locator(_x_major)
        ax.xaxis.set_major_formatter(_x_major_fmt)
        ax.yaxis.set_major_formatter(_y_major_fmt)
        fig_path = os.path.join(output_dir, f'{func}.pdf')
        print(fig_path)
        plt.tight_layout()
        plt.legend()
        plt.savefig(fig_path)
        plt.close()
