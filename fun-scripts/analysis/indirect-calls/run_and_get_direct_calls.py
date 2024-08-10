import os
import copy
import shutil
import argparse
import subprocess
import numpy as np
import pandas as pd

from tqdm import tqdm
from subprocess import DEVNULL
from funshm import *

"""
Start FUN_SHM, run the instrumented target, and parse
the triggered direct calls. All indirect calls can be
torn down into direct calls. Vice versa, direct calls
can be merged into indirect calls.
"""


DEFAULT_FUNC_NUM = 1 << 10

def run_target_fun(target_args: list, shmid: int, tmp_dir: str,
                   stdin=None, be_quiet: bool =False):
    _envs = {"__FUN_CC_SHM_ID": str(shmid), "FUN_DEBUG": "1", "AFL_FUN_TEMP": tmp_dir}
    if be_quiet:
        subprocess.run(target_args, env=_envs, stdin=stdin, stdout=DEVNULL, stderr=DEVNULL)
    else:
        print(LOG, 'Run target_args:', target_args)
        print(LOG, '+++++++++++++++ Program Outputs +++++++++++++++ ')
        subprocess.run(target_args, env=_envs, stdin=stdin)
        print(LOG, '+++++++++++++++++++++++++++++++++++++++++++++++ ')


def prepare_func_id_bimap(tmp_dir: str) -> tuple:
    """
    Parse funcInfo to build map between fname and fid.
    Return bimap and the number of functions (i.e., half
    of the length of the bimap).
    """
    _finfo_file = os.path.join(tmp_dir, 'funcInfo')
    _bimap = dict()
    with open(_finfo_file, 'r') as _f:
        for _ in _f.readlines():
            _parts = _.strip().split(',')
            _fname = _parts[0]
            _fid = int(_parts[1])
            _bimap[_fname] = _fid
            _bimap[_fid] = _fname
    return _bimap, int(len(_bimap) / 2)


def cal_cr_idx(len1d: int, fi: int, fj: int) -> int:
    """
    Calculate the index of a call relation CC[i][j], which
    means a call from the caller fi to the callee fj.
    """
    return fi * len1d + fj


def rev_caller_and_callee(idx: int, len1d: int) -> tuple:
    """
    Given the 1D length and CC 2D idx in 1D format, reverse
    the fid of the caller (fi) and the callee (fj).

    len1d = fnum + 1

    Suppose fnum = 500, fi = 1, len1d = 501, fj = 500,
    then, idx = fi * len1d + fj = 1 * 501 + 500 = 1001
    then, fi = idx / len1d = 1001 / 501 = 1
    then, fj = idx % len1d = 1001 % 501 = 500 

    """
    _fi = int(idx / len1d)
    _fj = int(idx % len1d)
    return _fi, _fj


def execute_cases_and_update_map(
        tmpdir: str,
        casedir: str, 
        cmd: list, 
        shmid: int, 
        ccshm,
        len1d: int = DEFAULT_FUNC_NUM,
        mapsize: int = DEFAULT_FUNC_NUM * DEFAULT_FUNC_NUM,
        use_stdin: bool = False,
        be_quiet: bool = False) -> np.array:
    """ 
    Execute every test cases inside the given casedir and return 
    the resultant toggle map.
    """
    # Prepare 
    _cc_matrix = np.zeros((len1d, len1d))
    # Execute test cases
    _case_cnt = 0
    _sorted_cases = sorted(os.listdir(casedir))
    for _ in tqdm(_sorted_cases, desc=f'{LOG} Processing {len(_sorted_cases)} test cases'):
        if _.startswith('.'):
            continue
        _path = os.path.join(casedir, _)
        if os.path.isdir(_path):
            raise RuntimeError('Cannot handle nested test case dir!')
        # Copy cmd
        _cmd = copy.deepcopy(cmd)
        # Judge type and run.
        if use_stdin:
            # use_stdin, use file instream as input.
            with open(_path, 'r') as _istream:
                run_target_fun(_cmd, shmid=shmid, stdin=_istream, 
                               be_quiet=be_quiet, tmp_dir=tmpdir)
        else:
            # use_file, replace @@ with the path to the file.            
            _idx = _cmd.index(FILEIN_LOC)
            _cmd[_idx] = _path
            run_target_fun(_cmd, shmid=shmid, be_quiet=be_quiet, tmp_dir=tmpdir)  
        # Count case
        _case_cnt += 1
    # Fill in the map after all cases are executed.
    for _idx in tqdm(range(mapsize), desc='[LOG] Turn resultant ccshm into matrix'):
        _fi, _fj = rev_caller_and_callee(_idx, len1d)
        if _fi == 0 or _fj == 0:
            # The first (0th) row are flags (not CC counts), skip them.
            # The first column is for nothing, skip it.
            continue
        # Found non-zero cc
        if ccshm[0][_idx]:
            _cc_matrix[_fi][_fj] = ccshm[0][_idx]
    return _cc_matrix, _case_cnt


def parse_indirect_calls(fmap: dict, cmatrix: np.array):
    """
    Parse indirect calls covered by the given set of test cases.
    The parsing should start from the main function and processed
    in a breadth first manner. An example is as follows:
    
    (How to deal with loops?)

    0. As for a C program, the entry point is always main(), so locate main() first.
    1. Start from fi and find a direct call fi -> fj at cmatrix[i][j].
    2. Start from fj and find another direct call fj -> fk, then we get a indirect 
       call fi -> fj -> fk; append fi -> fj -> fk to indirect call set (or just fi->fk?).
    3. Start from fk and back to Step-1.
    """



def build_arg_parser() -> argparse.ArgumentParser:
    """
    Build command line argument parser.
    :return: Arg parser instance.
    """
    _p = argparse.ArgumentParser()
    _p.add_argument('--in_dir', '-i', required=True, type=str,
                    help='Directory storing test cases.')
    _p.add_argument('--out_dir', '-o', required=True, type=str,
                    help='Directory to output toggle analysis results.')
    _p.add_argument('--tmp_dir', '-t', required=True, type=str,
                    help='Directory preserving fun temp files.')
    _p.add_argument('--quiet', '-q', required=False, action='store_true',
                    help='Whether hide target output.')
    return _p


def main(): 
    # Parse cmd.
    argv, target_cmd, use_stdin = parse_target_cmd()
    print(LOG, 'argv:', argv)
    print(LOG, 'target_cmd:', target_cmd)

    # Parse real args
    cmd_parser = build_arg_parser()
    args = cmd_parser.parse_args(argv)
    in_dir = os.path.abspath(args.in_dir)                                           # Folder put fuzzer-generated test inputs/cases.
    out_dir = os.path.join(os.path.abspath(args.out_dir), '__indirect_calls')       # Folder put script results.
    fun_tmp_dir = os.path.abspath(args.tmp_dir)                                     # Folder put funtmp files.    
    quiet = args.quiet
    fbimap, fnum = prepare_func_id_bimap(fun_tmp_dir)
    ccshmlen1d = fnum + 1               # We index function from 1 in the shm, so we plus 1 for each dimension of the CC matrix.
    map_size = ccshmlen1d * ccshmlen1d  # 2D for CC matrix
    print(LOG, 'fnum', fnum)
    print(LOG, 'ccshmlen1d', ccshmlen1d)
    print(LOG, 'map_size', map_size)


    # Load lots of shm functions from C library.
    c_shmget = load_c_shmget()
    c_shmctl = load_c_shmctl()
    c_shmat = load_c_shmat()
    c_shmdt = load_c_shmdt()

    # #####################
    # # Start core logics #
    # #####################

    # Load a shm. Take care of the size of the data type.
    shm_id = c_shmget(IPC_PRIVATE, map_size * sizeof(c_uint64), IPC_CREAT | IPC_EXCL | DEFAULT_PERMISSION)
    shm = load_shm(cshmat=c_shmat, shmid=shm_id, cdtype=c_uint64, shmlen=map_size)
    # print(shm[0][0])    # Read data from the shm like this.
    # for i in range(map_size):
    #     if shm[0][i]:
    #         print(shm[0][i])

    # Execute test cases and update global tog_map
    print(LOG, 'Execute testcases...')
    cc_matrix, num_case = execute_cases_and_update_map(
        casedir=in_dir, cmd=target_cmd, shmid=shm_id, ccshm=shm, len1d=ccshmlen1d,
        mapsize=map_size, use_stdin=use_stdin, be_quiet=quiet, tmpdir=fun_tmp_dir)

    # Free the shm
    c_shmdt(shm) 
    c_shmctl(shm_id, IPC_RMID, 0)

    # Log cc_matrix.
    # for i in range(1, ccshmlen1d):
    #     for j in range(1, ccshmlen1d):
    #         if cc_matrix[i][j]:
    #             print('[LOG]', f'{fbimap[i]}({i})', '->', f'{fbimap[j]}({j})', cc_matrix[i][j])

    # Parse indirect calls.

    # Write result to local.
    print(LOG, LOG_DELIM)
    if os.path.exists(out_dir):
        print(LOG, f"Out dir exists `{out_dir}`. We will recreate it.")
        shutil.rmtree(out_dir)
    os.makedirs(out_dir)

if __name__ == '__main__':   
    main()
    