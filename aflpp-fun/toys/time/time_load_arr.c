//
// Examine the time used by different means of visiting an array
//
#include <sys/time.h>
#include <stdio.h>

#define NUM  (1 << 13)
#define SIZE (NUM*NUM)

typedef long long u64;

int arr1[SIZE] = {0};
int arr2[SIZE] = {0};

u64 get_cur_time_us(void) {

  struct timeval  tv;
  struct timezone tz;

  gettimeofday(&tv, &tz);

  return (tv.tv_sec * 1000000ULL) + tv.tv_usec;

}

int main(void) {

  // Imitate visiting by rows and keep time
  u64 start_tp1 = get_cur_time_us();
  for (int i = 0; i < NUM; ++i)
    for (int j = 0; j < NUM; ++j) {
      int idx = i * NUM + j;
      ++arr1[idx];
    }
  u64 dura1 = get_cur_time_us() - start_tp1;

  // Imitate visiting by rows and keep time
  u64 start_tp2 = get_cur_time_us();
  for (int i = 0; i < NUM; ++i)
    for (int j = 0; j < NUM; ++j) {
      int idx = i + j * NUM;
      ++arr2[idx];
    }
  u64 dura2 = get_cur_time_us() - start_tp2;

  // Print result
  printf("NUM %d, SIZE(=NUM^2) %d\n", NUM, SIZE);
  printf("Time used by visit arr1 by rows: %llu (us)\n", dura1);
  printf("Time used by visit arr2 by cols: %llu (us)\n", dura2);
  printf("row_t/col_t=%lf\n", ((double)dura1) / ((double)dura2));
  printf("=================================================\n");

}
