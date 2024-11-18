import numpy as np
import time

TSTEPS=5

def kernel(A, B):
    for t in range(1, TSTEPS):
        B[1:-1, 1:-1, 1:-1] = (0.125 * (A[2:, 1:-1, 1:-1] - 2.0 * A[1:-1, 1:-1, 1:-1] + A[:-2, 1:-1, 1:-1]) 
                             + 0.125 * (A[1:-1, 2:, 1:-1] - 2.0 * A[1:-1, 1:-1, 1:-1] + A[1:-1, :-2, 1:-1]) 
                             + 0.125 * (A[1:-1, 1:-1, 2:] - 2.0 * A[1:-1, 1:-1, 1:-1] + A[1:-1, 1:-1, :-2]) 
                             + A[1:-1, 1:-1, 1:-1])
        A[1:-1, 1:-1, 1:-1] = (0.125 * (B[2:, 1:-1, 1:-1] - 2.0 * B[1:-1, 1:-1, 1:-1] + B[:-2, 1:-1, 1:-1]) 
                             + 0.125 * (B[1:-1, 2:, 1:-1] - 2.0 * B[1:-1, 1:-1, 1:-1] + B[1:-1, :-2, 1:-1]) 
                             + 0.125 * (B[1:-1, 1:-1, 2:] - 2.0 * B[1:-1, 1:-1, 1:-1] + B[1:-1, 1:-1, 0:-2]) 
                             + B[1:-1, 1:-1, 1:-1])
    return A
    
def initialize(N, iter, device):
    #print(np.core._multiarray_umath.__cpu_features__)
    # A = np.fromfunction(lambda i, j, k: (i + j + (N - k)) * 10 / N, (N, N, N),
    #                 dtype=np.float64)
    # B = np.copy(A)

    total_elapsed = 0
    for k in range(1, iter):
        A = np.fromfunction(lambda i, j, k: (i + j + (N - k)) * 10 / N, (N, N, N),
                    dtype=np.float64)
        B = np.copy(A)
        start = time.perf_counter()
        numpy_result = kernel(A, B)
        elapsed = time.perf_counter() - start
        print(elapsed)
        total_elapsed =+ elapsed
    
    return total_elapsed/iter


