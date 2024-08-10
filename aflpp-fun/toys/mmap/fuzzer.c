//
// Simulate the fuzzer (afl++) which read coverage from shm (using mmap)
//
#include <stdio.h>
#include <unistd.h>
#include <fcntl.h>
#include <sys/mman.h>

#include "common.h"

#define DEFAULT_PERMISSION 0600

int main() {

  printf("fuzzer.c#main()\n");

  printf("fuzzer.c, build mmap_shm\n");
  // works with O_RDWR (open code), fails with O_RDONLY
  int fd = open(GCC_MMAP_FILE,      /* File path */
                O_RDWR | O_CREAT,   /* File Operation Permission */
                S_IRUSR | S_IWUSR   /* Owner Privacy */);

  // Set file size
  lseek(fd, 1024-1, SEEK_SET);
  write(fd, "", 1);

  // The mmap() function establishes a mapping between a process' address space and a file or shared memory object.
  char *shm_map = mmap(0, FSIZE, PROT_READ | PROT_WRITE, MAP_SHARED, fd, 0);

  int cnt = 6;
  while (cnt--) {

    // Fork and call PUT. (Why always fork?)
    int pid = fork();

    if (pid != 0) {

      printf("Check shm_map (mmap)...\n");
      printf("shm_map[0]=%d\n", shm_map[0]);

    } else {

      // Run PUT on child process
      printf("Run PUT...\n");
      execv("./PUT", NULL);

    }

    sleep(3);

    printf("======================================================\n");

  }

}