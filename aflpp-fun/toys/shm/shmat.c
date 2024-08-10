//
// Examine map_id allocated by shmat
//
#include <sys/shm.h>
#include <stdio.h>
#include <stdlib.h>

typedef uint32_t u32;
typedef uint64_t u64;


int main() {

  // Allocate two shms.
  int shm_id1 = shmget(IPC_PRIVATE, 100, IPC_CREAT | IPC_EXCL | 0600);
  int shm_id2 = shmget(IPC_PRIVATE, 100, IPC_CREAT | IPC_EXCL | 0600);
  printf("shm_id1=%d, shm_id2=%d\n", shm_id1, shm_id2);

  // A zero address
  u64 addr = 0;
  printf("addr=0x%llx\n", addr);
  // `(void *) addr == NULL` if `addr==0`, else `(void *) addr != NULL`
//  if ((void *) addr == NULL) printf("(void *) addr is NULL!\n");
//  else                         printf("(void *) addr not NULL!\n");

  // Attach
  u32 *shm1       = shmat(shm_id1, (void *) addr, 0);
  u32 *shm1_null  = shmat(shm_id1, NULL, 0);
  u32 *shm2       = shmat(shm_id2, (void *) addr, 0);
  u32 *shm2_null  = shmat(shm_id2, NULL, 0);

  // Show ptrs.
  printf("shm1_p=%p, shm1_null_p=%p, shm2_p=%p, shm2_null_p=%p\n",
         shm1, shm1_null, shm2, shm2_null);

  return 0;
}