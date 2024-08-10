#include <stdlib.h>
#include <stdio.h>

#include "common.h"

int main() {

  // https://stackoverflow.com/questions/17929414/how-to-use-setenv-to-export-a-variable-in-c
  // The setenv() function shall update or add a variable in the environment of
  // the calling process.
  setenv(SHM_ID, "test", 1);

  printf("getenv(%s)=%s\n", SHM_ID, getenv(SHM_ID));

  return 0;

}
