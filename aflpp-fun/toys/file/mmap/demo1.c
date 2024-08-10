//
// A mmap demo
//
#include <stdio.h>
#include <fcntl.h>
#include <ctype.h>
#include <stdlib.h>
#include <unistd.h>
#include <string.h>
#include <sys/mman.h>

#define SHM_LEN 100

char *trim(char *str) {
  char *end;

  // Trim leading space
  while(isspace((unsigned char)*str)) str++;

  if(*str == 0)  // All spaces?
    return str;

  // Trim trailing space
  end = str + strlen(str) - 1;
  while(end > str && isspace((unsigned char)*end)) end--;

  // Write new null terminator character
  end[1] = '\0';

  return str;
}

int main(int argc, char **argv) {

  char *path = "./demo1.txt";

  int   fd;
  char *shm;

  fd = open(path, O_RDWR | O_CREAT);
  shm = mmap(NULL, SHM_LEN, PROT_READ | PROT_WRITE, MAP_SHARED, fd, 0);
  write(fd, "\0", SHM_LEN);
  close(fd);

  // Read or write...
  char *mode = argv[1];

  if (!strcmp(mode, "read")) {

    while (1) {
      printf("shm=%s\n", shm);
      trim(shm);
      long num = strtol(shm, NULL, 10);
//      char *trim_shm = trim(shm);
//      long num = strtol(trim_shm, NULL, 10);
      printf("num=%ld\n", num);
      sleep(3);
    }

  } else if (!strcmp(mode, "write")) {

    while (1) {
      fgets(shm, SHM_LEN, stdin);
    }

  } else {

    printf("Unrecognized command\n");

  }


}
