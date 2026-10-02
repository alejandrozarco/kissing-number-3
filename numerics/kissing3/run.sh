#!/bin/bash
# usage: ./run.sh <k3.py args...>   (nice 19, single thread; log appended to logs/)
cd "$(dirname "$0")"; mkdir -p logs
export OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1 VECLIB_MAXIMUM_THREADS=1 NUMEXPR_NUM_THREADS=1 RAYON_NUM_THREADS=1
exec nice -n 19 python3 k3.py "$@" 2>&1 | tee -a "logs/$(echo "$@ ${DEL:+del$DEL} ${F3:+F3$F3}" | tr ' ' '_').log"
