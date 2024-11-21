#include <dace/fpga_device.h>
#include <dace/math.h>
#include <dace/complex.h>
constexpr long long N = 100;

struct stencil_kernel_state_t {
    dace_fpga_context *fpga_context;
};


void stencil_kernel_0_0_0(const double* __A_in, const double* __B_in, const long long& __TSTEPS_in, double* __A_out, double* __B_out) {
    #pragma HLS INLINE
    long long t;




    for (t = 1; (t < __TSTEPS_in); t = (t + 1)) {
        {
            {
                for (long long __i0 = 0; __i0 < (N - 2); __i0 += 1) {
                    for (long long __i1 = 0; __i1 < (N - 2); __i1 += 1) {
                        for (long long __i2 = 0; __i2 < (N - 2); __i2 += 1) {
                            #pragma HLS PIPELINE II=1
                            #pragma HLS LOOP_FLATTEN
                            double __s1_n12__out_n13IN___tmp9;
                            {
                                double __in2 = __A_in[(((((N * N) * (__i0 + 1)) + (N * (__i1 + 1))) + __i2) + 1)];
                                double __out;

                                ///////////////////
                                // Tasklet code (_Mult_)
                                __out = (2.0 * __in2);
                                ///////////////////

                                __s1_n12__out_n13IN___tmp9 = __out;
                            }
                            double __s1_n13__out_n14IN___tmp10;
                            {
                                const double __in2 = __s1_n12__out_n13IN___tmp9;
                                double __in1 = __A_in[(((((N * N) * (__i0 + 1)) + (N * (__i1 + 1))) + __i2) + 2)];
                                double __out;

                                ///////////////////
                                // Tasklet code (_Sub_)
                                __out = (__in1 - __in2);
                                ///////////////////

                                __s1_n13__out_n14IN___tmp10 = __out;
                            }
                            double __s1_n14__out_n15IN___tmp11;
                            {
                                const double __in1 = __s1_n13__out_n14IN___tmp10;
                                double __in2 = __A_in[((((N * N) * (__i0 + 1)) + (N * (__i1 + 1))) + __i2)];
                                double __out;

                                ///////////////////
                                // Tasklet code (_Add_)
                                __out = (__in1 + __in2);
                                ///////////////////

                                __s1_n14__out_n15IN___tmp11 = __out;
                            }
                            double __s1_n15__out_n16IN___tmp12;
                            {
                                const double __in2 = __s1_n14__out_n15IN___tmp11;
                                double __out;

                                ///////////////////
                                // Tasklet code (_Mult_)
                                __out = (0.125 * __in2);
                                ///////////////////

                                __s1_n15__out_n16IN___tmp12 = __out;
                            }
                            double __s1_n7__out_n8IN___tmp4;
                            {
                                double __in2 = __A_in[(((((N * N) * (__i0 + 1)) + (N * (__i1 + 1))) + __i2) + 1)];
                                double __out;

                                ///////////////////
                                // Tasklet code (_Mult_)
                                __out = (2.0 * __in2);
                                ///////////////////

                                __s1_n7__out_n8IN___tmp4 = __out;
                            }
                            double __s1_n8__out_n9IN___tmp5;
                            {
                                const double __in2 = __s1_n7__out_n8IN___tmp4;
                                double __in1 = __A_in[(((((N * N) * (__i0 + 1)) + (N * (__i1 + 2))) + __i2) + 1)];
                                double __out;

                                ///////////////////
                                // Tasklet code (_Sub_)
                                __out = (__in1 - __in2);
                                ///////////////////

                                __s1_n8__out_n9IN___tmp5 = __out;
                            }
                            double __s1_n9__out_n10IN___tmp6;
                            {
                                const double __in1 = __s1_n8__out_n9IN___tmp5;
                                double __in2 = __A_in[(((((N * N) * (__i0 + 1)) + (N * __i1)) + __i2) + 1)];
                                double __out;

                                ///////////////////
                                // Tasklet code (_Add_)
                                __out = (__in1 + __in2);
                                ///////////////////

                                __s1_n9__out_n10IN___tmp6 = __out;
                            }
                            double __s1_n10__out_n11IN___tmp7;
                            {
                                const double __in2 = __s1_n9__out_n10IN___tmp6;
                                double __out;

                                ///////////////////
                                // Tasklet code (_Mult_)
                                __out = (0.125 * __in2);
                                ///////////////////

                                __s1_n10__out_n11IN___tmp7 = __out;
                            }
                            double __s1_n1__out_n2IN___tmp0;
                            {
                                double __in2 = __A_in[(((((N * N) * (__i0 + 1)) + (N * (__i1 + 1))) + __i2) + 1)];
                                double __out;

                                ///////////////////
                                // Tasklet code (_Mult_)
                                __out = (2.0 * __in2);
                                ///////////////////

                                __s1_n1__out_n2IN___tmp0 = __out;
                            }
                            double __s1_n3__out_n4IN___tmp1;
                            {
                                const double __in2 = __s1_n1__out_n2IN___tmp0;
                                double __in1 = __A_in[(((((N * N) * (__i0 + 2)) + (N * (__i1 + 1))) + __i2) + 1)];
                                double __out;

                                ///////////////////
                                // Tasklet code (_Sub_)
                                __out = (__in1 - __in2);
                                ///////////////////

                                __s1_n3__out_n4IN___tmp1 = __out;
                            }
                            double __s1_n4__out_n5IN___tmp2;
                            {
                                const double __in1 = __s1_n3__out_n4IN___tmp1;
                                double __in2 = __A_in[(((((N * N) * __i0) + (N * (__i1 + 1))) + __i2) + 1)];
                                double __out;

                                ///////////////////
                                // Tasklet code (_Add_)
                                __out = (__in1 + __in2);
                                ///////////////////

                                __s1_n4__out_n5IN___tmp2 = __out;
                            }
                            double __s1_n5__out_n6IN___tmp3;
                            {
                                const double __in2 = __s1_n4__out_n5IN___tmp2;
                                double __out;

                                ///////////////////
                                // Tasklet code (_Mult_)
                                __out = (0.125 * __in2);
                                ///////////////////

                                __s1_n5__out_n6IN___tmp3 = __out;
                            }
                            double __s1_n10__out_n11IN___tmp8;
                            {
                                const double __in1 = __s1_n5__out_n6IN___tmp3;
                                const double __in2 = __s1_n10__out_n11IN___tmp7;
                                double __out;

                                ///////////////////
                                // Tasklet code (_Add_)
                                __out = (__in1 + __in2);
                                ///////////////////

                                __s1_n10__out_n11IN___tmp8 = __out;
                            }
                            double __s1_n15__out_n16IN___tmp13;
                            {
                                const double __in1 = __s1_n10__out_n11IN___tmp8;
                                const double __in2 = __s1_n15__out_n16IN___tmp12;
                                double __out;

                                ///////////////////
                                // Tasklet code (_Add_)
                                __out = (__in1 + __in2);
                                ///////////////////

                                __s1_n15__out_n16IN___tmp13 = __out;
                            }
                            {
                                const double __in1 = __s1_n15__out_n16IN___tmp13;
                                double __in2 = __A_in[(((((N * N) * (__i0 + 1)) + (N * (__i1 + 1))) + __i2) + 1)];
                                double __out;

                                ///////////////////
                                // Tasklet code (_Add_)
                                __out = (__in1 + __in2);
                                ///////////////////

                                *(__B_out + (((((N * N) * (__i0 + 1)) + (N * (__i1 + 1))) + __i2) + 1)) = __out;
                            }
                        }
                    }
                }
            }
            {
                for (long long __i0 = 0; __i0 < (N - 2); __i0 += 1) {
                    for (long long __i1 = 0; __i1 < (N - 2); __i1 += 1) {
                        for (long long __i2 = 0; __i2 < (N - 2); __i2 += 1) {
                            #pragma HLS PIPELINE II=1
                            #pragma HLS LOOP_FLATTEN
                            double __s1_n30__out_n31IN___tmp24;
                            {
                                double __in2 = __B_out[(((((N * N) * (__i0 + 1)) + (N * (__i1 + 1))) + __i2) + 1)];
                                double __out;

                                ///////////////////
                                // Tasklet code (_Mult_)
                                __out = (2.0 * __in2);
                                ///////////////////

                                __s1_n30__out_n31IN___tmp24 = __out;
                            }
                            double __s1_n31__out_n32IN___tmp25;
                            {
                                const double __in2 = __s1_n30__out_n31IN___tmp24;
                                double __in1 = __B_out[(((((N * N) * (__i0 + 1)) + (N * (__i1 + 1))) + __i2) + 2)];
                                double __out;

                                ///////////////////
                                // Tasklet code (_Sub_)
                                __out = (__in1 - __in2);
                                ///////////////////

                                __s1_n31__out_n32IN___tmp25 = __out;
                            }
                            double __s1_n32__out_n33IN___tmp26;
                            {
                                const double __in1 = __s1_n31__out_n32IN___tmp25;
                                double __in2 = __B_out[((((N * N) * (__i0 + 1)) + (N * (__i1 + 1))) + __i2)];
                                double __out;

                                ///////////////////
                                // Tasklet code (_Add_)
                                __out = (__in1 + __in2);
                                ///////////////////

                                __s1_n32__out_n33IN___tmp26 = __out;
                            }
                            double __s1_n33__out_n34IN___tmp27;
                            {
                                const double __in2 = __s1_n32__out_n33IN___tmp26;
                                double __out;

                                ///////////////////
                                // Tasklet code (_Mult_)
                                __out = (0.125 * __in2);
                                ///////////////////

                                __s1_n33__out_n34IN___tmp27 = __out;
                            }
                            double __s1_n25__out_n26IN___tmp19;
                            {
                                double __in2 = __B_out[(((((N * N) * (__i0 + 1)) + (N * (__i1 + 1))) + __i2) + 1)];
                                double __out;

                                ///////////////////
                                // Tasklet code (_Mult_)
                                __out = (2.0 * __in2);
                                ///////////////////

                                __s1_n25__out_n26IN___tmp19 = __out;
                            }
                            double __s1_n26__out_n27IN___tmp20;
                            {
                                const double __in2 = __s1_n25__out_n26IN___tmp19;
                                double __in1 = __B_out[(((((N * N) * (__i0 + 1)) + (N * (__i1 + 2))) + __i2) + 1)];
                                double __out;

                                ///////////////////
                                // Tasklet code (_Sub_)
                                __out = (__in1 - __in2);
                                ///////////////////

                                __s1_n26__out_n27IN___tmp20 = __out;
                            }
                            double __s1_n27__out_n28IN___tmp21;
                            {
                                const double __in1 = __s1_n26__out_n27IN___tmp20;
                                double __in2 = __B_out[(((((N * N) * (__i0 + 1)) + (N * __i1)) + __i2) + 1)];
                                double __out;

                                ///////////////////
                                // Tasklet code (_Add_)
                                __out = (__in1 + __in2);
                                ///////////////////

                                __s1_n27__out_n28IN___tmp21 = __out;
                            }
                            double __s1_n28__out_n29IN___tmp22;
                            {
                                const double __in2 = __s1_n27__out_n28IN___tmp21;
                                double __out;

                                ///////////////////
                                // Tasklet code (_Mult_)
                                __out = (0.125 * __in2);
                                ///////////////////

                                __s1_n28__out_n29IN___tmp22 = __out;
                            }
                            double __s1_n20__out_n21IN___tmp15;
                            {
                                double __in2 = __B_out[(((((N * N) * (__i0 + 1)) + (N * (__i1 + 1))) + __i2) + 1)];
                                double __out;

                                ///////////////////
                                // Tasklet code (_Mult_)
                                __out = (2.0 * __in2);
                                ///////////////////

                                __s1_n20__out_n21IN___tmp15 = __out;
                            }
                            double __s1_n21__out_n22IN___tmp16;
                            {
                                const double __in2 = __s1_n20__out_n21IN___tmp15;
                                double __in1 = __B_out[(((((N * N) * (__i0 + 2)) + (N * (__i1 + 1))) + __i2) + 1)];
                                double __out;

                                ///////////////////
                                // Tasklet code (_Sub_)
                                __out = (__in1 - __in2);
                                ///////////////////

                                __s1_n21__out_n22IN___tmp16 = __out;
                            }
                            double __s1_n22__out_n23IN___tmp17;
                            {
                                const double __in1 = __s1_n21__out_n22IN___tmp16;
                                double __in2 = __B_out[(((((N * N) * __i0) + (N * (__i1 + 1))) + __i2) + 1)];
                                double __out;

                                ///////////////////
                                // Tasklet code (_Add_)
                                __out = (__in1 + __in2);
                                ///////////////////

                                __s1_n22__out_n23IN___tmp17 = __out;
                            }
                            double __s1_n23__out_n24IN___tmp18;
                            {
                                const double __in2 = __s1_n22__out_n23IN___tmp17;
                                double __out;

                                ///////////////////
                                // Tasklet code (_Mult_)
                                __out = (0.125 * __in2);
                                ///////////////////

                                __s1_n23__out_n24IN___tmp18 = __out;
                            }
                            double __s1_n28__out_n29IN___tmp23;
                            {
                                const double __in1 = __s1_n23__out_n24IN___tmp18;
                                const double __in2 = __s1_n28__out_n29IN___tmp22;
                                double __out;

                                ///////////////////
                                // Tasklet code (_Add_)
                                __out = (__in1 + __in2);
                                ///////////////////

                                __s1_n28__out_n29IN___tmp23 = __out;
                            }
                            double __s1_n33__out_n34IN___tmp28;
                            {
                                const double __in1 = __s1_n28__out_n29IN___tmp23;
                                const double __in2 = __s1_n33__out_n34IN___tmp27;
                                double __out;

                                ///////////////////
                                // Tasklet code (_Add_)
                                __out = (__in1 + __in2);
                                ///////////////////

                                __s1_n33__out_n34IN___tmp28 = __out;
                            }
                            {
                                const double __in1 = __s1_n33__out_n34IN___tmp28;
                                double __in2 = __B_out[(((((N * N) * (__i0 + 1)) + (N * (__i1 + 1))) + __i2) + 1)];
                                double __out;

                                ///////////////////
                                // Tasklet code (_Add_)
                                __out = (__in1 + __in2);
                                ///////////////////

                                *(__A_out + (((((N * N) * (__i0 + 1)) + (N * (__i1 + 1))) + __i2) + 1)) = __out;
                            }
                        }
                    }
                }
            }

        }

    }

    
}

void module_stencil_kernel_0_0(long long TSTEPS, double *fpga_A, double *fpga_B) {

    stencil_kernel_0_0_0(&fpga_A[0], &fpga_B[0], TSTEPS, &fpga_A[0], &fpga_B[0]);
}

DACE_EXPORTED void stencil_kernel_0_0(long long TSTEPS, double *fpga_A_0, double *fpga_B_0) {
    #pragma HLS INTERFACE m_axi port=fpga_A_0 offset=slave bundle=gmem0
    #pragma HLS INTERFACE m_axi port=fpga_B_0 offset=slave bundle=gmem1
    #pragma HLS INTERFACE s_axilite port=TSTEPS bundle=control
    #pragma HLS INTERFACE s_axilite port=fpga_A_0 bundle=control
    #pragma HLS INTERFACE s_axilite port=fpga_B_0 bundle=control
    #pragma HLS INTERFACE s_axilite port=return bundle=control
    
    #pragma HLS DATAFLOW
    
    HLSLIB_DATAFLOW_INIT();
    HLSLIB_DATAFLOW_FUNCTION(module_stencil_kernel_0_0, TSTEPS, fpga_A_0, fpga_B_0);
    HLSLIB_DATAFLOW_FINALIZE();
}
