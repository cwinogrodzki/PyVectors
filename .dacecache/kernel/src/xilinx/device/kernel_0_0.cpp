#include <dace/fpga_device.h>
#include <dace/math.h>
#include <dace/complex.h>
constexpr long long NI = 60;
constexpr long long NJ = 70;
constexpr long long NK = 80;

struct kernel_state_t {
    dace_fpga_context *fpga_context;
};


void module__Mult__7_0(dace::FIFO<double, 1, 32> A_pipe[32], double *__tmp0, double alpha, double *fpga_A) {

    {
        for (int __i0 = 0; __i0 < 60; __i0 += 1) {
            for (int __i1 = 0; __i1 < 80; __i1 += 1) {
                #pragma HLS PIPELINE II=1
                #pragma HLS LOOP_FLATTEN
                {
                    double __in1 = alpha;
                    double __in2 = fpga_A[((80 * __i0) + __i1)];
                    double __out;

                    ///////////////////
                    // Tasklet code (_Mult_)
                    __out = (__in1 * __in2);
                    ///////////////////

                    *(__tmp0 + ((80 * __i0) + __i1)) = __out;
                }
            }
        }
    }
    {
        for (int n0 = 0; n0 < 2; n0 += 1) {
            {
                const int tm = 0; // Degenerate loop
                for (int k = 0; k < 80; k += 1) {
                    for (int n1 = 0; n1 < 32; n1 += 1) {
                        #pragma HLS PIPELINE II=1
                        #pragma HLS LOOP_FLATTEN
                        {
                            const double &from_memory = __tmp0[((k + (2560 * n0)) + (80 * n1))];


                            ///////////////////
                            // Tasklet code (read_A)
                            auto data = ((((n0 * 32) + n1) < 60) ? from_memory : 0);
                            A_pipe[(31 - n1)].push(data);
                            ///////////////////

                        }
                    }
                }
            }
        }
    }
}

void module_init_dummy_B_25_read_B_27_0(dace::FIFO<double, 1, 1> B_pipe[33], double *fpga_B) {

    dace::vec<double, 1> B_dummy;
    {
        dace::vec<double, 1> init_data;

        ///////////////////
        // Tasklet code (init_dummy_B)
        init_data = 0;
        ///////////////////

        B_dummy = init_data;
    }
    {
        for (int n = 0; n < 2; n += 1) {
            {
                const int tm = 0; // Degenerate loop
                for (int k = 0; k < 80; k += 1) {
                    for (int m = 0; m < 70; m += 1) {
                        #pragma HLS PIPELINE II=1
                        #pragma HLS LOOP_FLATTEN
                        {
                            dace::vec<double, 1> dummy_data = B_dummy;
                            const double &from_memory = fpga_B[(((70 * k) + m) + (70 * tm))];


                            ///////////////////
                            // Tasklet code (read_B)
                            auto data = ((((tm * 70) + m) < 70) ? from_memory : dummy_data);
                            B_pipe[0].push(data);
                            ///////////////////

                        }
                    }
                }
            }
        }
    }
}

void module_compute_and_drain_44_buffer_b_43_buffer_a_41_C_data_init_40_0(dace::FIFO<double, 1, 32> A_pipe[32], dace::FIFO<double, 1, 1> B_pipe[33], dace::FIFO<double, 1, 70> C_pipe[33], int p) {

    double A_reg;
    dace::vec<double, 1> B_reg;
    dace::vec<double, 1> C_buffer[70];
    {
        long n0 = 0;
        long tm = 0;
        long k = 0;
        long m = 0;
        long m_drain = 0;
        long k_drain = 0;
        for (long __n0tmkm = 0; __n0tmkm < 11200 + 2240; ++__n0tmkm) {
            const bool __n0tmkm_drain = __n0tmkm >= 11200 + 2240 - 2240;
            #pragma HLS PIPELINE II=1
            #pragma HLS LOOP_FLATTEN
            #pragma HLS DEPENDENCE variable=C_buffer false
            dace::vec<double, 1> C_init;
            {
                dace::vec<double, 1> init_data;

                ///////////////////
                // Tasklet code (C_data_init)
                init_data = 0;
                ///////////////////

                C_init = init_data;
            }
            {
                dace::FIFO<double, 1, 32> &a_in = A_pipe[p];


                ///////////////////
                // Tasklet code (buffer_a)
                if (((m == 0) && (! __n0tmkm_drain))) {A_reg = a_in.pop();
                }
                ///////////////////

            }
            {
                dace::FIFO<double, 1, 1> &b_in = B_pipe[p];


                ///////////////////
                // Tasklet code (buffer_b)
                if (((m >= 0) && (! __n0tmkm_drain))) {B_reg = b_in.pop();
                }
                ///////////////////

            }
            {
                double a_in = A_reg;
                dace::vec<double, 1> b_in = B_reg;
                dace::vec<double, 1> c_init_data = C_init;
                dace::vec<double, 1> c_in = C_buffer[m];
                dace::FIFO<double, 1, 70> &forward_in = C_pipe[(p - 1)];
                dace::FIFO<double, 1, 1> &b_out = B_pipe[(p + 1)];

                dace::FIFO<double, 1, 70> &c_pipe_out = C_pipe[p];

                ///////////////////
                // Tasklet code (compute_and_drain)
                auto result = c_in;
                if (((m >= 0) && (! __n0tmkm_drain))) {
                    auto c_prev = ((k == 0) ? c_init_data : c_in);
                    result = (c_prev + (a_in * b_in));C_buffer[m] = result;
                    if ((p < (32 - 1))) {B_pipe[(p + 1)].push(b_in);
                    }
                }
                if (((((n0 > 0) || (tm > 0)) && (k_drain < p) && (m_drain < 70)) || ((k == (80 - 1)) && (m >= 0)) || (__n0tmkm_drain && (k_drain < p)))) {C_pipe[p].push((((p == 0) || ((k_drain == (80 - 1)) && (! __n0tmkm_drain))) ? result : forward_in.pop()));
                }
                if ((! __n0tmkm_drain)) {
                    if ((m_drain >= ((0 + 70) - 1))) {
                        m_drain = 0;
                        if ((k_drain >= (80 - 1))) {
                            k_drain = 0;
                        }
                        else {
                            k_drain = (k_drain + 1);
                        }
                    }
                    else {
                        m_drain = (m_drain + 1);
                    }
                }
                else if ((m_drain >= (70 - 1))) {
                    m_drain = 0;
                    if ((k_drain >= (80 - 1))) {
                        k_drain = 0;
                    }
                    else {
                        k_drain = (k_drain + 1);
                    }
                }
                else {
                    m_drain = (m_drain + 1);
                }
                ///////////////////

            }
            if (!__n0tmkm_drain) {
                if (m >= 69) {
                    m = 0;
                    if (k >= 79) {
                        k = 0;
                        if (tm >= 0) {
                            tm = 0;
                            if (n0 >= 1) {
                                n0 = 0;
                            } else {
                                n0 += 1;
                            }
                        } else {
                            tm += 1;
                        }
                    } else {
                        k += 1;
                    }
                } else {
                    m += 1;
                }
            }
        }
    }
}

void module_write_C_51__Mult__12_0(dace::FIFO<double, 1, 70> C_pipe[33], double *__tmp1, double *__tmp2, double beta, double *fpga_C) {

    {
        for (int __i0 = 0; __i0 < 60; __i0 += 1) {
            for (int __i1 = 0; __i1 < 70; __i1 += 1) {
                #pragma HLS PIPELINE II=1
                #pragma HLS LOOP_FLATTEN
                {
                    double __in1 = beta;
                    double __in2 = fpga_C[((70 * __i0) + __i1)];
                    double __out;

                    ///////////////////
                    // Tasklet code (_Mult_)
                    __out = (__in1 * __in2);
                    ///////////////////

                    *(__tmp2 + ((70 * __i0) + __i1)) = __out;
                }
            }
        }
    }
    {
        for (int n0 = 0; n0 < 2; n0 += 1) {
            {
                const int tm = 0; // Degenerate loop
                for (int n1 = 0; n1 < 32; n1 += 1) {
                    for (int m = 0; m < 70; m += 1) {
                        #pragma HLS PIPELINE II=1
                        #pragma HLS LOOP_FLATTEN
                        {
                            dace::vec<double, 1> from_kernel = (C_pipe[31]).pop();
                            double* to_memory = &__tmp1[(((m + (2240 * n0)) + (70 * n1)) + (70 * tm))];

                            ///////////////////
                            // Tasklet code (write_C)
                            if (((((tm * 70) + m) < 70) && (((n0 * 32) + n1) < 60))) {__tmp1[(((m + (2240 * n0)) + (70 * n1)) + (70 * tm))] = from_kernel;
                            }
                            ///////////////////

                        }
                    }
                }
            }
        }
    }
    {
        for (int __i0 = 0; __i0 < 60; __i0 += 1) {
            for (int __i1 = 0; __i1 < 70; __i1 += 1) {
                #pragma HLS PIPELINE II=1
                #pragma HLS LOOP_FLATTEN
                {
                    double __in1 = __tmp1[((70 * __i0) + __i1)];
                    double __in2 = __tmp2[((70 * __i0) + __i1)];
                    double __out;

                    ///////////////////
                    // Tasklet code (_Add_)
                    __out = (__in1 + __in2);
                    ///////////////////

                    *(fpga_C + ((70 * __i0) + __i1)) = __out;
                }
            }
        }
    }
}

DACE_EXPORTED void kernel_0_0(double *__tmp0_0, double *__tmp1_0, double *__tmp2_0, double alpha, double beta, double *fpga_A_0, double *fpga_B_0, double *fpga_C_0) {
    #pragma HLS INTERFACE m_axi port=__tmp0_0 offset=slave bundle=gmem0
    #pragma HLS INTERFACE m_axi port=__tmp1_0 offset=slave bundle=gmem1
    #pragma HLS INTERFACE m_axi port=__tmp2_0 offset=slave bundle=gmem2
    #pragma HLS INTERFACE m_axi port=fpga_A_0 offset=slave bundle=gmem3
    #pragma HLS INTERFACE m_axi port=fpga_B_0 offset=slave bundle=gmem4
    #pragma HLS INTERFACE m_axi port=fpga_C_0 offset=slave bundle=gmem5
    #pragma HLS INTERFACE s_axilite port=__tmp0_0 bundle=control
    #pragma HLS INTERFACE s_axilite port=__tmp1_0 bundle=control
    #pragma HLS INTERFACE s_axilite port=__tmp2_0 bundle=control
    #pragma HLS INTERFACE s_axilite port=alpha bundle=control
    #pragma HLS INTERFACE s_axilite port=beta bundle=control
    #pragma HLS INTERFACE s_axilite port=fpga_A_0 bundle=control
    #pragma HLS INTERFACE s_axilite port=fpga_B_0 bundle=control
    #pragma HLS INTERFACE s_axilite port=fpga_C_0 bundle=control
    #pragma HLS INTERFACE s_axilite port=return bundle=control
    
    #pragma HLS DATAFLOW
    
    HLSLIB_DATAFLOW_INIT();
    dace::FIFO<double, 1, 32> A_pipe[32];
    dace::SetNames(A_pipe, "A_pipe", 32);
    dace::FIFO<double, 1, 1> B_pipe[33];
    dace::SetNames(B_pipe, "B_pipe", 33);
    dace::FIFO<double, 1, 70> C_pipe[33];
    dace::SetNames(C_pipe, "C_pipe", 33);
    HLSLIB_DATAFLOW_FUNCTION(module__Mult__7_0, A_pipe, __tmp0_0, alpha, fpga_A_0);
    HLSLIB_DATAFLOW_FUNCTION(module_init_dummy_B_25_read_B_27_0, B_pipe, fpga_B_0);
    for (size_t p = 0; p < 32; p += 1) {
        #pragma HLS UNROLL
        HLSLIB_DATAFLOW_FUNCTION(module_compute_and_drain_44_buffer_b_43_buffer_a_41_C_data_init_40_0, A_pipe, B_pipe, C_pipe, p);
    }
    HLSLIB_DATAFLOW_FUNCTION(module_write_C_51__Mult__12_0, C_pipe, __tmp1_0, __tmp2_0, beta, fpga_C_0);
    HLSLIB_DATAFLOW_FINALIZE();
}
