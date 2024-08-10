import os.path
import sys
import matplotlib
import matplotlib.pyplot as plt
# from venn import venn

import deduplicate
from deduplicate import parse_one_crash_log, crash_types

# To avoid type-3 font error
matplotlib.rcParams['pdf.fonttype'] = 42
matplotlib.rcParams['ps.fonttype'] = 42
plt.rcParams['font.size'] = 16

# fuzzers = deduplicate.fuzzers
targets = deduplicate.targets
# fuzzers = ['fun']
# targets = ['cxxfilt']
fuzzers = ['aflgo']


def write_to_file(file, content: str):
    file.write(f'{content}\n')


if __name__ == '__main__':
    # Parse arg
    if len(sys.argv) != 2:
        print('Usage: python3 <script> <repro_dir>')
        sys.exit(-1)
    repro_dir = os.path.abspath(sys.argv[1])
    result_path = os.path.join(repro_dir, 'crash-report.txt')
    if os.path.exists(result_path):
        os.remove(result_path)
    result_file = open(result_path, 'a')

    # Parse for each
    crash_dict = {}
    for fuzzer in fuzzers:
        crash_dict[fuzzer] = set()
        print('[LOG] =======================')
        print('[LOG]', fuzzer)
        print('[LOG] -----------------------')
        write_to_file(result_file, '===================================================')
        write_to_file(result_file, f'fuzzer: {fuzzer}')
        global_crash_num = 0
        for target in targets:
            print('[LOG]', target)
            write_to_file(result_file, '---------------------------------------------------')
            crash_log = os.path.join(repro_dir, fuzzer, target, 'repro-crash')
            if not os.path.exists(crash_log):
                write_to_file(result_file, f'Not find crash log: {crash_log}')
                print('[LOG]', f'Not find crash log: {crash_log}')
                continue
            unique_crashes = parse_one_crash_log(crash_log, target)
            if not len(unique_crashes):
                continue
            # Update global
            global_crash_num += len(unique_crashes)
            crash_dict[fuzzer] = crash_dict[fuzzer].union(set([f'{target}-{c}' for c in unique_crashes]))
            # Log in file
            write_to_file(result_file, f'target: {target}')
            # Statistics for each type
            count_dict = {}
            for crash_type in crash_types:
                count_dict[crash_type] = 0
            for crash in unique_crashes:
                crash_type = crash.split('>-<')[-1].replace('>', '')
                count_dict[crash_type] += 1
            write_to_file(result_file, '------------------------')
            write_to_file(result_file, '+++++ Crash Counts +++++')
            write_to_file(result_file, '------------------------')
            write_to_file(result_file, f'total: {len(unique_crashes)}')
            for crash_type in crash_types:
                if count_dict[crash_type] > 0:
                    write_to_file(result_file, f'{crash_type}: {count_dict[crash_type]}')
            # Details
            write_to_file(result_file, '-------------------------')
            write_to_file(result_file, '+++++ Crash Details +++++')
            write_to_file(result_file, '-------------------------')
            for crash in unique_crashes:
                write_to_file(result_file, crash)
        write_to_file(result_file, '-------------------------------')
        write_to_file(result_file, '+++++ Fuzzer Global Stats +++++')
        write_to_file(result_file, '-------------------------------')
        write_to_file(result_file, f'{fuzzer}-total: {global_crash_num}')
        write_to_file(result_file, f'set-size-total: {len(crash_dict[fuzzer])}')

    print('[LOG] =======================')
    print(f'[LOG] Finished parse repro data :-). Find result at {result_path}')
    # print('[LOG] going to raw venn plot...')
    # # Draw figure
    # # plt.rcParams['font.family'] = 'Monospace'
    # fig, ax = plt.subplots(nrows=1, ncols=1, figsize=(5.5, 5.5))
    # # First output
    # venn(data=crash_dict, ax=ax, legend_loc='best', fontsize=18)
    # plt.gca().get_legend().remove()
    # output_path = os.path.join(repro_dir, 'venn.pdf')
    # plt.savefig(output_path)
    # print('[LOG] Output to:', output_path)
