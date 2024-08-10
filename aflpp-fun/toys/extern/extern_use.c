//
// Define and assign an extern
//
#include <stdio.h>
#include <unistd.h>

#include "extern.h"

extern int *exptr;

int main() {

  while (1) {
    // Never stop.
    sleep(1);
    printf("use: *exptr=%d\n", *exptr);
    printf("use: exval=%d\n", exval);

  }

}
