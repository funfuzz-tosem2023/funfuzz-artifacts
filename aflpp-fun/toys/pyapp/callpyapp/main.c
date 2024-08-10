//
// Try to fork and execute a python app
//
#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>
#include <sys/shm.h>

int main(void) {

  int pid = fork();

  if (pid == -1) {

    perror("fork error");
    exit(1);

  } else if (pid > 0) {

    // Parent: C process.
    printf("[CAPP] parent-process, pid=%d\n", pid);

  } else if (pid == 0) {

    // Child: PY process
    printf("[CAPP] child-process, pid=%d\n", pid);
    printf("[CAPP] childc-process, getpid=%d\n", getpid());

    execlp("python3", "python3", "app.py", NULL);

  }

  printf("[CAPP] orig-process, pid=%d (finish)\n", pid);

  return 0;

}

