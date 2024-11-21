open_project kernel_0_0  
open_solution -flow_target vitis xcu250-figd2104-2L-e  
set_part xcu250-figd2104-2L-e  
add_files -cflags "-std=c++14 -DDACE_SYNTHESIS -DDACE_XILINX -DDACE_XILINX_DEVICE_CODE -DHLSLIB_SYNTHESIS -DHLSLIB_XILINX -DVITIS_MAJOR_VERSION=2023 -DVITIS_MINOR_VERSION=1 -DVITIS_VERSION=2023.1 -D__VITIS_HLS__ -I/home/grodzki/.local/lib/python3.10/site-packages/dace/codegen/../external/hlslib/include -I/home/grodzki/.local/lib/python3.10/site-packages/dace/codegen/../runtime/include" "/net/myshella/home/grodzki/PyVectors/.dacecache/kernel/src/xilinx/device/kernel_0_0.cpp"  
set_top kernel_0_0  
config_compile -pipeline_style frp  
csynth_design  
exit