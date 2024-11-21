#include <cstdlib>
#include "../include/stencil_kernel.h"

int main(int argc, char **argv) {
    stencil_kernelHandle_t handle;
    int err;
    long long N = 42;
    double * __restrict__ A = (double*) calloc(((N * N) * N), sizeof(double));
    double * __restrict__ B = (double*) calloc(((N * N) * N), sizeof(double));


    handle = __dace_init_stencil_kernel(N);
    __program_stencil_kernel(handle, A, B, N);
    err = __dace_exit_stencil_kernel(handle);

    free(A);
    free(B);


    return err;
}
