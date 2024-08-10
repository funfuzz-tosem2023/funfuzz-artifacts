//
// Load value from 2d array using 1d idx
//
#include <stdio.h>
#include <stdlib.h>

#define D 3

int compute_idx(int i1, int i2) {
  return i1 * D + i2;
}

int main(int argc, char **argv) {

  if (argc < 3) {
    printf("Less than 2 arguments!!!");
    return -1;
  }

  static int arr[D][D] = {
    0, 1, 2,
    3, 4, 5,
    6, 7, 8
  };

  int idx1 = atoi(argv[1]);
  int idx2 = atoi(argv[2]);
  int idx = compute_idx(idx1, idx2);

  printf("arr[%d][%d]=%d, id-idx=%d\n", idx1, idx2, *(*arr + idx), idx);

}
