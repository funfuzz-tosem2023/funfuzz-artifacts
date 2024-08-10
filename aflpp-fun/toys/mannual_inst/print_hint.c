//
// Print some hints using instrumentation
//
#include <stdio.h>

int main(void) {
  puts("Wow! We have instrumented a call!");

  int arr[3] = {1, 2, 3};
  printf("arr[0]=%d\n", arr[0]);
//  printf("__fun_area_ptr[0]=%d\n", arr[0]);

  return 0;
}
