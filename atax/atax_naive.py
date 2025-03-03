import numpy as np
import time
import atax_numpy

dtype=np.float64

def kernel(A, x, y, tmp):
    M, N = A.shape
    for i in range(0, M):
        for j in range(0, N):
            tmp[i] = tmp[i] + A[i, j] * x[j]

        for j in range(0, N):
            y[j] = y[j] + A[i, j] * tmp[i]

    return y

def initialize(M, N, iter, device):
    fn = dtype(N)
    
    y = np.zeros(N)
    tmp = np.zeros(M)
    x = np.fromfunction(lambda i: 1 + (i / fn), (N, ), dtype=dtype)
    A = np.fromfunction(lambda i, j: ((i + j) % N) / (5 * M), (M, N),
                        dtype=dtype)

    total_elapsed = 0
    for k in range(1, iter):
        start = time.perf_counter()
        result = kernel(A, x, y, tmp)
        elapsed = time.perf_counter() - start
        print(elapsed)
        total_elapsed =+ elapsed

    return total_elapsed/iter

    # result = kernel(A, x, y, tmp)
    # ref_result = atax_numpy.kernel(A, x)
    # assert np.allclose(result, ref_result)