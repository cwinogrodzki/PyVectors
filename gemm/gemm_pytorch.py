import torch
import numpy as np
import time

def kernel(alpha, beta, A, B, C):
    C[:] = alpha * A @ B + beta * C

def initialize(Ni, Nj, Nk, iter, device):
    if(device == 'cpu'):
        print("CPU capability: ", torch.backends.cpu.get_cpu_capability())
        if torch.backends.mkl.is_available(): print("Using oneMKL.")
        if torch.backends.mkldnn.is_available(): print("Using oneDNN.")
    elif(device == 'cuda'):
        #check that CUDA is available
        if not torch.cuda.is_available():
            if not torch.backends.cuda.is_built():
                print("CUDA not available because the current PyTorch install was not "
                "built with CUDA.")
            else:
                print("CUDA not available because no device is detected.")
            device = 'cpu'
        else:
            print("Using device: ", torch.cuda.get_device_name(0))
            torch.backends.cuda.preferred_blas_library(backend='cublas')
    elif(device == 'rocm'):
        #check that ROCm is available
        if not torch.cuda.is_available():
            if not torch.backends.cuda.is_built():
                print("ROCm not available because the current PyTorch install was not "
                "built with ROCm.")
            else:
                print("ROCm not available because no device is detected.")
            device = 'cpu' 
        else:
            print("Using device: ", torch.cuda.get_device_name(0))
            device = 'cuda'
            #torch.backends.cuda.preferred_blas_library(backend='hipblaslt') 
    elif(device == 'mps'):
        #check that MPS is available
        if not torch.backends.mps.is_available():
            if not torch.backends.mps.is_built():
                print("MPS not available because the current PyTorch install was not "
                "built with MPS enabled.")
            else:
                print("MPS not available because the current MacOS version is not 12.3+ "
                "and/or you do not have an MPS-enabled device on this machine.")
            device = 'cpu' 
    else:
        device='cpu'

    dtype=np.float64
    alpha = dtype(1.5)
    beta = dtype(1.2)

    A = torch.tensor(np.fromfunction(lambda i, k: (i * (k + 1) % Nk) / Nk, (Ni, Nk),
                        dtype=dtype))
    B = torch.tensor(np.fromfunction(lambda k, j: (k * (j + 2) % Nj) / Nj, (Nk, Nj),
                        dtype=dtype))
    C = torch.tensor(np.fromfunction(lambda i, j: ((i * j + 1) % Ni) / Ni, (Ni, Nj),
                        dtype=dtype))

    total_elapsed = 0
    for k in range(1, iter):
        start = time.perf_counter()
        numpy_result = kernel(alpha, beta, A, B, C)
        elapsed = time.perf_counter() - start
        print(elapsed)
        total_elapsed =+ elapsed

    return total_elapsed/iter