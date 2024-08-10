//
// Test how to print format double
//
#include <stdio.h>

int main(void) {

  double d = 0.0111213141516171819;

  printf("%.18lf\n", d);
  printf("%.19lf\n", d);
  printf("%.20lf\n", d);

}