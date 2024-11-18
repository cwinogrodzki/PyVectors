import numpy as np
import time

TSTEPS = 5
def kernel(A, B):
    for t in range(1, TSTEPS):
        B[1:-1, 1:-1] = 0.2 * (A[1:-1, 1:-1] + A[1:-1, :-2] + A[1:-1, 2:] + A[2:, 1:-1] + A[:-2, 1:-1])
        A[1:-1, 1:-1] = 0.2 * (B[1:-1, 1:-1] + B[1:-1, :-2] + B[1:-1, 2:] + B[2:, 1:-1] + B[:-2, 1:-1]) 
    return A

def initialize(N, iter, device):
    dtype=np.float64

    A = np.fromfunction(lambda i, j: i * (j + 2) / N, (N, N), dtype=dtype)
    B = np.fromfunction(lambda i, j: i * (j + 3) / N, (N, N), dtype=dtype)

    total_elapsed = 0
    for k in range(1, iter):
        start = time.perf_counter()
        numpy_result = kernel(A, B, N)
        elapsed = time.perf_counter() - start
        print(elapsed)
        total_elapsed =+ elapsed

    return total_elapsed/iter