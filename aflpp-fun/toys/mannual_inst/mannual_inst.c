//
// Code snippet simulate instrumentation on direct calls. In this example, we
// choose `puts` and `strtol` as they will not be optimized by llvm/clang.
//

#include <stdio.h>
#include <stdlib.h>

// Show "unused" when not commented, but cannot compile without this header.
//#include "extern.h"

// Declaration. main: 1, puts: 2, strtol: 3, putchar: 4
extern int *area_ptr;

int main() {

  // Call `puts` and update counter.
  puts("Hello world!");
  ++area_ptr[1 * 4 + 1];

  // Call `strtol` and update counter.
  int exclCode = strtol("33", NULL, 10);
  ++area_ptr[1 * 4 + 2];
  int nlCode = strtol("10", NULL, 10);
  ++area_ptr[1 * 4 + 2];

  // Call `putchar` to prevent strtol from being omitted.
  putchar(exclCode);
  ++area_ptr[1 * 4 + 3];
  putchar(nlCode);
  ++area_ptr[1 * 4 + 3];

  return 0;
}
