import sys
import atax_numpy
import atax_pytorch
import atax_naive
#import atax_fpga
# atax_cpp

def main():
  # pass device, framework args from shell script
  # module load needed modules
  # load correct conda env + runtime from script

  # Defaults
  M, N = 60, 70
  device = 'cpu'

  if (len(sys.argv) > 1):
    framework = sys.argv[1]
  if (len(sys.argv) > 2):
    iter = int(sys.argv[2])
  if (len(sys.argv) > 3):
    device = sys.argv[3]
#   if (len(sys.argv) > 4):
#     N = int(sys.argv[4])

  if (framework=="pytorch"):
    time = atax_pytorch.initialize(M, N, iter, device)
  elif (framework=="numpy"):
    time = atax_numpy.initialize(M, N, iter, device)
  elif (framework=="naive"):
    time = atax_naive.initialize(M, N, iter, device)
  elif (framework=="fpga"):
    time = atax_fpga.initialize(M, N, iter, device)
  
  print(f"{time * 1000:.4f}")
  # print(f"kernel took: {time * 1000:.4f} ms, effective memory bandwidth: {bandwidth:.4f} GB/s")
  # print(f"Numpy kernel time: {t1 * 1000:.4f} ms, effective memory bandwidth: {numpy_bandwidth:.4f} GB/s")
  # print(f"For loop kernel time: {t2 * 1000:.4f} ms, effective memory bandwidth: {for_bandwidth:.4f} GB/s")

if __name__ == "__main__":
  main()