import numpy as np
import time

def kernel(A, x):
    return (A @ x) @ A

def initialize(M, N, iter, device):
    dtype=np.float64
    M, N = 60, 60
    fn = dtype(N)

    x = np.fromfunction(lambda i: 1 + (i / fn), (N, ), dtype=dtype)
    A = np.fromfunction(lambda i, j: ((i + j) % N) / (5 * M), (M, N),
                        dtype=dtype)

    total_elapsed = 0
    for k in range(1, iter):
        start = time.perf_counter()
        result = kernel(A, x)
        elapsed = time.perf_counter() - start
        print(elapsed)
        total_elapsed =+ elapsed

    return total_elapsed/iter