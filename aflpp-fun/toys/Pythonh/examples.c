//
// Examples using Python.h
//
#include <Python.h>

/// Run a simple code
void exec_pycode(const char* code) {
  Py_Initialize();
  PyRun_SimpleString(code);
  Py_Finalize();
}

int main(void) {

  exec_pycode("print('[PY.h] hello world!!!')");

}
