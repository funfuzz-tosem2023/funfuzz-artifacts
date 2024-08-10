//
// Test ull to u8
//
#include <stdio.h>

typedef unsigned long long u64;
typedef unsigned char u8;

int main() {

  u64 arr1[10];
  u8  arr2[10];
  u8 *u8ptr;

  for (int i = 0 ; i < 10 ; i++) {
    arr1[i] = i % 2;
    printf("%llu ", arr1[i]);
  }
  printf("\n");

  printf("Transforming to u8..........\n");


  for (int i = 0 ; i < 10 ; i++) {
    arr2[i] = (u8) arr1[i];
    printf("%u ", arr2[i]);
  }
  printf("\n");

  printf("Print u8ptr (not attach)..........\n");
  printf("u8ptr==NULL %s\n", (u8ptr == NULL) ? "true" : "false");
  printf("u8ptr %p\n", u8ptr);
  for (int i = 0 ; i < 10 ; i++) {
    printf("%u ", u8ptr[i]);
  }
  printf("\n");

  printf("Print u8ptr (attach)..........\n");
  u8ptr = arr2;
  printf("u8ptr %p\n", u8ptr);
  for (int i = 0 ; i < 10 ; i++) {
    printf("%u ", u8ptr[i]);
  }
  printf("\n");

}


