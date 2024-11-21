#include <cstdlib>
#include "../include/atax.h"

int main(int argc, char **argv) {
    ataxHandle_t handle;
    int err;
    double * __restrict__ A = (double*) calloc(4200, sizeof(double));
    double * __restrict__ __return = (double*) calloc(70, sizeof(double));
    double * __restrict__ x = (double*) calloc(70, sizeof(double));


    handle = __dace_init_atax();
    __program_atax(handle, A, __return, x);
    err = __dace_exit_atax(handle);

    free(A);
    free(__return);
    free(x);


    return err;
}
