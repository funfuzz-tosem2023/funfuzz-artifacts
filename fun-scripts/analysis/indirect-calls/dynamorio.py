import subprocess
import os
import pandas as pd

"""
Lib for reproducing test cases with DynamoRIO-libinstrcalls.so.
"""

LOG = '[LOG]'
ICALL_TEMP = 'indirect.calls'
RAW_LOG = 'raw_log'
ID_LOG = 'id_log'
TIME_LOG = 'time_log'


def run_cmd(args_list: list,
            log_dir: str,
            dynamorio_libdir: str,
            timeout=None,
            stdin=None):
    _envs = {'LOG_DIR': log_dir,
             'LD_LIBRARY_PATH': dynamorio_libdir}
    print(LOG, '+++++++++++++++ Program Outputs +++++++++++++++ ')
    if timeout == None:
        print('[LOG]', args_list)
        if stdin is None:
            subprocess.run(args_list, env=_envs)
        else:
            subprocess.run(args_list, stdin=stdin, env=_envs)
    else:
        timeout = int(timeout)
        print('[LOG]', args_list, f'timeout={timeout}s')
        # Catch the timeout
        try:
            if stdin is None:
                subprocess.run(args_list, timeout=timeout, env=_envs)
            else:
                subprocess.run(args_list, stdin=stdin, timeout=timeout, env=_envs)
        except subprocess.TimeoutExpired:
            print(f"[LOG] An execution exceeding {timeout} seconds.")
    print(LOG, '+++++++++++++++++++++++++++++++++++++++++++++++ ')


def run_one_test_case(dynamorio_home: str, dynamorio_client: str, log_dir: str, in_type: str,
                      target_path: str, target_opts: str, case_path: str, timeout: int = 2):
    # Locate dynamorio stuffs.
    _drrun_bin = os.path.join(dynamorio_home, 'bin64', 'drrun')
    _dyn_libdir = os.path.join(dynamorio_home, 'lib64', 'release')
    # Assemble command and run.
    _cmd = [_drrun_bin, '-root', dynamorio_home, '-c', dynamorio_client, '--', target_path]
    if target_opts != '':
        _cmd.extend(target_opts.split(' '))
    if in_type == 'file':
        _cmd.append(case_path)
        run_cmd(args_list=_cmd, log_dir=log_dir, dynamorio_libdir=_dyn_libdir, timeout=timeout)
    elif in_type == 'stdin':
        with open(case_path, 'r') as _istream:
            run_cmd(args_list=_cmd, log_dir=log_dir, stdin=_istream, dynamorio_libdir=_dyn_libdir, timeout=timeout)
    else:
        raise RuntimeError('[ERROR] Unsupported input type:', in_type)


def rm_runtime_address(line: str):
    """
    Helper function for extract_indirect_calls_from_log()
    """
    # Remove the '0x00007f49ce645493' from "CALL INDIRECT @  0x00007f49ce645493 libc.so.6!__run_exit_handlers+0x103 ./stdlib/exit.c:113+0x5"
    # Remove the '0x00007f4bcf761040' from "to  0x00007f4bcf761040 ld-linux-x86-64.so.2!_dl_fini+0x0 ./elf/dl-fini.c:31+0x0"
    _preserve_parts = []
    _has_dropped = 0
    for _ in line.split():
        _ = _.strip()
        if _ == '':
            continue
        if _has_dropped or not _.startswith('0x'):
            _preserve_parts.append(_)
    # return ' '.join(_preserve_parts)
    return _preserve_parts


def extract_indirect_calls_from_log(logfile: str) -> set:
    """
    Read in the dynamorio log file, extract the covered indirect calls
    from the log, and remove execution-specific information (e.g., the
    instruction addresses.)
    """
    _find_indirect = 0
    _indirect_calls = []
    with open(logfile, 'r') as _f:
        _call_parts = []
        for _ in _f.readlines():
            if _.startswith('CALL INDIRECT @'):
                _find_indirect = 1
                # Make up an intact call and append it to the list
                _indirect_calls.append(' '.join(_call_parts))
                _call_parts = []
            elif _.startswith('CALL @') or _.startswith('RETURN @'):
                _find_indirect = 0
            if _find_indirect:
                _call_parts.extend(rm_runtime_address(_))
    _indirect_calls = [_.strip() for _ in _indirect_calls if _.strip() != '']
    print('len_lst', len(_indirect_calls), 'len_set', len(set(_indirect_calls)))
    return set(_indirect_calls)


def write_lines_into_file(lines, out_file: str):
    with open(out_file, 'w') as _f:
        _f.write('\n'.join(list(lines)))


def parse_one_log(log_file: str, out_file: str):
    _indirect_calls = extract_indirect_calls_from_log(log_file)
    write_lines_into_file(_indirect_calls, out_file)
    print(LOG, 'Write minimized indirect calls to:', out_file)


def merge_logs(log_list: list) -> set:
    """
    Read indirect calls from given list of logs, merge them
    and return the resultant set.
    """
    _indirect_calls = set()
    for _log in log_list:
        with open(_log, 'r') as _f:
            _indirect_calls = _indirect_calls.union(set([_.strip() for _ in _f.readlines() if _.strip() != '']))
    return _indirect_calls


def parse_afl_caseid(case_name: str):
    # id:007855,src:007834,time:82752152,execs:92063255,op:havoc,rep:16
    return case_name.split(',')[0].split(':')[1]


def run_and_parse_afl_cases(dynamorio_home: str, dynamorio_client: str,
                            out_dir: str, tmp_dir: str, in_type: str, target_path: str,
                            target_opts: str, case_dir: str, timeout: int = 2):
    """
    Reproduce all the afl-style test cases under the give case dir.
    @param tmp_dir: Put temporary files like log_dirs and single log parsing results.
    """
    # Record the process of repro
    _repro_log = os.path.join(out_dir, 'drrun-repro.log')
    # Start repro
    for _case in sorted(os.listdir(case_dir)):
        _case_path = os.path.join(case_dir, _case)
        if not _case.startswith('id') or os.path.isdir(_case_path):
            continue
        # Prepare
        _caseid = str(int(parse_afl_caseid(case_name=_case)))
        _logdir = os.path.join(tmp_dir, RAW_LOG, _caseid)
        _parse_result = os.path.join(tmp_dir, ID_LOG, f'{_caseid}.{ICALL_TEMP}')
        os.mkdir(_logdir)
        # Run and collect raw indirect calls.
        run_one_test_case(dynamorio_home=dynamorio_home,
                          dynamorio_client=dynamorio_client,
                          log_dir=_logdir,
                          in_type=in_type,
                          target_path=target_path,
                          target_opts=target_opts,
                          case_path=_case_path,
                          timeout=timeout)
        # Locate the generated log and parse it.
        if len(os.listdir(_logdir)) < 1:
            with open(_repro_log, 'a') as _f:
                _f.write(f'Find no drrun log for test case: {_case_path}\n')
        else:
            # Normally, there will be only one file under the log dir.
            _raw_log = os.path.join(_logdir, os.listdir(_logdir)[0])
            parse_one_log(log_file=_raw_log, out_file=_parse_result)


def merge_afl_logs_by_time(afltype: str, plot_data: str, tmp_dir: str,
                           tgap: int = 900, tupper: int = 86400):
    # Calculate sampled time points.
    _time_points = [_ for _ in range(0, tupper + 1, tgap)]
    # Sanitize
    if not (afltype == 'aflpp' or afltype == 'afl'):
        raise RuntimeError('Unsupported type:', afltype)
    # Read in plot_ata
    _df = pd.read_csv(plot_data, index_col=0, delimiter=', ', engine='python')
    if afltype == 'afl':
        # Adjust df to align with aflpp style
        _df['corpus_count'] = _df['paths_total']
        # Reset index as relative time
        _new_index = _df.index.to_numpy() - _df.index[0]
        _df = _df.set_index(_new_index)
    # Find the largest id at certain time points
    _id_tuples = []
    for _tp in _time_points:
        _col = None
        if _tp == 0:
            # Special case. Use first coverage (or maybe 0) as the coverage at the time point 0.
            _col = _df.iloc[0]
            # _col = pd.Series(dict(edges_found=0, total_execs=0))
        elif _tp in _df.index:
            # Use the row if this tp exists
            _col = _df.loc[_tp]
        else:
            # Find the closest time point
            _tmp = _tp
            while _tmp and _tmp not in _df.index:
                _tmp -= 1
            # Sanitize check!
            if _tmp == 0:
                # raise RuntimeError('Find closest time point failed!: ' + plot_data)
                return []  # Just skip
            _col = _df.loc[_tmp]
        # The largest input id is the number of corpus count -1
        _id_tuples.append((_tp, _col['corpus_count']))
    print(_id_tuples)
    # Merge id logs into tp logs
    _timelog_dir = os.path.join(tmp_dir, TIME_LOG)
    _idlog_dir = os.path.join(tmp_dir, ID_LOG)
    _tp_last = -1
    _tid_max_last = -1
    for _tp, _tid_max in _id_tuples:
        # Locate tp log that going to out.
        _tp_log = os.path.join(_timelog_dir, f'{ICALL_TEMP}.{str(_tp)}')
        # Locate the list of .profraw files with the _tid_max
        if _tp == 0:
            _relevant_idlogs = [os.path.join(_idlog_dir, f'{_}.{ICALL_TEMP}') for _ in range(_tid_max)
                                if os.path.exists(os.path.join(_idlog_dir, f'{_}.{ICALL_TEMP}'))]
        else:
            _relevant_idlogs = [os.path.join(_idlog_dir, f'{_}.{ICALL_TEMP}') for _ in range(_tid_max_last, _tid_max)
                                if os.path.exists(os.path.join(_idlog_dir, f'{_}.{ICALL_TEMP}'))]
            _tplog_last = os.path.join(_timelog_dir, f'{ICALL_TEMP}.{str(_tp_last)}')
            _relevant_idlogs.append(_tplog_last)
        print(_relevant_idlogs)
        # Merge the logs and write to file
        _call_set = merge_logs(_relevant_idlogs)
        write_lines_into_file(_call_set, _tp_log)
        print(LOG, 'Write indirect calls to:', _tp_log)
        # Mark last tp
        _tp_last = _tp
        _tid_max_last = _tid_max


def gather_time_logs(out_dir: str, tmp_dir: str, tupper: int = 86400, tgap: int = 900):
    # Locate time log dir.
    _timelog_dir = os.path.join(tmp_dir, TIME_LOG)
    # Record data
    _data_dict = dict()
    _idx = 1
    _all_icalls = set()
    # Calculate sampled time points.
    _time_points = [_ for _ in range(0, tupper + 1, tgap)]
    for _tp in _time_points:
        # Locate time log
        _log = os.path.join(_timelog_dir, f'{ICALL_TEMP}.{_tp}')
        with open(_log, 'r') as _f:
            _icalls = [_.strip() for _ in _f.readlines() if _.strip() != '']
        _icall_set_tp = set(_icalls)
        _all_icalls = _all_icalls.union(_icall_set_tp)
        _data_dict[_idx] = dict(time=_tp, num_icalls=len(_icall_set_tp))
        _idx += 1
    # Write to local.
    _out_csv = os.path.join(out_dir, 'indirect-calls.csv')
    _df = pd.DataFrame(data=_data_dict)
    _df.T.to_csv(_out_csv)
    # print(_data_dict)
    print(_df)
    print(LOG, 'Write numbers of indirect calls to:', _out_csv)
    _out_calls = os.path.join(out_dir, 'indirect-calls.all')
    write_lines_into_file(lines=sorted(list(_all_icalls)), out_file=_out_calls)
    print(LOG, 'Write final indirect calls to:', _out_calls)
