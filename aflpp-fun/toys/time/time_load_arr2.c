//
// Examine the time used by different means of visiting an array
//
#include <sys/time.h>
#include <stdio.h>
#include <stdlib.h>

#define NUM  (1 << 10)
//#define NUM  ((1 << 10) | (1 << 9))
//#define NUM  (1 << 10 | 1 << 9 | 1 << 8)
//#define NUM  (1 << 10 | 1 << 9 | 1 << 8 | 1 << 7)
//#define NUM  (1 << 10 | 1 << 9 | 1 << 8 | 1 << 7 | 1 << 6)
//#define NUM  (1 << 11)
//#define NUM  (1 << 12)
//#define NUM  (1 << 13)
#define SIZE (NUM*NUM)

typedef long long u64;

int arr1[NUM][NUM] = {0};
int arr2[SIZE] = {0};
int arr3[NUM][NUM] = {0};
int arr4[SIZE] = {0};

u64 get_cur_time_us(void) {

  struct timeval  tv;
  struct timezone tz;

  gettimeofday(&tv, &tz);

  return (tv.tv_sec * 1000000ULL) + tv.tv_usec;

}

int main(void) {

  // Visiting by rows and keep time
  u64 start_tp1 = get_cur_time_us();
  for (int i = 0; i < NUM; ++i)
    for (int j = 0; j < NUM; ++j) {
      ++arr1[i][j];
    }
  u64 dura1 = get_cur_time_us() - start_tp1;

  // Imitate visiting by rows and keep time
  u64 start_tp2 = get_cur_time_us();
  for (int i = 0; i < NUM; ++i)
    for (int j = 0; j < NUM; ++j) {
      int idx = i * NUM + j;
      ++arr2[idx];
    }
  u64 dura2 = get_cur_time_us() - start_tp2;

  // Visiting by rows and keep time
  u64 start_tp3 = get_cur_time_us();
  for (int i = 0; i < NUM; ++i)
    for (int j = 0; j < NUM; ++j) {
      ++arr3[j][i];
    }
  u64 dura3 = get_cur_time_us() - start_tp3;

  // Imitate visiting by rows and keep time
  u64 start_tp4 = get_cur_time_us();
  for (int i = 0; i < NUM; ++i)
    for (int j = 0; j < NUM; ++j) {
      int idx = i + j * NUM;
      ++arr4[idx];
    }
  u64 dura4 = get_cur_time_us() - start_tp4;


  // Print result
  printf("NUM %d, SIZE(=NUM^2) %d\n", NUM, SIZE);
  printf("Time used by visit arr1 by rows: %llu (us)\n", dura1);
  printf("Time used by visit arr2 by rows (imit): %llu (us)\n", dura2);
  printf("Time used by visit arr3 by cols: %llu (us)\n", dura3);
  printf("Time used by visit arr4 by cols (imit): %llu (us)\n", dura4);
  printf("=================================================\n");

}
