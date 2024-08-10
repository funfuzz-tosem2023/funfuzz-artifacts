import networkit as nk
import numpy as np
from networkit.centrality import KatzCentrality

"""
Constants and utilities for function centrality analysis
"""


# ------------- #
#   Constants   #
# ------------- #


# Graph format.
GRAPH_FORMAT = nk.Format.LFR
DBG_GRAPH_FORMAT = nk.Format.DOT

# ------------- #
#   Utilities   #
# ------------- #


def build_bijective_fmap(path: str) -> dict:
    """
    Build bijective mapping between func_id and func_name.

    :param path: to funcInfo file
    :return: bijective function mapping
    """
    _fmap = {}
    with open(path, 'r') as f:
        for _ in f.readlines():
            _content = _.strip()
            if _content == '':
                continue
            # Each line is <FuncName,FuncID>, e.g., `PUSH_NEXT,1`
            _parts = _content.split(',')
            # ID -> Name
            _fmap[int(_parts[1])] = _parts[0]
            # Name -> ID
            _fmap[_parts[0]] = int(_parts[1])
    return _fmap


def setup_katz_for(graph: nk.Graph):
    return KatzCentrality(G=graph)


def block_centrality(katz: KatzCentrality, block_list: list) -> np.ndarray:
    """
    Blocking some functions (usually common functions like `main()`).
    By 'blocking' we refer to setting fs values to 0.

    :param katz: A KatzCentrality instance
    :param block_list: list of ids of the function we want to block
    :return: blocked fs vals wrapped as numpy array
    """
    _fs_vals = np.array(katz.scores())
    for _fid in block_list:
        # Shift
        _nid = _fid - 1
        # Block
        _fs_vals[_nid] = 0
    return _fs_vals


def read_lfr_dgraph(gfile: str, ncnt: int, with_weight: bool = False) -> nk.Graph:
    """
    Since networkit can only read undirected graph, we provide this
    utility to maintain the directness of call graph. Note that nodes
    are indexed from 1 in LFR file, so we need to shift by `-1` before
    add an edge.

    :param gfile: path to graph file
    :param ncnt: number of nodes, i.e., func_num
    :param with_weight: whether read the weight, default is `False`
    :return: A directed graph built from LFR file
    """
    _g = nk.Graph(ncnt, directed=True, weighted=True)
    with open(gfile, 'r') as _f:
        for _line in _f:
            _edge_info = _line.strip()
            if _edge_info == '':
                continue
            # Compute node id
            _parts = _edge_info.split()
            _u = int(_parts[0]) - 1
            _v = int(_parts[1]) - 1
            if with_weight:
                _w = float(_parts[2])
                _g.addEdge(_u, _v, _w)
            else:
                _g.addEdge(_u, _v)
    return _g


def update_edge_weights(graph: nk.Graph, matrix, len1d: int):
    """
    Update weights for edges in the call graph. The weights represent call
    probabilities between functions. Essentially, the call probability cp
    between two functions f1 and f2 are computed as:

        cp = cnt(f1, f2) / cnt(f1)

    where cnt(f1, f2) is the number of times f2 called by f2 and cnt(f1)
    the number of times f1 performs as caller. Note that we use a reversed
    call graph to make sure significance can flow to central functions.
    For example, for a call relation f1->f2, we add a reversed directed edge
    f2->f1 into graph. We reward functions connected to seldom functions by
    setting edge weights w as complimentary call probability, that is:

        w = 1 - cp

    :param graph: the (reversed) call graph
    :param matrix: the (n*n) matrix of call counts
    :param len1d: the 1D length of the matrix that essentially equals to
              func_num+1, or node_num+1
    """
    # Sanitize: len1d == node_num + 1
    if len1d != graph.numberOfNodes() + 1:
        raise RuntimeError(f'len1d({len1d}) != node_num({graph.numberOfNodes()})+1')
    # We index function from 1
    smallest_w = np.finfo(float).eps
    for _caller in range(1, len1d):
        for _callee in range(1, len1d):
            # We index function from 1, while networkit indexes nodes from 0.
            # Therefore, we need to shift function ids a bit to match node ids.
            # Note that the call graph we use is reversed.
            _nid_caller = _caller - 1
            _nid_callee = _callee - 1
            # Deal with cases that `cc == 0`.
            if matrix[_caller][_callee] == 0:
                if graph.hasEdge(_nid_callee, _nid_caller):
                    # (reversed) Although this call relation has not occurred so
                    # far, it exactly exists, so we set it to smallest_w.
                    graph.setWeight(u=_nid_callee, v=_nid_caller, w=smallest_w)
                # If matrix[_caller][0] == 0, that means id _caller has never
                # performs as a caller thus we just skip it (do nothing).
            else:
                if matrix[_caller][0] == 0:
                    raise RuntimeError(f'Divided by zero when computing cp, '
                                       f'matrix[{_caller}][{_callee}] {matrix[_caller][_callee]}, '
                                       f'matrix[{_caller}][0] {matrix[_caller][0]}')
                # We store caller cnt at cc_shm[callerID*shmLen1D], which equals
                # to cc_shm[0][callerID] in 2D view.
                _cp = matrix[_caller][_callee] / matrix[_caller][0]
                # (reversed) This operation may create new edges, which matches
                # intuition that "a new call relation is found at runtime".
                graph.setWeight(u=_nid_callee, v=_nid_caller, w=1-_cp+smallest_w)
