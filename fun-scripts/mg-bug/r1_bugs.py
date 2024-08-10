import sys
import os
import json


def load_json_dict(json_file: str) -> dict:
    with open(json_file, 'r') as _f:
        _res = json.load(_f)
    return _res['results']


def parse_triggerd_bugs(bug_sum_dict: dict) -> dict:
    _fuzzer_bugs_map = dict()
    for _fuzzer in bug_sum_dict:
        for _project in bug_sum_dict[_fuzzer]:
            for _target in bug_sum_dict[_fuzzer][_project]:
                for _trial in bug_sum_dict[_fuzzer][_project][_target]:
                    _trial_sum = bug_sum_dict[_fuzzer][_project][_target][_trial]
                    # print(_trial_sum)
                    if 'triggered' not in _trial_sum:
                        continue
                    # print(_trial_sum['triggered'])
                    _triggered_bugs = set(_trial_sum['triggered'].keys())
                    if _fuzzer not in _fuzzer_bugs_map:
                        _fuzzer_bugs_map[_fuzzer] = set()
                    _fuzzer_bugs_map[_fuzzer] = _fuzzer_bugs_map[_fuzzer].union(_triggered_bugs)
    return _fuzzer_bugs_map


def write_csv(bug_dict: dict, out_csv: str):
    fuzzers = ['funfuzz', 'aflplusplus', 'fairfuzz', 'aflgo', 'entropic', 'k_scheduler']
    with open(out_csv, 'w') as _f:
        _lines = ['\"fuzzer\",\"bugs\"']
        for _fuzzer in fuzzers:
            _bug_set = bug_dict[_fuzzer]
            _bug_data = ';'.join(list(_bug_set))
            _line = f'\"{_fuzzer}\",\"{_bug_data}\"'
            _lines.append(_line)
            # print(_line)
        _f.write('\n'.join(_lines))
    print('[LOG] Write to:', out_csv)


if __name__ == '__main__':
    # Locate raw files
    bug_dir = os.path.abspath(sys.argv[1])
    bug_summary = os.path.join(bug_dir, 'bug-summary.json')
    print(bug_summary)
    # Read the json into dict
    sum_dict = load_json_dict(bug_summary)
    # print(res, res.keys())
    bug_data = parse_triggerd_bugs(sum_dict)
    for fuzzer in bug_data:
        print(fuzzer, len(bug_data[fuzzer]))
    # Write to local
    output_file = os.path.join(bug_dir, 'bug.csv')
    write_csv(bug_data, output_file)
