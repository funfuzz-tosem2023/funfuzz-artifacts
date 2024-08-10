//
// Test fork and wait
//
#include <unistd.h>
#include <stdlib.h>
#include <stdio.h>

int main(void) {

  int child_status;

  int pid = fork();

  if (pid == 0) {

    // Child: execute
    execl("./child.o", "./child.o", NULL);

  } else {

    // Parent: wait child to finish.
    printf("[P] Go to work! I'll wait for you...\n");
    waitpid(pid, &child_status, 0);

  }

  printf("[P] Yeah! Now we have both finished!\n");

}
