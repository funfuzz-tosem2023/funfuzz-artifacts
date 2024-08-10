//
// Define and assign an extern
//
#include <stdio.h>
#include <unistd.h>

#include "extern.h"

extern int *exptr;

int main() {

  int cnt = 0;

  while (1) {
    // Never stop.
    sleep(1);
    printf("ass: *exptr=%d\n", *exptr);
    printf("ass: exval=%d\n", exval);
    *exptr = ++cnt;
  }

}
