//
// Simulate the fuzzer (afl++) which read coverage from shm
//
#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>
#include <time.h>
#include <sys/shm.h>

#include "common.h"

#define SHM_CNT     2
#define SWITCH_GAP  3

int main() {

  printf("[FUZZER] main()\n");

  int   *shm_ptr    = NULL;
  int   shm_ptr_id  = 0;
  int   shm_id[SHM_CNT];
  char  shm_id_str[SHM_CNT][20];
  long  last_tp, cur_tp, elapsed_sec;
  long  update_period = 5; // Update every 5 seconds

  // Build shm
  shm_id[0] = shmget(IPC_PRIVATE, 8, IPC_CREAT | IPC_EXCL | DEFAULT_PERMISSION);
  shm_id[1] = shmget(IPC_PRIVATE, 8, IPC_CREAT | IPC_EXCL | DEFAULT_PERMISSION);

  // Set id into env
  sprintf(shm_id_str[0], "%d", shm_id[0]);
  sprintf(shm_id_str[1], "%d", shm_id[1]);

  // Set shm_id[0] as initial
  setenv(SHM_ID, shm_id_str[0], 1);

  // Attach to SHMs and update value
  shm_ptr     = shmat(shm_id[0], NULL, 0);
  shm_ptr[0]  = 11111111;
  shm_ptr     = shmat(shm_id[1], NULL, 0);
  shm_ptr[0]  = 22222222;

  // Free it
  shm_ptr = NULL;

  // Mark the first update time point
  last_tp = time(NULL);

  // To see whether the map has been updated?
  printf("Get into loop\n");

  int cnt = 20;

  while (cnt--) {

    // Update time.
    cur_tp = time(NULL);
    elapsed_sec = cur_tp - last_tp;

    printf("[FUZZER] elapsed_sec %lu\n", elapsed_sec);

    // Switch shm_id if preset duration is reached.
    if (elapsed_sec >= SWITCH_GAP) {

      last_tp = cur_tp;
      shm_ptr_id = (shm_ptr_id + 1) % SHM_CNT;
      setenv(SHM_ID, shm_id_str[shm_ptr_id], 1);

      printf("[FUZZER] Switch SHM !!!\n");

    }

    // Fork and call PUT. (Why always fork?)
    int pid = fork();

    if (pid == 0) {

      // Run PUT on child process
      printf("[FUZZER] Execute PUT...\n");
      execv("./PUT.o", NULL);

    }

    sleep(1);

    printf("======================================================\n");

  }

}