//
// Test ternary
//
#include <stdlib.h>
#include <stdio.h>

int main(int argc, char **argv) {

  if (argc < 1) {
    printf("Require at least 1 argument!");
    exit(1);
  }

  int mode = atoi(argv[1]);

  printf("%s! \nmode=%d \n", mode ? "Mode Correct" : "Mode Wrong", mode);

  return 0;

}

