import matplotlib
import matplotlib.pyplot as plt

# To avoid type-3 font error
matplotlib.rcParams['pdf.fonttype'] = 42
matplotlib.rcParams['ps.fonttype'] = 42
plt.rcParams['font.size'] = 16

# fuzzers = [
#     # Real-world
#     'fun', 'fun-static',
#     'aflpp', 'fairfuzz', 'aflgo',
#     # Magma
#     'aflplusplus', 'funfuzz', 'fairfuzz',
#     'k_scheduler', 'aflgo', 'entropic',
# ]

targets = [
    # Real-world
    'cxxfilt', 'nm-new', 'objdump', 'readelf', 'djpeg',
    'readpng', 'mjs', 'mutool', 'xmllint', 'tcpdump',
    # Magma
    'libpng_read_fuzzer', 'sndfile_fuzzer',
    'libxml2_xml_read_memory_fuzzer', 'lua', 'sqlite3_fuzz'
]

# Color setting
colors = {
    'fun': '#FF3030',
    'fun-static': 'magenta',
    # 'fun-static': '#FFA500',
    # Baselines
    'aflpp': '#4169E1',
    'fairfuzz': '#4EEE94',
    'aflgo': 'gray',
    # Magma-specific
    'funfuzz': '#FF3030',
    'entropic': 'purple',
    'k_scheduler': 'orange',
    # Rho
    'fun-rho0d5': '#4EEE94',
    'fun-rho1': 'gray',
    'fun-rho1d5': 'purple',
    'fun-rho2': '#FF3030',
    'fun-rho2d5': 'magenta',
    'fun-rho3': 'green',
}

fuzzers = list(colors.keys())


def output_fig(figure: plt.Figure, path: str, tight: bool = True):
    if tight:
        figure.tight_layout()
    figure.savefig(path)
    print('[LOG] Output to:', path)
    plt.close()

