import sys

"""
Read from stdin
"""

BUFFER_SIZE = 1024

if __name__ == '__main__':
    cnt = 5
    while cnt:
        cnt -= 1
        passed_bytes = sys.stdin.read(BUFFER_SIZE)
        print(f'[P] pass_bytes={passed_bytes}')
