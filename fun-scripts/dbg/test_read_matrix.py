import sys

import numpy as np
import time
from tqdm import tqdm

"""
Test time used by read a large matrix
"""

if __name__ == '__main__':
    size = int(sys.argv[1])

    # 1d Arr
    arr = np.zeros(size)
    arr1 = np.ones(size)
    start_time1 = time.time()
    for i in tqdm(range(size), desc=f'Update array of size={size}'):
        arr1[i] = arr[i]
    elapsed_time1 = time.time() - start_time1

    # 2d Arr
    matrix = np.zeros((size, size))
    matrix1 = np.ones((size, size))
    start_time2 = time.time()
    for i in tqdm(range(size), desc=f'Update matrix of size={size}^2'):
        for j in range(size):
            matrix1[i][j] = matrix[i][j]
    elapsed_time2 = time.time() - start_time2

    print(f'arr_t={elapsed_time1}')
    print(f'matrix_t={elapsed_time2}')
    print(f'matrix_t/arr_t={elapsed_time2 / elapsed_time1}')
