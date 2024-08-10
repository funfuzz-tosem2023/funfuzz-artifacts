import matplotlib
import matplotlib.pyplot as plt

# To avoid type-3 font error
matplotlib.rcParams['pdf.fonttype'] = 42
matplotlib.rcParams['ps.fonttype'] = 42
plt.rcParams['font.size'] = 16


# Color setting
# colors = {
#     # 'fun': '#FF3030',
#     # 'fun-static': 'magenta',
#     # 'fun-static': '#FFA500',
#     # Baselines
#     'aflpp': '#4169E1',
#     'fairfuzz': '#4EEE94',
#     'aflgo': 'gray',
#     # Magma-specific
#     'funfuzz': '#FF3030',
#     'funfuzz-static': 'magenta',
#     'entropic': 'purple',
#     'k_scheduler': 'orange',
#     # Edge-only the shadow mode
#     'edgeonly': 'brown',
# }

# fuzzers = [
#     # Real-world
#     'aflpp',
#     'funfuzz', 'funfuzz-static',
#     'fairfuzz', 'aflgo',
#     # Magma
#     'aflplusplus', 'funfuzz', 'fairfuzz',
#     'k_scheduler', 'aflgo', 'entropic',
# ]

colors = {
    'aflpp': '#4169E1',
    'funfuzz': '#FF3030',
    'funfuzz-static': 'magenta',
    'fairfuzz': '#4EEE94',
    'aflgo': 'gray',
    # Magma-specific
    'aflplusplus': '#4169E1',
    'entropic': 'purple',
    'k_scheduler': 'orange',
    # Edge-only the shadow mode
    'edgeonly': 'brown',
}

fuzzers = list(colors.keys())

targets = [
    # Real-world
    'cxxfilt', 'nm-new', 'objdump', 'readelf', 'djpeg',
    'readpng', 'mjs', 'mutool', 'xmllint', 'tcpdump',
    # Magma
    'libpng_read_fuzzer', 'sndfile_fuzzer',
    'libxml2_xml_read_memory_fuzzer', 'lua', 'sqlite3_fuzz'
]


def output_fig(figure: plt.Figure, path: str, tight: bool = True):
    if tight:
        figure.tight_layout()
    figure.savefig(path)
    print('[LOG] Output to:', path)
    plt.close()

