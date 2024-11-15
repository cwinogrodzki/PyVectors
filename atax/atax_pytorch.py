import torch
import numpy as np
import time
import atax_numpy

def kernel(A, x):
    return (A @ x) @ A

def initialize(M, N, iter, device):
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
    fn = dtype(N)

    x = torch.tensor(np.fromfunction(lambda i: 1 + (i / fn), (N, ), dtype=dtype), device=device)
    A = torch.tensor(np.fromfunction(lambda i, j: ((i + j) % N) / (5 * M), (M, N),
                        dtype=dtype), device=device)
    
    x_ref = np.fromfunction(lambda i: 1 + (i / fn), (N, ), dtype=dtype)
    A_ref = np.fromfunction(lambda i, j: ((i + j) % N) / (5 * M), (M, N),
                        dtype=dtype)

    total_elapsed = 0
    for k in range(1, iter):
        start = time.perf_counter()
        result = kernel(A, x)
        elapsed = time.perf_counter() - start
        print(elapsed)
        total_elapsed =+ elapsed

    return total_elapsed/iter