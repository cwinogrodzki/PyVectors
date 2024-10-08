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

    # Skip boundary points
    for k in range(1, nz - 1):
        for j in range(1, ny - 1):
            for i in range(1, nx - 1):
                # Apply stencil approximation of Laplacian to all interior points
                A_xx = (A[i + 1, j, k] - 2 * A[i, j, k] + A[i - 1, j, k]) * INVHX2
                A_yy = (A[i, j + 1, k] - 2 * A[i, j, k] + A[i, j - 1, k]) * INVHY2
                A_zz = (A[i, j, k + 1] - 2 * A[i, j, k] + A[i, j, k - 1]) * INVHZ2
                B[i, j, k] = A_xx + A_yy + A_zz

def initialize(nx, ny, nz, iter):
    A = np.fromfunction(lambda i, j, k: (i + j + (nx - k)) * 10 / nx, (nx, ny, nz),
                    dtype=np.float64)
    B = np.copy(A)

    # total_elapsed = 0
    # for k in range(1, iter):
    #     start = time.perf_counter()
    #     numpy_result = kernel(A, B, nx, ny, nz)
    #     elapsed = time.perf_counter() - start
    #     total_elapsed =+ elapsed

    start = time.perf_counter()
    numpy_result = kernel(A, B, nx, ny, nz)
    total_elapsed = time.perf_counter() - start
    
    return total_elapsed

    return total_elapsed