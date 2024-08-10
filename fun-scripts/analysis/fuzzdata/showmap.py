import os
import shutil
import subprocess
import pandas as pd

args_map = {
    'readpng': [],
    'mjs': ['-f', '@@'],
    'cxxfilt': [],
    'djpeg': ['@@'],
    'mutool': ['draw', '@@', '-o', './out'],
    'nm-new': ['@@'],
    'objdump': ['-d', '@@'],
    'pngtest': ['@@'],
    'readelf': ['-a', '@@'],
    'tcpdump': ['-nr', '@@'],
    'xmllint': ['@@'],
}


def read_edgedata_as_dict(path: str) -> dict:
    _edgedata = {}
    with open(path, 'r') as f:
        for _ in f.readlines():
            _content = _.strip()
            if _content == '':
                continue
            _parts = _content.split(':')
            _edgedata[int(_parts[0])] = int(_parts[1])
    return _edgedata


def create_showmap_dict(dpath: str) -> dict:
    """
    Read edge data and create a dict from id -> #edge
    :param dpath: path to show directory
    :return: edge num dict from case_id -> #edge
    """
    _edgenum_dict = {}
    _total_edgedata_dict = {}
    for _fn in os.listdir(dpath):
        if not _fn.startswith('id'):
            continue
        # _fn be like: `id:000001,src:000000,time:125,execs:158,op:havoc,rep:8,+cov`
        _case_id = int(_fn.split(',')[0].replace('id:', ''))
        _total_edgedata_dict.update(read_edgedata_as_dict(path=os.path.join(dpath, _fn)))
        _edgenum_dict[_case_id] = len(_total_edgedata_dict)
    return _edgenum_dict


def calibrate_one(showmap_path, target_args: list, fuzzdata_dir):
    # Prepare paths
    queue_dir = os.path.join(fuzzdata_dir, 'queue')
    pd_path = os.path.join(fuzzdata_dir, 'plot_data')
    showmap_dir = os.path.join(fuzzdata_dir, 'showmap')
    total_edge_path = os.path.join(fuzzdata_dir, 'total_edge')
    old_pd_path = os.path.join(fuzzdata_dir, 'plot_data.old')

    # Choose source plot_data file
    target_pd_path = pd_path
    if os.path.exists(old_pd_path):
        print(f'plot_data.old exists, use it: `{old_pd_path}`')
        target_pd_path = old_pd_path

    # Remove exiting showmap_dir
    if os.path.exists(showmap_dir):
        shutil.rmtree(showmap_dir)

    # Generate edge coverage with showmap
    each_edge_cmd = [showmap_path, '-e', '-i', queue_dir, '-o', showmap_dir, '--'] + target_args
    total_edge_cmd = [showmap_path, '-eC', '-i', queue_dir, '-o', total_edge_path, '--'] + target_args
    subprocess.run(each_edge_cmd)
    subprocess.run(total_edge_cmd)
    print(f'Write showmap data to: `{showmap_dir}`')
    print(f'Write total showmap data to: `{total_edge_path}`')

    # Read edge data
    edgenum_map = create_showmap_dict(dpath=showmap_dir)
    # Debug
    # print(edgenum_map)

    # Read and deprecate old plot data
    pd_df = pd.read_csv(target_pd_path, index_col='# relative_time',
                        engine='python', delimiter=', ')
    if not os.path.exists(old_pd_path):
        # Meaning that we are using pd_path
        os.rename(target_pd_path, os.path.join(fuzzdata_dir, 'plot_data.old'))

    # Build new plot data and write back
    edge_col = []
    for corpus_count in pd_df['corpus_count']:
        case_id = int(corpus_count - 1)
        edge_col.append(edgenum_map[case_id])
    pd_df['edges_found'] = edge_col
    pd_df.to_csv(pd_path)
    print('--------------------------------------------------------------')
    print('Finish calibrating plot_data :-) !')
