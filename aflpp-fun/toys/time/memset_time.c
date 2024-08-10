//
// Test time used by memset
//
#include <memory.h>
#include <stdio.h>

#include "loadtime.h"

u64 arr[LEN_2D];

int main(void) {

  u64 stime, etime, elapsed_time;

  stime = get_cur_time_us();

  memset(arr, 1, SIZE_2D_U64);

  etime = get_cur_time_us();

  elapsed_time = etime - stime;

  printf("Time of memset arr: %lld (us)\n", elapsed_time);

  return 0;
}

