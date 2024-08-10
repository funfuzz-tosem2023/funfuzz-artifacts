//
// Example given by teacher FCR
//
#include <time.h>
#include <stdio.h>

//#define NUM 3200
//#define NUM 32000
#define NUM (1 << 13)

typedef long long u64;

u64 temp[NUM][NUM];

int main(void) {

  int rd = NUM * NUM;
  clock_t start, end;

  start = clock();
  for (int i = 0 ; i < rd; i++) {
    ++temp[(i+1)%NUM][i/NUM];
    ++temp[(i+2)%NUM][i/NUM];
    ++temp[(i+3)%NUM][i/NUM];
  }
  end = clock();
  printf("time=%f\n", (double)(end - start) / CLOCKS_PER_SEC);

  // ================================================ //

  start = clock();
  for (int i = 0 ; i < rd; i++) {
    ++temp[i/NUM][(i+1)%NUM];
    ++temp[i/NUM][(i+2)%NUM];
    ++temp[i/NUM][(i+3)%NUM];
  }
  end = clock();
  printf("time=%f\n", (double)(end - start) / CLOCKS_PER_SEC);


}
