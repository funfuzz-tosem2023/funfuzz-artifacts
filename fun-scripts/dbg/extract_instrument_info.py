import os
import sys

if __name__ == '__main__':
    # Read in
    log_path = os.path.abspath(sys.argv[1])
    # Prepare out
    out_path = os.path.join(os.path.dirname(log_path),
                            os.path.basename(log_path).replace('.log', '-extract.log'))

    print(f'Read from: `{log_path}`.')

    # Extract logs
    lines = []
    with open(log_path, 'r') as f:
        for line in f.readlines():
            if ('[+]' in line) and ('Instrumented' in line):
                lines.append(line)
    # Output
    with open(out_path, 'w') as f:
        f.write(''.join(lines))

    print(f'Output to: `{out_path}`.')
