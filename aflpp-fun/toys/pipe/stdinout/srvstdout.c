//
// Write to stdin, get from py client
//
#include <stdio.h>
#include <unistd.h>

#define BUFFER_SIZE 1024

typedef unsigned char u8;

int main(void) {

  u8 buffer[BUFFER_SIZE] = {
      '0',
      'H', 'e', 'l', 'l', 'o'
  };

  int cnt = 5;

  while (cnt--) {

    fwrite(buffer, sizeof(u8), BUFFER_SIZE,  stdout);

    buffer[0] = (u8) (cnt + '0');

    sleep(1);

  }

}
