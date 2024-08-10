#include <stdio.h>

int main(void) {

  unsigned int base = 100;

  unsigned int res = base * 4;
  unsigned int res1 = base * 4.1;
  unsigned int res2 = base * 4.15;
  unsigned int res3 = base * 4.157841;

  printf("%u %u %u %u\n", res, res1, res2, res3);

}
