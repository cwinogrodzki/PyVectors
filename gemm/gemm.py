import sys
import gemm_numpy
import gemm_pytorch
import gemm_naive
#import laplacian_fpga
# lap_cpp

def main():
  # pass device, framework args from shell script
  # module load needed modules
  # load correct conda env + runtime from script

  # Defaults
  Ni, Nj, Nk = 60, 70, 80
  device = 'cpu'

  if (len(sys.argv) > 1):
    framework = sys.argv[1]
  if (len(sys.argv) > 2):
    iter = int(sys.argv[2])
  if (len(sys.argv) > 3):
    device = sys.argv[3]
  if (len(sys.argv) > 4):
    N = int(sys.argv[4])

  if (framework=="pytorch"):
    time = gemm_pytorch.initialize(Ni, Nj, Nk, iter, device)
  elif (framework=="numpy"):
    time = gemm_numpy.initialize(Ni, Nj, Nk, iter, device)
  elif (framework=="naive"):
    time = gemm_naive.initialize(Ni, Nj, Nk, iter, device)
  elif (framework=="fpga"):
    time = gemm_fpga.initialize(Ni, Nj, Nk, iter, device)
  
  # Effective memory bandwidth
  #bandwidth = (theoretical_fetch_size + theoretical_write_size) / time
  
  #print(f"{time * 1000:.4f}")
  # print(f"kernel took: {time * 1000:.4f} ms, effective memory bandwidth: {bandwidth:.4f} GB/s")
  # print(f"Numpy kernel time: {t1 * 1000:.4f} ms, effective memory bandwidth: {numpy_bandwidth:.4f} GB/s")
  # print(f"For loop kernel time: {t2 * 1000:.4f} ms, effective memory bandwidth: {for_bandwidth:.4f} GB/s")

if __name__ == "__main__":
  main()