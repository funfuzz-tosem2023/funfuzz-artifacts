//
// Fork. Set env in parent process and get env in current process.
// Fork will generate two process (p1 and p2) from original process p0. Let
// p1 be the parent process and p2 the child. Both p1 and p2 will inherit the
// environments set in p0, but the setenv() in p1 cannot influence envs in p2
// (and vise versa).
//
#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>

#include "common.h"

#define ENV   "__TEST"

int main(void) {

  setenv(ENV, "test1", 1);
  printf("Set ENV (1)!\n");

  setenv(SHM_ID, "shm_test", 1);
  printf("Set SHM_ID (1)!\n");

  // Fork a children process
  int pid = fork();

  if ( pid == 0 ) {

    printf("This is being printed from the child process\n");
    printf("getenv(ENV)=`%s`\n", getenv(ENV));

    // execv()
//    char *argv[] = {"p_child, ", "$__SHM_ID"};
    char *argv[] = {"p_child"};
    execvp("echo", argv);

  } else {

    printf( "This is being printed in the parent process:\n"
        " - the process identifier (pid) of the child is %d\n", pid );

    printf("getenv(ENV)=`%s`\n", getenv(ENV));

    setenv(ENV, "test2", 1);
    printf("Set ENV (2)!\n");

    // execv()
//    char *argv[] = {"p_parent, ", "$__SHM_ID"};
    char *argv[] = {"p_parent"};
    execvp("echo", argv);

  }

}
