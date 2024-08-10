//
// Test afl powerof2
//
#include <stdio.h>

#define powerof2(x)     ((((x)-1)&(x))==0)

int main (void) {

  int a = 25;

  printf("%d\n", powerof2(a));

}