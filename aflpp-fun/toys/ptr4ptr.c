//
// How to make a ptr for ptr?
//
#include <stdio.h>

void change_ptr4ptr(int **ptr4ptr) {

  int s_area[1]  = {10086};
  int *s_ptr     = s_area;

//  ptr4ptr = (int **) &s_area; // (x) The value of ptr4ptr will not pass out.
//  *ptr4ptr = s_area; // Can get pass the address of s_area out.
  *ptr4ptr = s_ptr; // Equal to the upper line.

}

int main() {

  int area[1]   = {0};
  int *ptr      = area;
  int **ptr4ptr = &ptr;

  printf("Before:\t %d\n", *ptr4ptr[0]);
  change_ptr4ptr(ptr4ptr);
  printf("After:\t %d\n", *ptr4ptr[0]);

}
