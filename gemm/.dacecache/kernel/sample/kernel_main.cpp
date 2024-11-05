#include <cstdlib>
#include "../include/kernel.h"

int main(int argc, char **argv) {
    kernelHandle_t handle;
    int err;
    double alpha = 42;
    double beta = 42;
    double * __restrict__ A = (double*) calloc(4800, sizeof(double));
    double * __restrict__ B = (double*) calloc(5600, sizeof(double));
    double * __restrict__ C = (double*) calloc(4200, sizeof(double));


    handle = __dace_init_kernel();
    __program_kernel(handle, A, B, C, alpha, beta);
    err = __dace_exit_kernel(handle);

    free(A);
    free(B);
    free(C);


    return err;
}
