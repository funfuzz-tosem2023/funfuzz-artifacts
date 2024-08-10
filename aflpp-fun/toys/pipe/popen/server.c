//
// Use popen to send data to a client
//
#include <stdio.h>
#include <time.h>
#include <unistd.h>
#include <stdlib.h>

int main(void) {

  FILE *fp = popen("python3 ./client.py", "w");

  if (fp == NULL) {

    printf("popen() failed!\n");
    exit(1);

  }

  // fopen succeed!

  int cnt = 5;
  char mes[50];

  while (cnt--) {

    sprintf(mes, "%lu, 1111%d 2222%d\n", time(NULL), cnt, cnt);

    fputs(mes, fp);
    fflush(fp);

    printf("[C] mes=%s\n", mes);
//    sleep(1);
    sleep(3); /* asynchronous? */

  }

  pclose(fp);

  printf("[C] finish time=%lu\n", time(NULL));

  return 0;

}
