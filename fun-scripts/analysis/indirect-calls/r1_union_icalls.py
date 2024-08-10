import os
import sys
import pandas as pd
import numpy as np

targets = ['cxxfilt', 'nm-new', 'objdump', 'readelf', 'djpeg',
           'readpng', 'mjs', 'mutool', 'tcpdump', 'xmllint']
fuzzers = ['fun', 'fun-static', 'aflpp', 'fairfuzz', 'aflgo']


def build_pool(cdict: dict) -> dict:
    _set = set()
    _pool = dict()
    for _fuzzer in cdict:
        _set = _set.union(cdict[_fuzzer])
    cnt = 1
    for _ in _set:
        _pool[_] = f"IC{cnt}"
        cnt += 1
    return _pool


def write_csv(bug_dict: dict, out_csv: str, crash_pool: dict):
    with open(out_csv, 'w') as _f:
        _lines = ['\"fuzzer\",\"icalls\",\"#icalls\"']
        for _fuzzer in fuzzers:
            _bug_set = bug_dict[_fuzzer]
            _bug_lst = [crash_pool[_] for _ in _bug_set]
            _bug_data = ';'.join(_bug_lst)
            _line = f'\"{_fuzzer}\",\"{_bug_data}\",\"{len(_bug_set)}\"'
            _lines.append(_line)
            # print(_line)
        _f.write('\n'.join(_lines))
    print('[LOG] Write to:', out_csv)


if __name__ == '__main__':
    data_dir = os.path.abspath(sys.argv[1])
    icall_set_dict = dict()
    icall_ave_dict = dict()
    icall_std_dict = dict()
    for fuzzer in fuzzers:
        dn = f'{fuzzer}-raw-outs'
        fuzzer_ave_dict = dict()
        fuzzer_std_dict = dict()
        icall_set = set()
        for target in targets:
            outs = os.path.join(data_dir, dn, target, 'outs')
            if not os.path.isdir(outs):
                print('[WARN] Skip as cannot find:', outs)
                fuzzer_ave_dict[target] = 0.0
                continue
            # Record for each target
            icall_list = []
            for fn in sorted(os.listdir(outs)):
                if not fn.startswith('out-'):
                    continue
                # Locate out content dir, maybe out-* or out-*/default
                out_dir = os.path.join(outs, fn, 'default')
                if not os.path.isdir(out_dir):
                    out_dir = os.path.join(outs, fn)
                # Locate indirect-calls.all and indirect-calls.csv
                icall_all = os.path.join(out_dir, 'indirect-calls.all')
                icall_csv = os.path.join(out_dir, 'indirect-calls.csv')
                # Read icalls seen at this trial.
                with open(icall_all, 'r') as f:
                    icall_out = set([f'{target}#{_.strip()}' for _ in f.readlines() if _.strip() != ''])
                icall_set = icall_set.union(icall_out)
                # Read final #icall
                icall_list.append(pd.read_csv(icall_csv)['num_icalls'].to_list()[-1])
            # Cal average.
            icall_arr = np.asarray(icall_list)
            fuzzer_ave_dict[target] = np.round(icall_arr.mean(), decimals=1)
            fuzzer_std_dict[target] = np.round(icall_arr.std(), decimals=1)
        # Bind to global
        icall_set_dict[fuzzer] = icall_set
        icall_ave_dict[fuzzer] = fuzzer_ave_dict
        icall_std_dict[fuzzer] = fuzzer_std_dict
    # Output exact icall csv for subsequent R analysis.
    r_csv = os.path.join(data_dir, 'all-indirect-calls.csv')
    icall_pool = build_pool(icall_set_dict)
    write_csv(icall_set_dict, r_csv, icall_pool)
    # Output final average data.
    ave_csv = os.path.join(data_dir, 'ave-indirect-calls.csv')
    df = pd.DataFrame(data=icall_ave_dict)
    df.to_csv(ave_csv)
    print('[LOG] Write to:', ave_csv)
    # Include standard deviations.
    # print(icall_std_dict)
    std_csv = os.path.join(data_dir, 'stats-indirect-calls.csv')
    std2_csv = os.path.join(data_dir, 'stats2-indirect-calls.csv')
    data_dict = dict()
    data_dict2 = dict()
    for fuzzer in icall_std_dict:
        inner_dict = dict()
        ave_dict = dict()
        std_tiny_dict = dict()
        for target in icall_std_dict[fuzzer]:
            ave = str(icall_ave_dict[fuzzer][target])
            std = str(icall_std_dict[fuzzer][target])
            std_tiny_str = '\\tiny{\\textpm' + std + '}'
            inner_dict[target] = ave + std_tiny_str
            ave_dict[target] = ave
            std_tiny_dict[target] = std_tiny_str
        data_dict[fuzzer] = inner_dict
        data_dict2[f'{fuzzer}-ave'] = ave_dict
        data_dict2[f'{fuzzer}-std'] = std_tiny_dict
    df = pd.DataFrame(data=data_dict)
    df.to_csv(std_csv)
    df2 = pd.DataFrame(data=data_dict2)
    print(df2)
    df2.to_csv(std2_csv)
    print('[LOG] Write to:', std_csv)
    print('[LOG] Write to:', std2_csv)
