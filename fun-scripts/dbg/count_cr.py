import sys
import os

"""
Count to tell us: how many unique call relations a PUT contains?
"""

if __name__ == '__main__':
    # Path to bbCalls
    in_path = os.path.abspath(sys.argv[1])

    # Count for unique calls
    call_relations = []
    with open(in_path, 'r') as f:
        for line in f.readlines():
            if line.strip() == '':
                continue
            cr = ','.join(line.strip().split(',')[1:3])
            call_relations.append(cr)

    # Deduplicate
    call_relations = sorted(list(set(call_relations)))
    cnt = 0
    for cr in call_relations:
        cnt += 1
        print(f'{cnt}\t`{cr}`')
