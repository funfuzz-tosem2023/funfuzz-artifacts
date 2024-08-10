//
// Manipulations on bits
//
#include <stdio.h>

#define U8_SIZE 8

typedef unsigned char u8;
typedef unsigned long long u64;

void printBits(const char *name, const u64 *temp) {

  printf("%s=[", name);

  u8 *bits = (u64 *)temp;

  for (int i = 0 ; i < U8_SIZE; i++) {
    printf("%d", bits[i]);
    if (i != (U8_SIZE - 1)) printf(", ");
  }

  printf("]\n");

}

int main() {

  u8 val1 = 127;

  u8 *bits1 = &val1;

  printBits("val1", (u64 *)bits1);

  return 0;

}
