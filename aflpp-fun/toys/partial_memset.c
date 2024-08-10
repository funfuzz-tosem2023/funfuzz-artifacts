//
// Test memset partially
//
#include <stdio.h>
#include <memory.h>

int main(void) {

  int arr[10];

  memset(arr, 1, 10 * sizeof(int));

  for (int i = 0; i < 10; ++i) {
    printf("%d ", arr[i]);
  }
  printf("\n");

  // memset partially.
//  memset(&arr[5], 0, 5 * sizeof(int));
  memset(arr+1, 0, 5 * sizeof(int)); /* Set bytes at arr[1] ~ arr[5] to 0 */

  for (int i = 0; i < 10; ++i) {
    printf("%d ", arr[i]);
  }
  printf("\n");

}
