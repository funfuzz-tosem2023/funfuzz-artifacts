//
// Test macro instructions
//
#include <stdio.h>
#include <stdlib.h>

int main(void) {

  if (getenv("MACRO")) { // Same as use if-else directly.
#define USEMACRO
  }

#ifdef USEMACRO

  printf("The world has been controled by MACRO!!!\n");

#else

  printf("Hello world!\n");

#endif

  return 0;

}
