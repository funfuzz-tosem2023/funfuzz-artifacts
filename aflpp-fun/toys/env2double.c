#include <stdlib.h>
#include <stdio.h>
#include <unistd.h>

int main(int argc, char ** argv) {

    double rho = strtod(getenv("RHO"), NULL);
    printf("rho=%lf\n", rho);
    
    return 0;
}
