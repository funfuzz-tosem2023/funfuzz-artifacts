//
// Simulate the instrumented PUT
//
#include <stdio.h>

// Monitor the ptr to area
extern int *__area_ptr;

int main() {

  printf("PUT#main(), Update value in __area_ptr (%p)\n", __area_ptr);
  ++__area_ptr[0];

  return 0;

}
