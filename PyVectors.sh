#!/bin/bash

#framework, kernel, iter, device
KERNEL=$1
FRAMEWORK=$2
BLAS=$3
ITER=$4
DEVICE=$5
N=$6

eval "$(conda shell.bash hook)"

# if [ "$DEVICE" = "cpu" ]; then
# 	salloc -p skylake-gold
# elif [ "$DEVICE" = "amdcpu" ]; then
# 	salloc -p shared-milan
# elif [ "$DEVICE" = "amdgpu" ]; then
# 	salloc -p shared-gpu-amd-mi100
# 	module load rocm
# fi

if  [ "$BLAS" = "MKL" ]; then
	conda activate mkl
elif [ "$BLAS" = "OpenBLAS" ]; then
	conda activate openblas
elif [ "$BLAS" = "BLIS" ]; then
	conda activate blis
else [ "$BLAS" = "oneAPI" ]
	conda activate idp
fi

echo "conda env: $CONDA_DEFAULT_ENV"
echo "kernel/framework: $KERNEL $FRAMEWORK"
echo "problem size: $N"
echo "iterations: $ITER"

print_progress_bar() {
    local percent=$(( ($1 * 100) / $2 ))
    local done_chars=$(( ($percent * 3) / 10 ))
    local left_chars=$(( 30 - $done_chars ))

    printf "\rProgress: [%-30s] %d%%" \
           $(printf '#%.0s' $(seq $done_chars)) \
           $percent
}

results=()
for (( i=1; i <= $ITER; ++i ))
do
	result=$(python3 $KERNEL/$KERNEL.py $FRAMEWORK $ITER $DEVICE $N)

        if [ $? -eq 0 ]; then
                results+=($result)
        else
                echo "program failed on run $i."
                #results+=("N/A")
        fi

        #if (( $i % 10 == 0 )); then
	       print_progress_bar $i $ITER
        #fi
done

printf '\nkernel time per iteration (ms)\n'
printf '%s\n' "${results[@]}"

# (IFS=$'\n'; echo "${results[*]}")


