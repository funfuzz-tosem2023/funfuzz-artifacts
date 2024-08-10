//
// Test fork and wait
//
#include <stdio.h>
#include <unistd.h>

int main(void) {

  int cnt = 5;

  while (cnt--) {

    printf("[C] OK, I'm working (%d)...\n", cnt);

    sleep(1);

  }

}
