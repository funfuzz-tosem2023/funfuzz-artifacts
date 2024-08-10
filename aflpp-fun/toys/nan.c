//
// double nan?
//
#include <stdio.h>

int main(void) {

  double zd = 0;

  printf("(zd == 0) %d\n", (zd == 0));
  printf("1/zd %lf\n", 1 / zd);
  printf("0/zd %lf\n", 0 / zd);

}