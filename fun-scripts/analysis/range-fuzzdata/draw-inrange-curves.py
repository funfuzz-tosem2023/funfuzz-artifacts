import os
import sys
import matplotlib
import matplotlib.pyplot as plt
import pandas as pd

from constants import *


# To avoid type-3 font error
matplotlib.rcParams['pdf.fonttype'] = 42
matplotlib.rcParams['ps.fonttype'] = 42
plt.rcParams['font.size'] = 16

if __name__ == '__main__':
    
    if len(sys.argv) != 2:
        print('Usage: <this_script> <bench_dir>')
        sys.exit(1)
    
    # Directory puts fuzz data
    bench_dir = os.path.abspath(sys.argv[1])

    # Directory output analysis results
    res_dir = os.path.join(bench_dir, '_results')
    if not os.path.exists(res_dir):
        raise RuntimeError(f'Cannot find _results dir in `{bench_dir}`. Cannot read figure data :-(')

    # Start to draw
    for target in targets:
        # Draw by target. Set style first
        fig, ax = plt.subplots(nrows=1, ncols=1, figsize=figsize)
        ax.set(xlabel='Time (Hour)', xticks=[_*4 for _ in range(7)],
               ylabel='#Edges')
        has_drawn = False
        # Each line is a fuzzer
        for fuzzer in fuzzers:
            print(f'{target} {fuzzer}')
            # Locate figure data csv
            fdata_csv = os.path.join(res_dir, f'{target}-{fuzzer}.csv')
            if not os.path.exists(fdata_csv):
                print(f'Cannot find `{fdata_csv}`, skip...')
                continue
            # Read in figure data, build map
            fdata_df = pd.read_csv(fdata_csv, index_col=0)
            # Drawing
            has_drawn = True
            color, linestyle = shapes[fuzzer]
            xs = fdata_df['time']/3600  # Time in hours
            # The mean coverage curve line
            ax.plot(xs, fdata_df['ave'],
                    label=fuzz_label[fuzzer], linewidth=cline_width,
                    color=color, linestyle=linestyle, alpha=0.7)
            # The in range filling
            ax.fill_between(xs, fdata_df['min'], fdata_df['max'],
                            alpha=0.3, color=color)
            ax.grid(color='gray', linestyle='--', linewidth=0.3)
            # print(fdata_df['min'])
        if has_drawn:
            fig.tight_layout()
            # plt.legend(loc='best')
            # plt.show()
            fig_dir = os.path.join(res_dir, '__figs')
            if not os.path.exists(fig_dir):
                os.mkdir(fig_dir)
            fig_path = os.path.join(fig_dir, f'{target}-covline.pdf')
            plt.savefig(fig_path)
            print(f'Output to: {fig_path}')
