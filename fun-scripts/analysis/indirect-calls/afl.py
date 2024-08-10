import os


def determine_afl_type(out_dir: str) -> str:
    """
    Determine afl type ('afl' or 'aflpp') by the header of plot_data
    """
    # Locate plot_data
    _pd_file = os.path.join(out_dir, 'plot_data')
    with open(_pd_file, 'r') as _f:
        _header = _f.readline()
    if _header.startswith('# unix_time'):
        return 'afl'
    elif _header.startswith('# relative_time'):
        return 'aflpp'
    else:
        raise RuntimeError('[ERROR] Unsupported afl-type: ' + out_dir)


def is_afl_out_folder(folder: str) -> bool:
    _fn_list = os.listdir(folder)
    return ('plot_data' in _fn_list) and ('queue' in _fn_list) and \
        (os.path.isdir(os.path.join(folder, 'queue'))) and \
        (not os.path.isdir(os.path.join(folder, 'plot_data')))


def locate_out_folders(root_dir: str) -> list:
    """
    Locate afl out dir recursively. An afl out dir must have a plot_data
    and a queue/ dir under it.
    """
    _out_dirs = set()
    _folder_stack = [root_dir]
    while len(_folder_stack) != 0:
        _dir = _folder_stack.pop()
        if is_afl_out_folder(folder=_dir):
            _out_dirs.add(_dir)
        else:
            # Dig afl out dirs recursively
            for _fn in os.listdir(_dir):
                _path = os.path.join(_dir, _fn)
                if os.path.isdir(_path):
                    _folder_stack.append(_path)
    return sorted(list(_out_dirs))
