import numpy as np
import time

def kernel(A, B, nx, ny, nz):
    # Grid spacings
    hx = 1.0 / (nx - 1)
    hy = 1.0 / (ny - 1)
    hz = 1.0 / (nz - 1)

    INVHX2 = 1.0 / hx / hx
    INVHY2 = 1.0 / hy / hy
    INVHZ2 = 1.0 / hz / hz
    INVHXYZ2 = -2.0 * (INVHX2 + INVHY2 + INVHZ2)

    B[1:-1, 1:-1, 1:-1] = (A[1:-1, 1:-1, 1:-1] * INVHXYZ2 +
                            (A[2:, 1:-1, 1:-1] + A[:-2, 1:-1, 1:-1]) * INVHX2 +
                            (A[1:-1, 2:, 1:-1] + A[1:-1, :-2, 1:-1]) * INVHY2 +
                            (A[1:-1, 1:-1, 2:] + A[1:-1, 1:-1, :-2]) * INVHZ2)
    
def initialize(nx, ny, nz):
    A = np.fromfunction(lambda i, j, k: (i + j + (nx - k)) * 10 / nx, (nx, ny, nz),
                    dtype=np.float64)
    B = np.copy(A)

    start = time.perf_counter()
    numpy_result = kernel(A, B, nx, ny, nz)
    elapsed = time.perf_counter() - start

    return elapsed


