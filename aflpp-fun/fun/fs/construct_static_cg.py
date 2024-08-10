import sys
from tqdm import tqdm

from common import *
from centrality import *

"""
Static Graph Construction (SGC) phase for aflpp-fun. 

Construct weighted call graph, compute function centrality values and preserve the call graph 
and values at temporary directory. The function centrality values computed here are used as 
initial values for the FS-based power scheduling. 
"""

if __name__ == '__main__':
    # Read in temp directory path from CLI
    temp_dir = os.path.abspath(sys.argv[1])

    # Prepare paths to input files
    func_info = os.path.join(temp_dir, FUNC_INFO)       # Function mapping file
    bb_calls = os.path.join(temp_dir, CALL_SITES)       # Call sites extracted by llvm pass

    # Prepare paths to output files
    cg_file = os.path.join(temp_dir, CALL_GRAPH)        # Graph for DCC
    dbg_cg_file = os.path.join(temp_dir, DEBUG_CG)      # Graph for debugging
    static_fs = os.path.join(temp_dir, STATIC_FS)       # Static centrality values as initial FS
    debug_fs = os.path.join(temp_dir, DEBUG_FS)         # More readable static FS info for debugging

    # Construct FuncName->FuncID mapping
    bi_fmap = build_bijective_fmap(path=func_info)
    fslog(f'fmap={bi_fmap}')

    # Construct adjacent matrix. Weights are the number of appearances
    func_num = int(len(bi_fmap)/2)
    len1d = func_num + 1
    cc = np.zeros((len1d, len1d))  # The numbers of static call sites
    with open(bb_calls, 'r') as f:
        for line in tqdm(f.readlines(), desc=f'{LOG_H_STD} Compute edge weights'):
            content = line.strip()
            if content == '':
                continue
            # Each line is <BBID,CallerName,CalleeName>, e.g., `xmllint.c:3177,main,usage`
            parts = content.split(',')
            caller_id = bi_fmap[parts[1]]
            callee_id = bi_fmap[parts[2]]
            cc[caller_id][callee_id] += 1   # Call relation counts
            cc[caller_id][0] += 1           # Caller counts

    # Build graph according to the matrix and preserve
    call_graph = nk.Graph(func_num, directed=True, weighted=True)
    fslog(f'Build call graph...')
    update_edge_weights(graph=call_graph, matrix=cc, len1d=len1d)

    fslog(f'Write call graph to `{cg_file}`')
    nk.writeGraph(G=call_graph, path=cg_file, fileformat=GRAPH_FORMAT)

    # Write dot graph for debugging
    fslog(f'Write debug call graph to `{dbg_cg_file}`')
    nk.writeGraph(G=call_graph, path=dbg_cg_file, fileformat=DBG_GRAPH_FORMAT)

    # Compute initial FS values as Katz centrality and preserve.
    katz = setup_katz_for(graph=call_graph)
    katz.run()

    # Block some functions. TODO: more functions to block?
    fs_vals = block_centrality(katz=katz, block_list=[bi_fmap['main']])

    # Save static fs to local
    fslog(f'Write static FS values to `{static_fs}`')
    np.savetxt(static_fs, X=fs_vals)

    # Debug FS
    # Normalize fs values
    norm_fs = fs_vals.copy()
    if np.min(norm_fs) == np.max(norm_fs):
        norm_fs = np.ones(norm_fs.size)
    else:
        norm_fs = (norm_fs - np.min(norm_fs)) / (np.max(katz.scores()) - np.min(norm_fs))
    # Create tuples and sort by norm_fs
    assert func_num == len(norm_fs), f'Unequal func_num ({func_num}) and fs_arr (len{len(norm_fs)})!'
    debug_data = []
    for i in range(len(norm_fs)):
        fid = i + 1
        debug_data.append((fid, bi_fmap[fid], norm_fs[i]))
    debug_data = sorted(debug_data, key=lambda x: x[2])
    # Write to file
    with open(debug_fs, 'w') as f:
        for tup in debug_data:
            # fid,fname,norm_fs
            f.write(f'{tup[0]},{tup[1]},{tup[2]}\n')
    fslog(f'Write debug FS info into `{debug_fs}`')
