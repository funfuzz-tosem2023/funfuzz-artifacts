"""
@FUN: Transform Fdumps.txt into the BBtargets.txt file required by aflgo.
"""
import os
import sys

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("Usage: this_script.py <fundump_dir>")
        exit(0)
    # Parse args and locate Fdumps.txt file.
    fundump_dir = os.path.abspath(sys.argv[1])
    fdumps_file = os.path.join(fundump_dir, 'Fdumps.txt')

    # Read lines and filter out function names.
    bbtargets = []
    with open(fdumps_file, 'r') as f:
        # Line pat: `<func_name>,<filename>:<linenumber>`, i.e., `<func_name>,<aflgo_bbname>` 
        for line in f.readlines():
            bbtargets.append(line.split(',')[-1])

    # Write into BBtargets.txt file
    bbtargets_file = os.path.join(fundump_dir, 'BBtargets.txt')        
    with open(bbtargets_file, 'w') as f:
        f.writelines(bbtargets)
    print('Write to file: ', bbtargets_file)
