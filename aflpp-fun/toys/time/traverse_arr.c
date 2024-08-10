//
// Time used by traversing arr of different types
//
#include <stdio.h>
#include "loadtime.h"

#define NUM  (1 << 13)
#define SIZE (NUM*NUM)

u64 arr1[SIZE] = {0};
u32 arr2[SIZE] = {0};

int main(void) {

  u64 start_tp1 = get_cur_time_us();
  for (int i = 0; i < NUM; ++i)
    for (int j = 0; j < NUM; ++j) {
      int crIdx = j * NUM + i;
      ++arr1[0];
      ++arr1[crIdx];        // Count for the call relation
    }
  u64 dura1 = get_cur_time_us() - start_tp1;
  printf("Time of traversing u64 arr: %llu\n", dura1);

  u64 start_tp2 = get_cur_time_us();
  for (int i = 0; i < NUM; ++i)
    for (int j = 0; j < NUM; ++j) {
      int crIdx = j * NUM + i;
      ++arr2[0];
      ++arr2[crIdx];        // Count for the call relation
    }
  u64 dura2 = get_cur_time_us() - start_tp2;
  printf("Time of traversing u32 arr: %llu\n", dura2);

}
