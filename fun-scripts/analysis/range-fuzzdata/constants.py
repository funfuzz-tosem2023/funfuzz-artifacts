figsize = (5.0, 4.5)
cline_width = 2                           # Line width for curve
time_upper = 86400                          # 24hour
fuzzers = ['aflpp', 'fun', 'fun-static', 'fairfuzz']
targets = ['cxxfilt', 'objdump', 'nm-new', 'readelf', 'djpeg',
           'mjs', 'mutool', 'readpng', 'tcpdump', 'xmllint']
fuzz_label = {
    'fun': 'FunFuzz',
    'fun-static': 'FunFuzz-static',
    'aflpp': 'AFL++',
    'fairfuzz': 'FairFuzz',
}
shapes = {                                  # Shapes for lines in figures, each tuple is (<color>, <style>)
    'aflpp': ('#4169E1', (0, (1, 1))),               # RoyalBlue, Densely DashDotted
    'fairfuzz': ('#4EEE94', 'dashdot'),                 # Seagreen2, DashDot
    'fun': ('#FF3030', 'solid'),                   # Firebrick1, Solid
    'fun-static': ('#FFA500', 'dashed'),                  # Orange, Dashed
}
lab_map = {
    'time': 'Time (Hours)',
    'execution': '#Executions',
    'coverage': '#Edges',
    'crash': '#Crashes',
}


