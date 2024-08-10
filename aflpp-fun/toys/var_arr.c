//
// Initialize array with variable length in C
//
#include <stdlib.h>
#include <stdio.h>

#define LEN 10

int main(int argc, char **argv) {

  double *arr_ptr = (double *)malloc(LEN * sizeof(double));

  for (int i = 0 ; i < LEN; ++i)
    printf("arr_ptr[%d]=%lf\n", i, arr_ptr[i]);


}
