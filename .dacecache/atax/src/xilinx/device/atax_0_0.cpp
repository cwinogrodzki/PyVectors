#include <dace/fpga_device.h>
#include <dace/math.h>
#include <dace/complex.h>
constexpr long long M = 60;
constexpr long long N = 70;

struct atax_state_t {
    dace_fpga_context *fpga_context;
};


void gemv_0_0_4(const double* _A, const double* _x, double* _y) {
    #pragma HLS INLINE

    {
        {
            {
                const int ty = 0; // Degenerate loop
                double y_local[60];
                {
                    {
                        const int tx = 0; // Degenerate loop
                        double x_local[70];
                        {
                            for (int ix = 0; ix < 70; ix += 1) {
                                #pragma HLS PIPELINE II=1
                                #pragma HLS LOOP_FLATTEN
                                {
                                    double x_memory = _x[(ix + (70 * tx))];
                                    double x_buffer;

                                    ///////////////////
                                    // Tasklet code (read_x)
                                    x_buffer = x_memory;
                                    ///////////////////

                                    dace::Write<double, 1>(&x_local[ix], x_buffer);
                                    #pragma HLS DEPENDENCE variable=x_local false
                                }
                            }
                        }
                        {
                            for (int iy = 0; iy < 60; iy += 1) {
                                #pragma HLS DEPENDENCE variable=y_local false
                                double partial_sums[16];
                                #pragma HLS ARRAY_PARTITION variable=partial_sums complete
                                double accumulate_sum;
                                {
                                    for (int ix = 0; ix < 70; ix += 1) {
                                        #pragma HLS PIPELINE II=1
                                        #pragma HLS LOOP_FLATTEN
                                        double product_vector;
                                        double accumulate_product;
                                        double product_scalar;
                                        {
                                            double A_in = _A[(((ix + (70 * iy)) + (70 * tx)) + (4200 * ty))];
                                            double x_in = x_local[ix];
                                            double product;

                                            ///////////////////
                                            // Tasklet code (multiply)
                                            product = (A_in * x_in);
                                            ///////////////////

                                            product_vector = product;
                                        }
                                        dace::Write<double, 1>(product_scalar, dace::Read<double, 1>(product_vector));
                                        {
                                            double acc_out;

                                            ///////////////////
                                            // Tasklet code (init_reduce_vector)
                                            acc_out = 0;
                                            ///////////////////

                                            accumulate_product = acc_out;
                                        }
                                        {
                                            {
                                                const int u = 0; // Degenerate loop
                                                {
                                                    double product_in = product_scalar;
                                                    double acc_in = accumulate_product;
                                                    double acc_out;

                                                    ///////////////////
                                                    // Tasklet code (reduce_vector)
                                                    acc_out = (product_in + acc_in);
                                                    ///////////////////

                                                    accumulate_product = acc_out;
                                                }
                                            }
                                        }
                                        {
                                            double y_in = accumulate_product;
                                            double acc_in = partial_sums[(ix % 16)];
                                            double acc_out;

                                            ///////////////////
                                            // Tasklet code (update_y)
                                            auto prev = ((ix >= 16) ? acc_in : 0);
                                            acc_out = (prev + y_in);
                                            ///////////////////

                                            dace::Write<double, 1>(&partial_sums[(ix % 16)], acc_out);
                                        }
                                    }
                                }
                                {
                                    for (int u = 0; u < 16; u += 1) {
                                        #pragma HLS UNROLL
                                        {
                                            double sum_in = accumulate_sum;
                                            double val_in = partial_sums[u];
                                            double sum_out;

                                            ///////////////////
                                            // Tasklet code (reduce_partial_sums)
                                            auto prev = ((u > 0) ? sum_in : 0);
                                            sum_out = (prev + val_in);
                                            ///////////////////

                                            accumulate_sum = sum_out;
                                        }
                                    }
                                }
                                {
                                    double val = accumulate_sum;
                                    double buffer_in = y_local[iy];
                                    double buffer_out;

                                    ///////////////////
                                    // Tasklet code (combine_y)
                                    auto prev = ((tx > 0) ? buffer_in : 0);
                                    buffer_out = (prev + val);
                                    ///////////////////

                                    dace::Write<double, 1>(&y_local[iy], buffer_out);
                                    #pragma HLS DEPENDENCE variable=y_local false
                                }
                            }
                        }
                    }
                }
                {
                    for (int iy = 0; iy < 60; iy += 1) {
                        #pragma HLS PIPELINE II=1
                        #pragma HLS LOOP_FLATTEN
                        {
                            double y_buffer = y_local[iy];
                            double y_memory;

                            ///////////////////
                            // Tasklet code (write_y)
                            y_memory = y_buffer;
                            ///////////////////

                            *(_y + (iy + (60 * ty))) = y_memory;
                        }
                    }
                }
            }
        }

    }
    
}

void gemv_0_0_5(const double* _A, const double* _x, double* _y) {
    #pragma HLS INLINE

    {
        {
            {
                const int ty = 0; // Degenerate loop
                double y_local[70];
                {
                    {
                        const int tx = 0; // Degenerate loop
                        double x_local[60];
                        {
                            for (int ix = 0; ix < 60; ix += 1) {
                                #pragma HLS PIPELINE II=1
                                #pragma HLS LOOP_FLATTEN
                                {
                                    double x_memory = _x[(ix + (60 * tx))];
                                    double x_buffer;

                                    ///////////////////
                                    // Tasklet code (read_x)
                                    x_buffer = x_memory;
                                    ///////////////////

                                    dace::Write<double, 1>(&x_local[ix], x_buffer);
                                    #pragma HLS DEPENDENCE variable=x_local false
                                }
                            }
                        }
                        {
                            for (int iy = 0; iy < 70; iy += 1) {
                                #pragma HLS DEPENDENCE variable=y_local false
                                double partial_sums[16];
                                #pragma HLS ARRAY_PARTITION variable=partial_sums complete
                                double accumulate_sum;
                                {
                                    for (int ix = 0; ix < 60; ix += 1) {
                                        #pragma HLS PIPELINE II=1
                                        #pragma HLS LOOP_FLATTEN
                                        double product_vector;
                                        double accumulate_product;
                                        double product_scalar;
                                        {
                                            double A_in = _A[((((70 * ix) + iy) + (4200 * tx)) + (70 * ty))];
                                            double x_in = x_local[ix];
                                            double product;

                                            ///////////////////
                                            // Tasklet code (multiply)
                                            product = (A_in * x_in);
                                            ///////////////////

                                            product_vector = product;
                                        }
                                        dace::Write<double, 1>(product_scalar, dace::Read<double, 1>(product_vector));
                                        {
                                            double acc_out;

                                            ///////////////////
                                            // Tasklet code (init_reduce_vector)
                                            acc_out = 0;
                                            ///////////////////

                                            accumulate_product = acc_out;
                                        }
                                        {
                                            {
                                                const int u = 0; // Degenerate loop
                                                {
                                                    double product_in = product_scalar;
                                                    double acc_in = accumulate_product;
                                                    double acc_out;

                                                    ///////////////////
                                                    // Tasklet code (reduce_vector)
                                                    acc_out = (product_in + acc_in);
                                                    ///////////////////

                                                    accumulate_product = acc_out;
                                                }
                                            }
                                        }
                                        {
                                            double y_in = accumulate_product;
                                            double acc_in = partial_sums[(ix % 16)];
                                            double acc_out;

                                            ///////////////////
                                            // Tasklet code (update_y)
                                            auto prev = ((ix >= 16) ? acc_in : 0);
                                            acc_out = (prev + y_in);
                                            ///////////////////

                                            dace::Write<double, 1>(&partial_sums[(ix % 16)], acc_out);
                                        }
                                    }
                                }
                                {
                                    for (int u = 0; u < 16; u += 1) {
                                        #pragma HLS UNROLL
                                        {
                                            double sum_in = accumulate_sum;
                                            double val_in = partial_sums[u];
                                            double sum_out;

                                            ///////////////////
                                            // Tasklet code (reduce_partial_sums)
                                            auto prev = ((u > 0) ? sum_in : 0);
                                            sum_out = (prev + val_in);
                                            ///////////////////

                                            accumulate_sum = sum_out;
                                        }
                                    }
                                }
                                {
                                    double val = accumulate_sum;
                                    double buffer_in = y_local[iy];
                                    double buffer_out;

                                    ///////////////////
                                    // Tasklet code (combine_y)
                                    auto prev = ((tx > 0) ? buffer_in : 0);
                                    buffer_out = (prev + val);
                                    ///////////////////

                                    dace::Write<double, 1>(&y_local[iy], buffer_out);
                                    #pragma HLS DEPENDENCE variable=y_local false
                                }
                            }
                        }
                    }
                }
                {
                    for (int iy = 0; iy < 70; iy += 1) {
                        #pragma HLS PIPELINE II=1
                        #pragma HLS LOOP_FLATTEN
                        {
                            double y_buffer = y_local[iy];
                            double y_memory;

                            ///////////////////
                            // Tasklet code (write_y)
                            y_memory = y_buffer;
                            ///////////////////

                            *(_y + (iy + (70 * ty))) = y_memory;
                        }
                    }
                }
            }
        }

    }
    
}

void module__MatMult_gemv_4__MatMult_gemvt_5_0(double *__tmp0, double *fpga_A, double *fpga___return, double *fpga_x) {

    gemv_0_0_4(&fpga_A[0], &fpga_x[0], &__tmp0[0]);
    gemv_0_0_5(&fpga_A[0], &__tmp0[0], &fpga___return[0]);
}

DACE_EXPORTED void atax_0_0(double *__tmp0_0, double *fpga_A_0, double *fpga___return_0, double *fpga_x_0) {
    #pragma HLS INTERFACE m_axi port=__tmp0_0 offset=slave bundle=gmem0
    #pragma HLS INTERFACE m_axi port=fpga_A_0 offset=slave bundle=gmem1
    #pragma HLS INTERFACE m_axi port=fpga___return_0 offset=slave bundle=gmem2
    #pragma HLS INTERFACE m_axi port=fpga_x_0 offset=slave bundle=gmem3
    #pragma HLS INTERFACE s_axilite port=__tmp0_0 bundle=control
    #pragma HLS INTERFACE s_axilite port=fpga_A_0 bundle=control
    #pragma HLS INTERFACE s_axilite port=fpga___return_0 bundle=control
    #pragma HLS INTERFACE s_axilite port=fpga_x_0 bundle=control
    #pragma HLS INTERFACE s_axilite port=return bundle=control
    
    #pragma HLS DATAFLOW
    
    HLSLIB_DATAFLOW_INIT();
    HLSLIB_DATAFLOW_FUNCTION(module__MatMult_gemv_4__MatMult_gemvt_5_0, __tmp0_0, fpga_A_0, fpga___return_0, fpga_x_0);
    HLSLIB_DATAFLOW_FINALIZE();
}
