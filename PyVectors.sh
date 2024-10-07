#!/bin/bash

#framework, kernel, iter, device
KERNEL=$1
FRAMEWORK=$2
BLAS=$3
ITER=$4
DEVICE=$5

if [$DEVICE eq "cpu"]; then
	salloc -p skylake-gold
elif [$DEVICE eq "amdcpu"]; then
	salloc -p shared-milan
elif [$DEVICE eq "amdgpu"]; then
	salloc -p shared-gpu-amd-mi100
	module load rocm

if [$BLAS eq "MKL"]; then
	conda activate mkl
elif [$BLAS eq "OpenBLAS"]; then
	conda activate openblas
elif [$BLAS eq "BLIS"]; then
	conda activate blis
else [$BLAS eq "oneAPI"]
	conda activate idp

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
	result=$(python3 $KERNEL/$KERNEL.py $FRAMEWORK $ITER $DEVICE)

        if [ $? -eq 0 ]; then
                results+=($result)
        else
                echo "program failed on run $i."
                #results+=("N/A")
        fi

        #if (( $i % 10 == 0 )); then
        #       ProgressBar $i
	       print_progress_bar $i $ITER
        #fi
done

echo "%s\n" "${results[@]}"


