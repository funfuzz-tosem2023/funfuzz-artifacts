//
// Test read env and then atoi
//
#include <stdio.h>
#include <stdlib.h>

typedef unsigned char u8;

int main(void) {

//  u8 flag = !atoi(getenv("TEST"));
  u8 flag = !!getenv("TEST");

  printf("flag=%u\n", flag);

  return 0;
}
