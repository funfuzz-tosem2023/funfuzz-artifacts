#include "stdio.h"


int main(int argc, char **argv) {

  char *ptr = NULL;
  ptr = argv[0];
  ptr += 5;
  printf("ptr=%s\n", ptr);

  return 0;

}
