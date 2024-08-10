//
// Print constants in IPC
//
#include <sys/shm.h>
#include <stdio.h>

int main() {

  printf("IPC_CREAT %o %d, IPC_EXCL %o %d, (IPC_CREAT | IPC_EXCL) %o %d, "
      "(IPC_CREAT | IPC_EXCL | 0600) %o %d,IPC_PRIVATE %d\n",
      IPC_CREAT, IPC_CREAT, IPC_EXCL, IPC_EXCL,
      IPC_CREAT | IPC_EXCL, IPC_CREAT | IPC_EXCL,
      IPC_CREAT | IPC_EXCL | 0600, IPC_CREAT | IPC_EXCL | 0600, IPC_PRIVATE);

  return 0;

}
