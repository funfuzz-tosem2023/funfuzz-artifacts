//
// Test double min max
//
#include <float.h>
#include <stdio.h>

int main() {

  printf("max=%lf\n", DBL_MAX);
  printf("min=%lf\n", DBL_MIN);


  printf("(-1.0 < DBL_MIN)=%s\n", (-1.0 < DBL_MIN) ? "true" : "false");

  printf("(0.0 < DBL_MIN)=%s\n", (0.0 < DBL_MIN) ? "true" : "false");

  printf("(0.0001241287 < DBL_MIN)=%s\n",
         (0.0001241287 < DBL_MIN) ? "true" : "false");

  printf("1/DBL_MID=%.18lf\n", 1/DBL_MIN);
  printf("0/DBL_MID=%.18lf\n", 0/DBL_MIN);
  printf("0+DBL_MID=%.18lf\n", 0+DBL_MIN);
  printf("1+DBL_MID=%.18lf\n", 1+DBL_MIN);

  printf("(0.0 == 0)=%s\n", (0.0 == 0) ? "true" : "false");
  printf("(0.0 == 0)=%s\n", (0.0 > 0) ? "true" : "false");
  printf("(0.0 == 0)=%s\n", (0.0000000000001 > 0) ? "true" : "false");

}
