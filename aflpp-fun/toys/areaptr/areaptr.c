//
// Test aflpp-fun instrumentation
//
#include <stdio.h>

#define cCYA "\x1b[0;36m"
#define cRST "\x1b[0m"

static int cnt = 0;

void inline show() {

  printf(cCYA "CALL_SHOW(%d)\n" cRST, ++cnt);

}

int main(void) {

  show();
  show();
  show();
  show();

  return 0;

}

