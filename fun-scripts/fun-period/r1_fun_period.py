import os
import sys
import pandas as pd
import numpy as np
from tqdm import tqdm
from commons import periods


def cal_ave_execs(root_dir) -> dict:
    _ave_execs_dict = dict()
    for _fn in [f'period-{str(_)}s' for _ in periods]:
        _period_outs_dir = os.path.join(root_dir, _fn, 'mjs', 'outs')  # We only experiment on mjs for this response.
        _final_total_execs = list()
        _cnt = 1
        _execs_dict = dict()
        for _out_fn in tqdm(os.listdir(_period_outs_dir), desc=f'Extract final execs for {_fn}'):
            if not _out_fn.startswith('out-'):
                continue
            _plot_data = os.path.join(_period_outs_dir, _out_fn, 'default', 'plot_data')
            # print(_plot_data)
            _df = pd.read_csv(_plot_data, index_col=0, delimiter=', ', engine='python')
            _execs = _df['total_execs'].to_list()[-1]
            _final_total_execs.append(_execs)
            _execs_dict[f'out-{_cnt}'] = _execs
            _cnt += 1
        _execs_dict['ave_total_execs'] = np.array(_final_total_execs).mean()
        _ave_execs_dict[_fn] = _execs_dict
    return _ave_execs_dict


if __name__ == '__main__':
    data_dir = os.path.abspath(sys.argv[1])
    out_csv = os.path.join(data_dir, 'execs.csv')
    exec_dict = cal_ave_execs(data_dir)
    df = pd.DataFrame(data=exec_dict)
    print(df)
    df.to_csv(out_csv)
    print('[LOG] Write to:', out_csv)
