//
// ?:
//
#include <stdio.h>
#include <stdlib.h>
#include <memory.h>

#define SIZE 10

typedef unsigned long long u64;

typedef struct struct_type {

  u64     arr1[SIZE];
  double  arr2[SIZE];

} struct_t;

int main() {

  int a = 1 ? 1 : 0;

  printf("a = %d\n", a);

//  double arr[SIZE] = {0};
  u64 arr[SIZE];
  memset(arr, 0, SIZE * sizeof(u64));

  for (int i = 0 ; i < SIZE ; ++i) {
    printf("arr[%d]=%lld\n", i, arr[i]);
    printf("arr[%d]+1=%lld\n", i, arr[i] + 1);
  }
//  for (int i = 0 ; i < SIZE ; ++i) {
//    printf("arr[%d]=%lf\n", i, arr[i]);
//    printf("arr[%d]+1=%lf\n", i, arr[i] + 1);
//  }

  struct_t *s = calloc(1, sizeof(struct_t));

  memset(s, 0, sizeof(struct_t));

  for (int i = 0 ; i < SIZE ; ++i) {
    printf("s->arr1[%d]=%lld\n", i, s->arr1[i]);
    printf("s->arr2[%d]=%lf\n", i, s->arr2[i]);
  }

  return 0;
}
