//
// Use popen to send data to a client
//
#include <stdio.h>
#include <time.h>
#include <unistd.h>
#include <stdlib.h>
#include <signal.h>

#ifdef __linux__
  #define PYTHON "/usr/bin/python3"
#endif

#ifdef __APPLE__
  #define PYTHON "/opt/homebrew/bin/python3.9"
#endif

pid_t popen2(int *infdptr, int *outfdptr) {

#define READ  0   /* The pipe position prepared for reading */
#define WRITE 1   /* The pipe position prepared for writing */

  int p_stdin[2], p_stdout[2];
  pid_t pid;

  if (pipe(p_stdin) < 0 || pipe(p_stdout) < 0) {

    printf("pipe() error.\n");
    exit(10086);

  }

  // Fork to run sub program
  pid = fork();

  if (pid < 0) {

    printf("fork() error.\n");
    exit(10086);

  }else if (pid == 0) {

    // Child process

    /*
       int dup(int oldfd);

       The dup() system call allocates a new file descriptor that refers
       to the same open file description as the descriptor oldfd.

       int dup2(int oldfd, int newfd);

       The dup2() system call performs the same task as dup(), but instead
       of using the lowest-numbered unused file descriptor, it uses the file
       descriptor number specified in newfd.
    */

    close(p_stdin[WRITE]);
    dup2(p_stdin[READ], READ);

    close(p_stdout[READ]);
    dup2(p_stdout[WRITE], WRITE);

    execlp("python3", "python3", "./client.py", NULL); // works on mac
//    execl(PYTHON, "python3", "./client.py", NULL); // works on mac
    perror("execl");

    exit(1);

  }

  // Side-effects
  if (infdptr == NULL)
    close(p_stdin[WRITE]);
  else
    *infdptr = p_stdin[WRITE];

  if (outfdptr == NULL)
    close(p_stdout[READ]);
  else
    *outfdptr = p_stdout[READ];

  return pid;
}

int main(void) {

  int infd = -1, outfd = -1;

  printf("[C] Before popen2(), infd=%d, &infd=%p, outfd=%d, &outfd=%p\n",
         infd, &infd, outfd, &outfd);

  int pid = popen2(&infd, NULL);

  if (infd == -1) {

    printf("popen2() failed!\n");
    exit(1);

  }

  printf("[C] After popen2(), infd=%d, &infd=%p, outfd=%d, &outfd=%p\n",
         infd, &infd, outfd, &outfd);

  // fopen succeed!
//  FILE *fp = fdopen(outfd, "w");    // Write to stdin, read from stdout
  FILE *fp = fdopen(infd, "w"); // Write to stdin, read from stdout

  int cnt = 10;
//  int cnt = 30;

  while (cnt--) {

    printf("[C] loop(%d), 1111%d 2222%d\n", cnt, cnt, cnt);

    fprintf(fp, "%lu, 1111%d 2222%d\n", time(NULL), cnt, cnt);
    fflush(fp);

    sleep(1);
//    sleep(3); /* asynchronous? */

  }


  printf("[C] finish time=%lu\n", time(NULL));

  printf("[C] Kill the script...\n");
  kill(pid, SIGTERM);

  return 0;

}
