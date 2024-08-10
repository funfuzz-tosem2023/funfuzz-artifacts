//
// Test what is received by py script if we pass relative path
//
#include <stdio.h>
#include <unistd.h>

#ifdef __linux__
  #define PYTHON "/usr/bin/python3"
#endif

#ifdef __APPLE__
  #define PYTHON "/opt/homebrew/bin/python3.9"
#endif

int main(void) {

  char *relative_path = "./test";
  char *relative_path1 = "test";
  char *absolute_path = "/usr";

  printf("[C] We pass relative path0 like: `%s`\n", relative_path);
  printf("[C] We pass relative path1 like: `%s`\n", relative_path1);
  printf("[C] We pass absolute path like: `%s`\n", absolute_path);

  execlp("python3", "python3", "./py/script.py",
         relative_path, relative_path1, absolute_path, NULL);


}
