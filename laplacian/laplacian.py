import time
import sys
import numpy as np

def laplacian(hx, hy, hz, nx, ny, nz):
    u = [0]*(nx*ny*nz)
    f = [0]*(nx*ny*nz)

    # Convert to numpy arrays  
    u = np.array(u)
    f = np.array(f)

    # Reshape arrays to 3D
    u = u.reshape((nx, ny, nz))
    f = f.reshape((nx, ny, nz))

    INVHX2 = 1.0 / hx / hx
    INVHY2 = 1.0 / hy / hy
    INVHZ2 = 1.0 / hz / hz
    INVHXYZ2 = -2.0 * (INVHX2 + INVHY2 + INVHZ2)

    f[1:-1, 1:-1, 1:-1] = (u[1:-1, 1:-1, 1:-1] * INVHXYZ2 +
                            (u[2:, 1:-1, 1:-1] + u[:-2, 1:-1, 1:-1]) * INVHX2 +
                            (u[1:-1, 2:, 1:-1] + u[1:-1, :-2, 1:-1]) * INVHY2 +
                            (u[1:-1, 1:-1, 2:] + u[1:-1, 1:-1, :-2]) * INVHZ2)

    return f

def laplacian_for(hx, hy, hz, nx, ny, nz):
    u = [0]*(nx*ny*nz)
    f = [0]*(nx*ny*nz)

    # Convert to numpy arrays  
    u = np.array(u)
    f = np.array(f)

    # Reshape arrays to 3D
    u = u.reshape((nx, ny, nz))
    f = f.reshape((nx, ny, nz))

    INVHX2 = 1.0 / hx / hx
    INVHY2 = 1.0 / hy / hy
    INVHZ2 = 1.0 / hz / hz

    # Skip boundary points
    for k in range(1, nz - 1):
        for j in range(1, ny - 1):
            for i in range(1, nx - 1):
                # Apply stencil approximation of Laplacian to all interior points
                u_xx = (u[i + 1, j, k] - 2 * u[i, j, k] + u[i - 1, j, k]) * INVHX2
                u_yy = (u[i, j + 1, k] - 2 * u[i, j, k] + u[i, j - 1, k]) * INVHY2
                u_zz = (u[i, j, k + 1] - 2 * u[i, j, k] + u[i, j, k - 1]) * INVHZ2
                f[i, j, k] = u_xx + u_yy + u_zz

    return f

def main():
  # Default problem size
  nx, ny, nz = 10, 10, 10
  precision = 'float32'
  float_bytes = 4


  if (len(sys.argv) > 0):
    nx = int(sys.argv[1])
  if (len(sys.argv) > 1):
    ny = int(sys.argv[2])
  if (len(sys.argv) > 2):
    nz = int(sys.argv[3])
  if len(sys.argv) > 3:
    precision = sys.argv[4]

  print(f"nx, ny, nz = {nx}, {ny}, {nz}")

  if precision=='float64': float_bytes = 8
  elif precision=='float16': float_bytes = 2

  # Theoretical fetch and write sizes:
  theoretical_fetch_size = (nx * ny * nz - 8 - 4 * (nx - 2) - 4 * (ny - 2) - 4 * (nz - 2)) * float_bytes * 1e-9
  theoretical_write_size = ((nx - 2) * (ny - 2) * (nz - 2)) * float_bytes * 1e-9
  print(f"Theoretical fetch size (GB): {theoretical_fetch_size:.4f}")
  print(f"Theoretical write size (GB): {theoretical_write_size:.4f}")

  # Grid spacings
  hx = 1.0 / (nx - 1)
  hy = 1.0 / (ny - 1)
  hz = 1.0 / (nz - 1)

  # Move data to device
  # device = 'cuda:0'
  # cuda.synchronize()
  # d_f = d_f.to(device)
  # d_u = d_u.to(device)
  # cuda.synchronize()

  # Compute Laplacian for all interior points
  t1 = time.perf_counter()
  numpy_result = laplacian(hx, hy, hz, nx, ny, nz)
  t1 = time.perf_counter() - t1

  t2 = time.perf_counter()
  for_result = laplacian_for(hx, hy, hz, nx, ny, nz)
  t2 = time.perf_counter() - t2
  
  # Effective memory bandwidth
  numpy_bandwidth = (theoretical_fetch_size + theoretical_write_size) / t1
  for_bandwidth = (theoretical_fetch_size + theoretical_write_size) / t2
  
  if((numpy_result == for_result).all):
     is_equal = True
  else: is_equal = False   
  
  # print(f"Laplacian kernel took: {elapsed_time * 1000:.4f} ms, effective memory bandwidth: {bandwidth:.4f} GB/s")
  print(f"Numpy kernel time: {t1 * 1000:.4f} ms, effective memory bandwidth: {numpy_bandwidth:.4f} GB/s")
  print(f"For loop kernel time: {t2 * 1000:.4f} ms, effective memory bandwidth: {for_bandwidth:.4f} GB/s")
  print(f"Results are equal: {is_equal}")

if __name__ == "__main__":
    main()