//
// Test time of switching idx
//
#include <stdio.h>
#include "loadtime.h"

#define CNT 2U

int main(void) {

  int idx = 1;
//  int idx = 0;
  long st, et;

  printf("Before switch (1), idx=%d\n", idx);

  st  = get_cur_time_us();
  idx = (idx + 1) % CNT;
  et  = get_cur_time_us();

  printf("Time switch (1): %ld (us), idx=%d\n", et - st, idx);

  printf("==========================================================\n");

  printf("Before switch (2), idx=%d\n", idx);

  st  = get_cur_time_us();
  idx = idx ? 0 : 1;
  et  = get_cur_time_us();

  printf("Time switch (2): %ld (us), idx=%d\n", et - st, idx);



}
