import os
from tqdm import tqdm

"""
Core utils for reproduction
"""

# targets = ['mjs', 'cxxfilt', 'nm-new', 'objdump', 'readelf',
#            'djpeg', 'pngtest', 'readpng', 'tcpdump', 'mutool', 'xmllint']
targets = ['mjs', 'cxxfilt', 'nm-new', 'objdump', 'readelf',
           'djpeg', 'readpng', 'tcpdump', 'mutool', 'xmllint']

repro_tmp_map = {
    'mjs': '@target -f @input 2>> @log 1>/dev/null',
    'cxxfilt': 'cat @input | @target 2>> @log 1>/dev/null',
    'djpeg':   '@target @input 2>> @log 1>/dev/null',
    'mutool':  '@target draw @input -o ./mutool-out 2>> @log 1>/dev/null',
    'nm-new':  '@target @input 2>> @log 1>/dev/null',
    'objdump': '@target -d @input 2>> @log 1>/dev/null',
    'pngtest': '@target @input 2>> @log 1>/dev/null',
    'readpng': 'cat @input | @target 2>> @log 1>/dev/null',
    'readelf': '@target -a @input 2>> @log 1>/dev/null',
    'tcpdump': '@target -nr @input 2>> @log 1>/dev/null',
    'xmllint': '@target @input 2>> @log 1>/dev/null',
}

splitter = 'FUN-FUN-FUN-FUN-FUN'


def create_cmd(target: str, target_path: str, input_path: str, log_path: str):
    """
    Parse commandline needed for reproduction
    """
    _cmdtmp = repro_tmp_map[target]
    _cmd = _cmdtmp.replace('@target', target_path).replace('@input', input_path).replace('@log', log_path)
    return _cmd


def rerun_one(target: str, target_path: str, input_path: str, log_path: str):
    """
    Rerun one preserved test input
    """
    _cmd = create_cmd(target, target_path, input_path, log_path)
    # print('[LOG]', _cmd)
    splitter_cmd = f'echo {splitter} >> {log_path}'
    os.system(_cmd)
    os.system(splitter_cmd)


def get_input_paths(fuzzdata_dir: str) -> list:
    _crashes_dir = os.path.join(fuzzdata_dir, 'crashes')
    _queue_dir = os.path.join(fuzzdata_dir, 'queue')
    if not os.path.isdir(_crashes_dir):
        raise RuntimeError('Invalid crashes dir: ', _crashes_dir)
    if not os.path.isdir(_queue_dir):
        raise RuntimeError('Invalid queue dir: ', _queue_dir)
    _crashing_inputs = [os.path.join(_crashes_dir, _) for _ in os.listdir(_crashes_dir) if _.startswith('id')]
    _queue_inputs = [os.path.join(_queue_dir, _) for _ in os.listdir(_queue_dir) if _.startswith('id')]
    print('[LOG] Find %d crashing inputs from `%s`' % (len(_crashing_inputs), _crashes_dir))
    print('[LOG] Find %d queue inputs from `%s`' % (len(_queue_inputs), _queue_dir))
    _input_paths = sorted(_crashing_inputs + _queue_inputs)
    print('[LOG] Find %d inputs in total' % len(_input_paths))
    return _input_paths


def reproduce_one_out(fuzzdata_dir: str, target: str, target_path: str, log_path: str):
    """
    Reproduce all test cases under fuzzdata directory, including 
    1) xxx/crashes/ and 2) xxx/queue
    """
    _input_paths = get_input_paths(fuzzdata_dir)
    # Run each
    for _input_path in tqdm(_input_paths, desc='Reproducing test inputs'):
        rerun_one(target, target_path, _input_path, log_path)
