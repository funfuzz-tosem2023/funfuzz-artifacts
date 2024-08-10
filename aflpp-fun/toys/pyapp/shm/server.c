//
// Communicate with pyclient through SHM
//
#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>
#include <sys/shm.h>

#define SHM_ENV "__SHM_ID"

#define cMGN "\x1b[0;35m"
#define cRST "\x1b[0m"

int main(void) {

  // Build up shm
  int shm_id = shmget(IPC_PRIVATE, 8, IPC_CREAT | IPC_EXCL | 0600);
  perror("error shmget ");
  int *shm;

  int pid = fork();

  if (pid == -1) {

    perror(cMGN "[CAPP] " cRST "fork error");
    exit(1);

  }
  else if (pid > 0) {

    // Parent: C process.
    printf(cMGN "[CAPP] " cRST "parent-process, pid=%d\n", pid);

    int cnt = 6;
    while (cnt) {

      // Undefined error if we do not attach to the shm and write sth into it.
      // I guess this is the so-called "being discarded".
      shm = shmat(shm_id, NULL, 0);
      shm[0] = --cnt;
      printf(cMGN "[CAPP] " cRST "write shm: shm[0]=%d\n", shm[0]);

      sleep(1);

    }

  }
  else if (pid == 0) {

    // Child: PY process
    printf(cMGN "[CAPP] " cRST "child-process, pid=%d\n", pid);
    printf(cMGN "[CAPP] " cRST "childc-process, getpid=%d\n", getpid());

    // Prepare environments
    char id_env[20];
    char *envp[] = {id_env, NULL};
    sprintf(id_env, "%s=%d", SHM_ENV, shm_id);
    printf(cMGN "[CAPP] " cRST "id_env %s\n", id_env);

    /// Use: int execle(const char *path, const char *arg, ..., char *const envp[] );
    execle("/Users/adian/.conda/envs/aflfun/bin/python3", "python3", "client.py", NULL, envp); // works
    perror("error exec ");


  }

  // Detach
  shmdt(shm);

  // http://www.csl.mtu.edu/cs4411.ck/www/NOTES/process/shm/shmdt.html
  // To remove a shared memory, use shmctl().
  shmctl(shm_id, IPC_RMID, NULL);

  return 0;

}

