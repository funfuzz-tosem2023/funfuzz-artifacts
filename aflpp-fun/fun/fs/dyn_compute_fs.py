import sys
import signal
import pandas as pd
from time import time
from datetime import timedelta
from ctypes import c_ulonglong, c_double

from cshm import *
from common import *
from centrality import *

"""
Dynamic Centrality Computation (DCC) phase for aflpp-fun.

This script reads call counts, i.e., weights for edges in the call graph, 
dynamically from cold cc_shm to update FS values on-the-fly. The updated 
FS values are passed to fuzzer into hot fs_shm. These FS values will 
support FS-based scheduling when the fs_shm are cooled down.
"""


def parse_shmid(idstr: str):
    """
    Read shm_ids passed from Fuzzer through stdin of this process. The shm_ids
    are passed in a line end with '\n' and the two ids for cc_shm are separated
    by ','. The format is <cc_id_rd>,<fs_id_wt>

    :return: cc_shm_id for reading, fs_shm_id for writing.
    """
    # sys.stdin is like scanf, which will wait util getting an input
    _id_strs = idstr.strip().split(',')
    return int(_id_strs[0]), int(_id_strs[1])


def sigterm_handler(_signo, _stack_frame):
    """
    Handle SIGTERM. Raises SystemExit(0):
    """
    sys.exit(0)


if __name__ == '__main__':

    # Whether print log to standard out?
    tostd = not not os.getenv(FUN_DEBUG_STD)

    # Prepare environments
    fun_temp_dir = os.path.abspath(sys.argv[1])
    fuzz_out_dir = os.path.abspath(sys.argv[2])

    # Prepare log file
    dcclog = os.path.join(fuzz_out_dir, FSLOG)
    dynamic_fs = os.path.join(fuzz_out_dir, DYNAMIC_FS)
    if not tostd:
        empty_logfile(dcclog)

    # Start DCC component!
    debug_fslog('Setup DCC component...', tostd, dcclog)
    start_tp = time()

    # Prepare FS computation materials
    cg_file = os.path.join(fun_temp_dir, CALL_GRAPH)
    func_info = os.path.join(fun_temp_dir, FUNC_INFO)
    debug_fslog('Prepare tempfiles, fun_temp_dir %s, cg_file %s, func_info %s, dcclog %s, dynamic_fs %s'
                % (fun_temp_dir, cg_file, func_info, dcclog, dynamic_fs), tostd, dcclog)

    # Prepare c functions
    c_shmat = load_c_shmat()
    debug_fslog('Load C shmat, c_shmat %s' % c_shmat, tostd, dcclog)

    # Load function number from funcInfo file and determine shm len
    bi_fmap = build_bijective_fmap(path=func_info)
    func_num = int(len(bi_fmap)/2)
    shm_len1d = func_num + 1
    shm_len2d = shm_len1d * shm_len1d
    debug_fslog('Load shm_len, shm_len1d %d, shm_len2d %d' %
                (shm_len1d, shm_len2d), tostd, dcclog)

    # Prepare block list
    block_list = [bi_fmap['main']]

    # Build up call graph skeleton and initialize katz
    debug_fslog('Read call graph skeleton from tmpdir', tostd, dcclog)
    call_graph = read_lfr_dgraph(gfile=cg_file, ncnt=func_num)
    katz = setup_katz_for(graph=call_graph)

    # -------------------------------- #
    #   Function Centrality Analysis   #
    # -------------------------------- #

    # Global matrix to accumulate call counts
    CC = np.zeros((shm_len1d, shm_len1d))

    debug_fslog('', tostd, dcclog)

    # To collect dynamic fs vals at each update
    dyn_fs_data = []

    # Register handler to process SIGTERM gracefully.
    signal.signal(signal.SIGTERM, sigterm_handler)

    try:
        # Infinite loop as a subprocess
        while True:
            debug_fslog('========== Function Centrality Analysis ==========', tostd, dcclog)

            # Continuously read shm_ids from stdin.
            line = sys.stdin.readline().strip()
            debug_fslog('Read line from the fuzzer, line `%s`' % line, tostd, dcclog)

            # Report time
            time_elapsed = time() - start_tp
            debug_fslog('Time elapsed since started - %s (HH:MM:SS)'
                        % timedelta(seconds=time_elapsed), tostd, dcclog)

            # Record time used by computing fs_vals
            last_comp_start_tp = time()

            # Parse shm_ids
            cc_id_rd, fs_id_wt = parse_shmid(line)
            debug_fslog('Get shm_id, cc_id_rd %d, fs_id_wt %d'
                        % (cc_id_rd, fs_id_wt), tostd, dcclog)

            # Load target shms
            cc_shm_rd = load_shm(c_shmat, c_ulonglong, cc_id_rd, shm_len2d)
            fs_shm_wt = load_shm(c_shmat, c_double, fs_id_wt, shm_len1d)
            debug_fslog('Load shm, cc_shm_rd %s, fs_shm_wt %s'
                        % (cc_shm_rd, fs_shm_wt), tostd, dcclog)

            # Read cc and update the global matrix CC
            debug_fslog('Update call counts...', tostd, dcclog)
            cc = np.array(read_cc_from_shm(shm=cc_shm_rd, shmlen1d=shm_len1d))

            # Sanitize: if global counter [0][0] is 0, jump out of the loop and kill this process.
            if cc[0][0] == 0:
                break

            # Update global CC
            CC += cc
            debug_fslog('Check read cc, cc[0][0] %d, CC[0][0] %d'
                        % (cc[0][0], CC[0][0]), tostd, dcclog)

            # Update edge weights, i.e., call probabilities among functions
            debug_fslog('Update call probabilities...', tostd, dcclog)
            update_edge_weights(graph=call_graph, matrix=CC, len1d=shm_len1d)

            # Self loops may come into existence after updating. Remove them, or
            # centrality analysis can be trapped in an infinite loop.
            debug_fslog('Remove %d self loops...' % call_graph.numberOfSelfLoops(),
                        tostd, dcclog)

            # Perform centrality analysis to update FS values
            debug_fslog('Perform centrality analysis with Katz...', tostd, dcclog)
            katz.run()

            # Block some functions
            debug_fslog('Block some functions...', tostd, dcclog)
            fs_vals = block_centrality(katz=katz, block_list=block_list)

            # Write FS values into fs_shm_wt
            debug_fslog('Write FS values into fs_shm_wt...', tostd, dcclog)
            write_fs_shm(vec=fs_vals, shm=fs_shm_wt, shmlen=shm_len1d)

            # Debug fs_update_flag
            debug_fslog('Check fs_shm update flag: %s' % fs_shm_wt[0][0], tostd, dcclog)

            # Update dynamic_fs to local
            debug_fslog('Record dynamic FS values.', tostd, dcclog)
            dyn_fs_data.append(np.append(fs_vals, time() - start_tp))

            # Record time used at this computation
            debug_fslog('Time used for computation: %f(s)'
                        % (time() - last_comp_start_tp), tostd, dcclog)

            # Mark a new iteration in logfile
            debug_fslog('', tostd, dcclog)

    finally:

        # ----------------------- #
        #   Preserve dynamic fs   #
        # ----------------------- #

        debug_fslog('Process SIGTERM gracefully...', tostd, dcclog)

        # Build table head: f1,f2,....,fn,time_elapsed
        table_head = [bi_fmap[i+1] for i in range(func_num)]
        table_head.append('time_elapsed')

        # Build dataframe
        fs_df = pd.DataFrame(data=dyn_fs_data, columns=table_head)

        # Write to local
        fs_df.to_csv(path_or_buf=dynamic_fs)
        debug_fslog('Write dynamic fs to `%s`' % dynamic_fs, tostd, dcclog)
