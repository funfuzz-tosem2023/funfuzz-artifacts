import os
import sys


def extract_detailed_crash_info_easy(crash_summary: str) -> dict:
    _crash_dict = dict()
    with open(crash_summary, 'r') as _f:
        _crashes = set()
        _target = ''
        _fuzzer = ''
        _first_target = True
        for _ in _f.readlines():
            if _.startswith('fuzzer: '):
                if not _first_target:
                    _crash_dict[_fuzzer] = _crashes
                    _crashes = set()
                else:
                    _first_target = False
                _fuzzer = _.strip().replace('fuzzer: ', '')
            elif _.startswith('target: '):
                _target = _.strip().replace('target: ', '')
            elif _.startswith('<'):
                _crash_line = f'{_target}:{_.strip()}'
                _crashes.add(_crash_line)
                # _crashes.add(str(hash(_crash_line)))
        # Deal with the last fuzzer.
        if not _first_target:
            _crash_dict[_fuzzer] = _crashes
            _crashes = set()
    return _crash_dict


def build_crash_pool(cdict: dict) -> dict:
    _crash_set = set()
    _crash_pool = dict()
    for _fuzzer in cdict:
        _crash_set = _crash_set.union(cdict[_fuzzer])
    cnt = 1
    for _crash in _crash_set:
        _crash_pool[_crash] = f"C{cnt}"
        cnt += 1
    return _crash_pool


def write_csv(bug_dict: dict, out_csv: str, crash_pool: dict):
    fuzzers = ['fun', 'fun-static', 'aflpp', 'fairfuzz', 'aflgo']
    with open(out_csv, 'w') as _f:
        _lines = ['\"fuzzer\",\"bugs\"']
        for _fuzzer in fuzzers:
            _bug_set = bug_dict[_fuzzer]
            _bug_lst = [crash_pool[_] for _ in _bug_set]
            _bug_data = ';'.join(_bug_lst)
            _line = f'\"{_fuzzer}\",\"{_bug_data}\"'
            _lines.append(_line)
            # print(_line)
        _f.write('\n'.join(_lines))
    print('[LOG] Write to:', out_csv)


if __name__ == '__main__':
    # Locate raw files
    crash_dir = os.path.abspath(sys.argv[1])
    crash_data_old = os.path.join(crash_dir, 'crash-report-noaflgo.txt')
    crash_data_aflgo = os.path.join(crash_dir, 'crash-report-aflgo.txt')
    # Parse into set
    crash_dict = extract_detailed_crash_info_easy(crash_data_old)
    crash_dict_aflgo = extract_detailed_crash_info_easy(crash_data_aflgo)
    crash_dict.update(crash_dict_aflgo)
    for fuzzer in crash_dict:
        print(fuzzer, len(crash_dict[fuzzer]))
    # Build bug pool.
    pool = build_crash_pool(crash_dict)
    print(pool)
    # Write to local
    output_file = os.path.join(crash_dir, 'crash.csv')
    write_csv(crash_dict, output_file, pool)
