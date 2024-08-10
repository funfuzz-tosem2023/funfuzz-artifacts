from ctypes.util import find_library
from ctypes import CDLL, POINTER


def load_c_shmat():
    return CDLL(find_library('c')).shmat


def load_shm(cshmat, cdtype, shmid: int, shmlen: int):
    """
    Attach to shm and return a ptr to this shm. As ctypes treat
    return type as c_int by default, We need to set proper return
    type before invoking a function.

    :param cshmat: the c shmat function to be called
    :param cdtype: the C type of the elements stored in the shm
    :param shmid: id of the shm to load
    :param shmlen: the number of elements assigned for the shm
    :return: a C pointer to the shm
    """
    cshmat.restype = POINTER(cdtype * shmlen)
    return cshmat(shmid, None, 0)


def write_fs_shm(vec, shm, shmlen: int):
    """
    Update fs_shm according to data preserving in vec.

    :param vec: an array-like vector preserving data used for updating
    :param shm: shm area to be updated
    :param shmlen: the number of elements assigned for the shm
    :return:
    """
    _veclen = len(vec)
    if shmlen != _veclen + 1:
        raise RuntimeError(f'shmlen ({shmlen}) should be veclen ({_veclen}) + 1!')
    # We index function from 1 by default, while networkit indexes nodes from 0.
    # Therefore, we need to shift a bit to match shm_idx and vec_idx (fs_idx).
    for _i in range(_veclen):
        # First `[0]` get the array item; second `[_i]`, load the exact element.
        # This mechanism is somehow like LLVM IR.
        shm[0][_i+1] = vec[_i]
    # The flag of whether the update is completed.
    shm[0][0] = 1.


def read_cc_from_shm(shm, shmlen1d: int):
    """
    Read cc from cc_shm and return the resultant 2D list.

    :param shm: shm area to be updated
    :param shmlen1d: the 1D number of elements assigned for the shm
    :return:
    """
    # Initialize cc as a 2D list. Cannot do `[[0]*len1d]*len1d` as
    # it will cause all rows reference to the same object such that
    # the assign to _cc[i][j] will influence every _cc[*][j].
    _cc = []
    for _i in range(shmlen1d):
        _row = []
        for _j in range(shmlen1d):
            _row.append(0)
        _cc.append(_row)
    # Read cc from cc_shm
    for _i in range(shmlen1d):
        for _j in range(shmlen1d):
            # Turn 2D idx into 1D idx
            _idx = _i * shmlen1d + _j
            # Update cr counter, caller counter, and global counter ([0][0]).
            _cnts = shm[0][_idx]
            _cc[_i][_j] = _cnts
            _cc[_i][0] += _cnts
            _cc[0][0] += _cnts
    return _cc
