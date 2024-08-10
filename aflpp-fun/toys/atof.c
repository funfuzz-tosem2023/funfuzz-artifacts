//
// Test atof
//
#include <stdlib.h>
#include <stdio.h>

int main(void) {

  char *double_str = "5.565158670517678444e-03";

  double d = atof(double_str);

  printf("Number d=%lf\n", d);

}