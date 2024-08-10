#include <stdlib.h>
#include <stdio.h>

#include "common.h"

int main(int argc, char **argv) {

  printf("argc=%d\n", argc);

  if (getenv(SHM_ID))
    printf("%s, %s %s\n", argv[1], SHM_ID, getenv(SHM_ID));
  else
    printf("%s, No value set at `%s`\n", argv[1], SHM_ID);

  return 0;

}
