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
  int *shm;

  int pid = fork();

  if (pid == -1) {

    perror(cMGN "[CAPP] " cRST "fork error");
    exit(1);

  } else if (pid > 0) {

    // Parent: C process.
    printf(cMGN "[CAPP] " cRST "parent-process, pid=%d\n", pid);

    int cnt = 6;
    while (cnt) {

      printf(cMGN "[CAPP] " cRST "write shm\n");

      shm = shmat(shm_id, NULL, 0);
      shm[0] = --cnt;

      sleep(1);

    }

  } else if (pid == 0) {

    // Child: PY process
    printf(cMGN "[CAPP] " cRST "child-process, pid=%d\n", pid);
    printf(cMGN "[CAPP] " cRST "childc-process, getpid=%d\n", getpid());

    // Prepare environments
    char id_env[20];
    char *envp[] = {id_env, NULL};
    sprintf(id_env, "%s=%d", SHM_ENV, shm_id);
    printf(cMGN "[CAPP] " cRST "id_env %s\n", id_env);

    /// Use: int execve( const char *file, char *const argv[], char *const envp[] );
//    // Prepare arguments
//    char *argv[] = {"/Users/adian/.conda/envs/aflfun/bin/python3", "client.py", NULL}; // works
//    char *argv[] = {"python3", "client.py", NULL}; //: No such file or directory
//    printf("argv %p, &argv[0] %p\n", argv, &argv[0]);
//
//    // Execute
//    execve(argv[0], argv, envp);
//    perror("error exec\n");

    /// Use: int execle(const char *path, const char *arg, ..., char *const envp[] );
//    execle("python3", "python3", "client.py", NULL, envp); //: No such file or directory
//    execle("/Users/adian/.conda/envs/aflfun/bin/python3", "python3", "client.py", NULL, envp); // works
//    perror("error exec\n");

    /// exec ls?
//    execle("ls", "ls", "client.py", NULL, envp); //: No such file or directory
//    execle("/bin/ls", "ls", "client.py", NULL, envp); // works
//    perror("error exec\n");
//    char *argv[] = {"ls", "client.py", NULL}; //: No such file or directory
    char *argv[] = {"/bin/ls", "client.py", NULL}; //: No such file or directory
    execve(argv[0], argv, envp);
    perror("error exec\n");
  }

  // Detach
  shmdt(shm);

  return 0;

}

