import os

from reproduce import splitter
crash_types = [
    'memory-leak',
    'out-of-memory',
    'heap-buffer-overflow',
    'stack-overflow',
    'stack-buffer-overflow',
    'allocation-size-too-big',
    'global-buffer-overflow',
    'heap-use-after-free',
    'SEGV',
    'memcpy-param-overlap',
    'negative-size-param',
]


fuzzers = ['aflpp', 'fairfuzz', 'fun', 'fun-static', 'aflgo']
targets = ['readpng', 'mjs', 'cxxfilt', 'nm-new', 'objdump',
           'readelf', 'djpeg', 'tcpdump', 'mutool', 'xmllint']
# targets = ['cxxfilt', 'nm-new', 'objdump', 'readelf',
#            'djpeg', 'pngtest', 'tcpdump', 'mutool', 'xmllint']


def parse_summary(full_summary: str) -> str:
    for _crash_type in crash_types:
        if _crash_type in full_summary:
            return _crash_type
    if 'leak' in full_summary:
        return 'memory-leak'
    print('[WARN] Find unknown crash type, summary:', full_summary)
    return full_summary


def parse_one_crash_log(path: str, target: str) -> set:
    """
    Parse one crash log to get unique crashes, each crash is represented
    as <first_loc>-<summary>

    :param path: path to the crash log
    :param target: target that are parse
    :return: a set of unique crashes
    """
    crash_pattern = '<%s>-<%s>'
    _crash_set = set()
    with open(path, 'rb') as f:
        _crash_start = False
        _first_loc = None
        for _ in f.readlines():
            try:
                _content = _.decode('utf-8').strip()
            except UnicodeDecodeError:
                continue
            # print(_content)
            if _content == splitter:
                # A crash started
                _crash_start = True
            elif _crash_start:
                # Find first line of location
                if _content == '<empty stack>' and not _first_loc:
                    _first_loc = 'empty-stack'
                elif _content.startswith('#') and not _first_loc:
                    if '(<unknown module>)' in _content:
                        _first_loc = 'unknown-module'
                    elif ('libc-start.c' not in _content) and ('sanitizer' not in _content) \
                            and ('asan_' not in _content) \
                            and ('0x' in _content) \
                            and (';&#' not in _content):
                        # 'sanitizer' and 'asan': filter out some sanitizer stacks
                        # Parse first location as file:line
                        _first_loc = os.path.basename(_content.split(' ')[-1])
                elif _content.startswith('SUMMARY'):
                    # Summarize the crash
                    _summary_detail = _content.split(': ')[-1]
                    if _first_loc is None:
                        # Handle the special cases that first loc has not been found
                        if (target == 'mjs') and ('mjs+' in _summary_detail):
                            # SEGV (/root/qrx/aflpp_fun/evaluation/asan/bench/mjs/mjs+0x578803) in _fini
                            # print('[LOG]', _summary_detail)
                            # print(_summary_detail.split(' '))
                            _parenthesis_content = _summary_detail.split(' ')[1].lstrip('(').rstrip(')')
                            _first_loc = _parenthesis_content.split('/')[-1]
                        elif '<unknown module>' in _summary_detail:
                            # SEGV (<unknown module>)
                            _first_loc = 'unknown-module'
                        else:
                            # SEGV /root/qrx/aflpp_fun/evaluation/bench-others/mjs-2.20.0/mjs.c:8472:31 in getprop_builtin_foreign
                            _path_content = _summary_detail.split(' ')[1]
                            _first_loc = _path_content.split('/')[-1].split(':')[0]
                    # Only record line number
                    if ':' in _first_loc:
                        _first_loc = '%s:%s' % (_first_loc.split(':')[0], _first_loc.split(':')[1])
                    if 'byte(s)' in _first_loc:
                        _first_loc = 'unknown-location'
                    if '+' in _first_loc:
                        _first_loc = _first_loc.rstrip(')')
                        _first_loc = _first_loc.split('+')[0]
                    # SUMMARY: AddressSanitizer: out-of-memory /root/build/llvm_tools/llvm-11.0.0.src/projects/compiler-rt/lib/asan/asan_malloc_linux.cpp:145 in malloc
                    _summary = parse_summary(_summary_detail)
                    # Build a crash
                    _crash = crash_pattern % (_first_loc, _summary)
                    if ')' in _crash:
                        print(_crash)
                        print(_content)
                    # print(_crash)
                    if _summary is None or _first_loc is None:
                        print('[ERROR] Crash content error')
                        print('[ERROR]', _content)
                        raise RuntimeError(f'Invalid summary of loc, summary={_summary}, loc={_first_loc}')
                    _crash_set.add(_crash)
                    # This crash finished when met summary
                    _crash_start = False
                    _first_loc = None
                else:
                    continue
    return _crash_set
