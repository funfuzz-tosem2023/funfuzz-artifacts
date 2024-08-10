//
// Examine the time used by different means of visiting an array
//
#include <sys/time.h>
#include <stdio.h>

//#define NUM  (1 << 10)
//#define NUM  ((1 << 10) | (1 << 9))
//#define NUM  (1 << 10 | 1 << 9 | 1 << 8)
//#define NUM  (1 << 10 | 1 << 9 | 1 << 8 | 1 << 7)
//#define NUM  (1 << 10 | 1 << 9 | 1 << 8 | 1 << 7 | 1 << 6)
//#define NUM  (1 << 11)
//#define NUM  (1 << 12)
#define NUM  (1 << 13)
#define SIZE (NUM*NUM)

typedef long long u64;

u64 arr1[SIZE] = {0};

u64 get_cur_time_us(void) {

  struct timeval  tv;
  struct timezone tz;

  gettimeofday(&tv, &tz);

  return (tv.tv_sec * 1000000ULL) + tv.tv_usec;

}

int main(void) {


  // Use arr[caller][0] to count for a caller.
  u64 start_tp1 = get_cur_time_us();
  for (int i = 1; i < NUM; ++i)
    for (int j = 1; j < NUM; ++j) {
      int callerIdx = i * NUM + 0;
      int crIdx = callerIdx + j;
      ++arr1[0];              // Count all calls
      ++arr1[callerIdx];      // Count for the caller
      ++arr1[crIdx];          // Count for the call relation
    }
  u64 dura1 = get_cur_time_us() - start_tp1;

  // arr[0][caller] to count for caller?
  u64 start_tp2 = get_cur_time_us();
  for (int i = 1; i < NUM; ++i)
    for (int j = 1; j < NUM; ++j) {
      int callerIdx = i;
      int crIdx = callerIdx + j;
      ++arr1[0];            // Count all calls
      ++arr1[callerIdx];    // Count for the caller
      ++arr1[crIdx];        // Count for the call relation
    }
  u64 dura2 = get_cur_time_us() - start_tp2;

  // What if we only count for call relation?
  u64 start_tp3 = get_cur_time_us();
  for (int i = 1; i < NUM; ++i)
    for (int j = 1; j < NUM; ++j) {
      int crIdx = i * NUM + j;
      ++arr1[crIdx];        // Count for the call relation
    }
  u64 dura3 = get_cur_time_us() - start_tp3;

  // arr[caller][0] and cr
  u64 start_tp4 = get_cur_time_us();
  for (int i = 1; i < NUM; ++i)
    for (int j = 1; j < NUM; ++j) {
      int callerIdx = i * NUM + 0;
      int crIdx = callerIdx + j;
      ++arr1[callerIdx];    // Count for the caller
      ++arr1[crIdx];        // Count for the call relation
    }
  u64 dura4 = get_cur_time_us() - start_tp4;

  // arr[0][caller] and cr
  u64 start_tp5 = get_cur_time_us();
  for (int i = 1; i < NUM; ++i)
    for (int j = 1; j < NUM; ++j) {
      int caller = i;
      int crIdx = i * NUM + j;
      ++arr1[caller];            // Count for the caller
      ++arr1[crIdx];        // Count for the call relation
    }
  u64 dura5 = get_cur_time_us() - start_tp5;

  // Print result
  printf("NUM %d, SIZE(=NUM^2) %d\n", NUM, SIZE);
  printf("dura1 (0+arr[caller][0]+cr): %llu (us)\n", dura1);
  printf("dura2 (0+arr[0][caller]+cr): %llu (us)\n", dura2);
  printf("dura3 (only cr): %llu (us)\n", dura3);
  printf("dura4 (arr[caller][0]+cr): %llu (us)\n", dura4);
  printf("dura5 (arr[0][caller]+cr): %llu (us)\n", dura5);
  printf("=================================================\n");

}
