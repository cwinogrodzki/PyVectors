import numpy as np
import time
import gemm_numpy

def kernel(alpha, beta, A, B, C):
    Ni, Nk = A.shape
    Nk, Nj = B.shape

    # C[:] = alpha * A @ B + beta * C
    for i in range(1, Ni):
        for j in range(1, Nj):
            result = 0
            for k in range(1, Nk):
                result += A[i, k] * B[k, j]
            C[i, j] = alpha * result + beta * C[i, j]
    
    return C


def initialize(Ni, Nj, Nk, iter, device):
    dtype=np.float64
    alpha = dtype(1.5)
    beta = dtype(1.2)

    A = np.fromfunction(lambda i, k: (i * (k + 1) % Nk) / Nk, (Ni, Nk),
                        dtype=dtype)
    B = np.fromfunction(lambda k, j: (k * (j + 2) % Nj) / Nj, (Nk, Nj),
                        dtype=dtype)
    C = np.fromfunction(lambda i, j: ((i * j + 1) % Ni) / Ni, (Ni, Nj),
                        dtype=dtype)
    C_ref = np.copy(C)

    # total_elapsed = 0
    # for k in range(1, iter):
    #     start = time.perf_counter()
    #     C = kernel(alpha, beta, A, B, C)
    #     elapsed = time.perf_counter() - start
    #     print(elapsed)
    #     total_elapsed =+ elapsed

    # return total_elapsed/iter

    C = kernel(alpha, beta, A, B, C)
    C_ref = gemm_numpy.kernel(alpha, beta, A, B, C_ref)
    print(C, C_ref)
    #assert np.allclose(C, C_ref)