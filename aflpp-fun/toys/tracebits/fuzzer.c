//
// Simulate the fuzzer (afl++) which read coverage from shm
//
#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>
#include <sys/shm.h>

#include "common.h"

#define DEFAULT_PERMISSION 0600

int main() {

  printf("fuzzer.c#main()\n");

  int   *shm_map = NULL;
  int   shm_id;
  char  shm_id_str[20];

  // Build shm
  shm_id = shmget(IPC_PRIVATE, 8, IPC_CREAT | IPC_EXCL | DEFAULT_PERMISSION);
  printf("Get shm_id=%d\n", shm_id);

  // Set id into env
  sprintf(shm_id_str, "%d", shm_id);
  printf("sprintf(), shm_id_str=%s\n", shm_id_str);
  setenv(SHM_ID, shm_id_str, 1);
  printf("Set `%s` at `%s`\n", shm_id_str, SHM_ID);

  // Attach to the shm
  shm_map = shmat(shm_id, NULL, 0);
  printf("shm_map-p=%p\n", shm_map);

  // To see whether the map has been updated?
  printf("Get into loop\n");

  int cnt = 6;

  while (cnt--) {

    // Fork and call PUT. (Why always fork?)
    int pid = fork();

    if (pid != 0) {

      printf("Check shm_map...\n");
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