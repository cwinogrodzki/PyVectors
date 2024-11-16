import numpy as np
import time
import laplacian_numpy

TSTEPS=5

def kernel(A, B, N):
    # Skip boundary points
    for t in range(1, TSTEPS):
        print(t)
        print(B[1,1,])
        for k in range(1, N - 1):
            for j in range(1, N - 1):
                for i in range(1, N - 1):
                    # Apply stencil approximation of Laplacian to all interior points
                    A_xx = (A[i + 1, j, k] - 2 * A[i, j, k] + A[i - 1, j, k]) * 0.125
                    A_yy = (A[i, j + 1, k] - 2 * A[i, j, k] + A[i, j - 1, k]) * 0.125
                    A_zz = (A[i, j, k + 1] - 2 * A[i, j, k] + A[i, j, k - 1]) * 0.125
                    B[i, j, k] = A_xx + A_yy + A_zz
    return B

def initialize(N, iter, device):
    A = np.fromfunction(lambda i, j, k: (i + j + (N - k)) * 10 / N, (N, N, N),
                    dtype=np.float64)
    B = np.copy(A)
    A_ref = np.copy(A)
    B_ref = np.copy(B)

    # total_elapsed = 0
    # for k in range(1, iter):
    #     start = time.perf_counter()
    #     numpy_result = kernel(A, B, N)
    #     elapsed = time.perf_counter() - start
    #     print(elapsed)
    #     total_elapsed =+ elapsed
    
    # return total_elapsed/iter

    result = kernel(A, B, N)
    result_ref = laplacian_numpy.kernel(A_ref, B_ref)
    assert np.allclose(result, result_ref)
