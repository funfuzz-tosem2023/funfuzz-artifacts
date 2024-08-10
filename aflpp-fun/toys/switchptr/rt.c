//
// Runtime code switch ptr
//
#include <stdlib.h>
#include <stdio.h>
#include <sys/shm.h>
#include "common.h"

#define ID 2

static int shm_area_init[1];

int  *area_ptr = shm_area_init;

__attribute__((constructor(0)))
void shm_map() {

  printf("[RT] remap shm...\n");

  int shm_id = atoi(getenv(SHM_ID));
  area_ptr = shmat(shm_id, NULL, 0);

}
