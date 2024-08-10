//
// Trial on some types
//
#include <stdio.h>

#define SIZE 10

typedef unsigned char u8;

void printarr(const char *name, u8 *arr) {

  printf("Arr [%s]: ", name);

  for (int i = 0; i < SIZE; ++i)
    printf("%d", arr[i]);

  printf("\n");

}

int main() {

  u8 arr[SIZE] = {0};
  u8 arr1[SIZE];

  printarr("arr", arr);
  printarr("arr1", arr1);

}
