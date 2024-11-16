import numpy as np
import time
import jacobi_numpy

TSTEPS = 5
def kernel(A, B):
    for t in range(1, TSTEPS):
        # Get the shape of A (assumed to be the same as B)
        rows, cols = A.shape

        # Create temporary arrays to hold the new values
        new_B = np.copy(B)
        new_A = np.copy(A)

        # Iterate through the interior elements
        for i in range(1, rows - 1):
            for j in range(1, cols - 1):
                # Update new_B
                new_B[i, j] = 0.2 * (A[i, j] + A[i, j - 1] + A[i, j + 1] +
                                    A[i + 1, j] + A[i - 1, j])
                # Update new_A
                new_A[i, j] = 0.2 * (B[i, j] + B[i, j - 1] + B[i, j + 1] +
                                    B[i + 1, j] + B[i - 1, j])

    # Assign the new values back to B and A
    B[1:-1, 1:-1] = new_B[1:-1, 1:-1]
    A[1:-1, 1:-1] = new_A[1:-1, 1:-1]

    return A



def initialize(N, iter, device):
    dtype=np.float64

    A = np.fromfunction(lambda i, j: i * (j + 2) / N, (N, N), dtype=dtype)
    B = np.fromfunction(lambda i, j: i * (j + 3) / N, (N, N), dtype=dtype)
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

    result = kernel(A, B)
    result_ref = jacobi_numpy.kernel(A_ref, B_ref)
    assert np.allclose(result, result_ref)