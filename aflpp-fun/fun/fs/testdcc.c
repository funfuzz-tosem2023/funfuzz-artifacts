//
// Test FS computation component
//

#include <stdlib.h>
#include <stdio.h>
#include <unistd.h>
#include <signal.h>
#include <memory.h>
#include <time.h>
#include <sys/shm.h>
#include <sys/wait.h>

#define LOG_TITLE "[FUN-TEST]"
#define ECODE     10086
#define cGRN      "\x1b[0;32m"
#define cRST      "\x1b[0m"

typedef unsigned long long  u64;
typedef unsigned int        u32;
typedef int                 s32;


u32 get_fun_shm_len1d(char *tmpdir) {

  const char *FUNC_INFO = "funcInfo";

  // Declarations.

  FILE *fp;
  char  fpath[100];
  int   lcnt = 0;   /* Counter for lines */

  // Locate function file.

  sprintf(fpath, "%s%c%s", tmpdir, '/', FUNC_INFO);
  printf("%s funcInfo: `%s`\n", LOG_TITLE, fpath);

  // Open funcInfo file and count lines. Each line is info for a function
  // in format <funName>, <funcID>, e.g, "main,123". Note that funcInfo
  // file should only have one empty line as the last.

  fp = fopen(fpath, "r");

  // Sanitize
  if (fp == NULL) {
    printf("%s Cannot open funcInfo file `%s`!\n", LOG_TITLE, fpath);
    exit(ECODE);
  }

  // Increment count if this character is newline
  for (char c = (char) getc(fp); c != EOF; c = (char) getc(fp))
    if (c == '\n') lcnt = lcnt + 1;

  fclose(fp);

  // lcnt == func_num iff the last line is empty.
  // We hope shm_len1d == func_num + 1
  return lcnt + 1;

}

pid_t init_dcc(char *tmpdir, s32 *infdptr, s32 *outfdptr) {

#define RD 0   /* The pipe position prepared for reading */
#define WT 1   /* The pipe position prepared for writing */

  int p_stdin[2], p_stdout[2];
  pid_t pid;

  /*
    int pipe(int fds[2]);
    Parameters: fd[0] will be the fd(file descriptor) for the read end of pipe.
                fd[1] will be the fd for the write end of pipe.
    Returns: 0 on Success, -1 on error.
   */
  // Build pipes on stdin and stdout
  if (pipe(p_stdin) != 0 || pipe(p_stdout) != 0) {

    printf("%s init_dcc(), pipe error\n", LOG_TITLE);
    exit(ECODE);

  }

  // Fork to run sub program
  pid = fork();

  if (pid < 0) {

    printf("%s init_dcc(), fork() error\n", LOG_TITLE);
    exit(ECODE);

  } else if (pid == 0) {

    // Child process: start dcc.

    /*
       int dup(int oldfd);

       The dup() system call allocates a new file descriptor that refers
       to the same open file description as the descriptor oldfd.

       int dup2(int oldfd, int newfd);

       The dup2() system call performs the same task as dup(), but instead
       of using the lowest-numbered unused file descriptor, it uses the file
       descriptor number specified in newfd.
    */

    // Redirect stdin and stdout
    close(p_stdin[WT]);
    dup2(p_stdin[RD], RD);

    close(p_stdout[RD]);
    dup2(p_stdout[WT], WT);

    // Start dcc process. For testing, we use tmpdir to replace out_dir
    execlp("python3", "python3", "dyn_compute_fs.py", tmpdir, tmpdir, NULL);

    perror("[FUN-TEST] init_dcc(), exec() failed");
    exit(ECODE);

  }

  // Pass fds out through side effects.
  if (infdptr == NULL)
    close(p_stdin[WT]);
  else
    *infdptr = p_stdin[WT];

  if (outfdptr == NULL)
    close(p_stdout[RD]);
  else
    *outfdptr = p_stdout[RD];

  // Return the pid of dcc process.
  return pid;

}


int main(int argc, char **argv) {

  s32     cc_shm_id, fs_shm_id;
  u64     *cc_shm;
  double  *fs_shm;
  u32     shm_len1d, shm_len2d;
  u32     cc_shm_size, fs_shm_size;

  // Prepare fun_tmpdir
  char  *fun_tmpdir = argv[1];
  printf("%s fun_tmpdir %s\n", LOG_TITLE, fun_tmpdir);

  // Read shm size
  shm_len1d   = get_fun_shm_len1d(fun_tmpdir);
  shm_len2d   = shm_len1d * shm_len1d;
  cc_shm_size = shm_len2d * sizeof(u64);
  fs_shm_size = shm_len1d * sizeof(double);
  printf("%s shm_len1d %u, shm_len2d %u, cc_shm_size %u, fs_shm_size %u\n",
      LOG_TITLE, shm_len1d, shm_len2d, cc_shm_size, fs_shm_size);

  // Build shm
  cc_shm_id = shmget(IPC_PRIVATE, cc_shm_size, IPC_CREAT | IPC_EXCL | 0600);
  fs_shm_id = shmget(IPC_PRIVATE, fs_shm_size, IPC_CREAT | IPC_EXCL | 0600);
  printf("%s cc_shm_id %d, fs_shm_id %d\n", LOG_TITLE, cc_shm_id, fs_shm_id);

  if (cc_shm_id == -1 || fs_shm_id == -1) {

    printf("%s shmget failed!\n", LOG_TITLE);

    // Free shm to avoid memory leak.
    shmdt(cc_shm);
    shmctl(cc_shm_id, IPC_RMID, 0);
    shmdt(fs_shm);
    shmctl(fs_shm_id, IPC_RMID, 0);

    exit(ECODE);

  }

  // shmat
  cc_shm = shmat(cc_shm_id, NULL, 0);
  fs_shm = shmat(fs_shm_id, NULL, 0);

  // Initialize SHMs
//  for (u32 i = 0; i < shm_len2d; ++i) cc_shm[i] = 1;
  memset(cc_shm, 0, cc_shm_size);
  memset(fs_shm, 0, fs_shm_size);
  printf("%s After init SHMs, cc_shm[%d] %llu, fs_shm[0] %lf\n",
         LOG_TITLE, shm_len2d - 1, cc_shm[shm_len2d - 1], fs_shm[0]);

  // Fork and startup FS computation component.
  s32 infd = -1;
  pid_t dcc_pid = init_dcc(fun_tmpdir, &infd, NULL);

  if (infd == -1) {
    
    printf("%s Init DCC failed!", LOG_TITLE);
    
    // Free shm to avoid memory leak.
    shmdt(cc_shm);
    shmctl(cc_shm_id, IPC_RMID, 0);
    shmdt(fs_shm);
    shmctl(fs_shm_id, IPC_RMID, 0);

    exit(ECODE);
    
  }

  // Build pipe to dcc process
  FILE *dcc_infp = fdopen(infd, "w");

  if (dcc_infp == NULL) {

    printf("%s fdopen(infd) failed!", LOG_TITLE);

    // Free shm to avoid memory leak.
    shmdt(cc_shm);
    shmctl(cc_shm_id, IPC_RMID, 0);
    shmdt(fs_shm);
    shmctl(fs_shm_id, IPC_RMID, 0);

    exit(ECODE);

  }


  u32 cnt = 2;

  // Initialize
  srand(time(NULL));

  while (cnt--) {

    // Periodically empty fs_shm, update cc, run dcc and check fs_shm[last]

    // Empty fs_shm
    printf("%s Refresh cc_shm and fs_shm.....\n", LOG_TITLE);
    memset(cc_shm, 0, cc_shm_size);
    memset(fs_shm, 0, fs_shm_size);
    printf("%s cc_shm[0] %llu, fs_shm[1] %lf.\n",
           LOG_TITLE, cc_shm[0], fs_shm[1]);

    // Update cc_shm. Set 1/10 the edges to 1
    for (int i = 1; i < shm_len1d; ++i) {
      for (int j = 1; j < shm_len1d; ++j) {
        u32 val = rand() % 10 + 1;
        if (rand() % 10 > 4) // 0~9
          continue ;
        int callerIdx = i * shm_len1d;
        int crIdx     = callerIdx + j;
        cc_shm[0]         += val;
        cc_shm[callerIdx] += val;
        cc_shm[crIdx]     =  val;
      }
    }


    printf("%s After updating cc_shm, cc_shm[0] %llu, cc_shm[%u] %llu\n",
           LOG_TITLE, cc_shm[0], shm_len2d - 1, cc_shm[shm_len2d - 1]);
    printf("%s After updating cc_shm, cc_shm[1][2] %llu, cc_shm[1][0] %llu\n",
           LOG_TITLE, cc_shm[1 * shm_len1d + 2], cc_shm[1 * shm_len1d + 0]);

    // Send id to make dcc work
    printf("%s Send shm_ids to make dcc work.....\n", LOG_TITLE);
    fprintf(dcc_infp, "%d,%d\n", cc_shm_id, fs_shm_id);
    fflush(dcc_infp);

    // Wait for dcc component to finish centrality analysis...
    printf("%s Wait for dcc component.....\n", LOG_TITLE);
//    int status;
    pid_t wait_dcc;
    u32 time_elapsed = 0, dura = 1;
    while (!fs_shm[0]) { // Use addr-0 to perform the flag of a complete update

      // Check if dcc alive
//      wait_dcc = waitpid(dcc_pid, &status, WNOHANG);
      wait_dcc = waitpid(dcc_pid, NULL, WNOHANG);

      if (wait_dcc == -1) {
        // DCC has already died!
        printf("%s DCC has already died! \n", LOG_TITLE);

        shmdt(cc_shm);
        shmctl(cc_shm_id, IPC_RMID, 0);
        shmdt(fs_shm);
        shmctl(fs_shm_id, IPC_RMID, 0);

        exit(ECODE);
      }

      printf("%s Waiting reading fs_vals, elapsed time: %d ...\n",
             LOG_TITLE, time_elapsed);

      sleep(dura);
      time_elapsed += dura;

    }

    printf("%s Check fs_vals, fs_shm[1] %.18lf, fs_shm[%u] %.18lf\n",
           LOG_TITLE, fs_shm[1], shm_len1d-1, fs_shm[shm_len1d-1]);

    sleep(1);
  }

  // Release everything

  // Kill the dcc subprocess
  printf("%s Kill dcc component.....\n", LOG_TITLE);
  kill(dcc_pid, SIGKILL);

  // Free shm to avoid memory leak.
  printf("%s Release SHMs.....\n", LOG_TITLE);
  shmdt(cc_shm);
  shmctl(cc_shm_id, IPC_RMID, 0);
  shmdt(fs_shm);
  shmctl(fs_shm_id, IPC_RMID, 0);
  
  printf("%s " cGRN ".....OK, test finished :-)\n" cRST, LOG_TITLE);

}

