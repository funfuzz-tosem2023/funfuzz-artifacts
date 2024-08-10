//
// Test random
//
#include <stdlib.h>
#include <stdio.h>
#include <time.h>

#define LEN   2614*2614

int arr1[LEN], arr2[LEN];

int main(void) {

  srand(time(NULL));

  for (int i = 0; i < LEN; i++) {
    arr1[i] = rand() % 10;
  }

  for (int i = 0; i < LEN; i++) {
    arr2[i] = rand() % 10;
  }

  for (int i = 0; i < LEN; i++) {
    printf("%d %d, ", arr1[i], arr2[i]);
  }
  printf("\n");

//  for (int i = 0; i < 10; ++i)
//    printf("%d ", rand() % 10);
//  printf("\n");
//
//  for (int i = 0; i < 10; ++i)
//    printf("%d ", rand() % 10);
//  printf("\n");


}
