//
// Test strol
//
#include <stdio.h>
#include <stdlib.h>

int main(int argc, char **argv) {
  char *input = argv[1];
  long number = strtol(input, NULL, 10);

  printf("input=%s\n", input);
  printf("number=%ld\n", number);

  return 0;
}