#!/bin/bash

#SBATCH --job-name=AROCt_AROCz_BS
#SBATCH --output=LogATOS/AROCt_AROCz_BS-%J.out
#SBATCH --error=LogATOS/AROCt_AROCz_BS-%J.out
#SBATCH --cpus-per-task=64
#SBATCH --mem=128G
#SBATCH --qos=nf
#SBATCH --mail-type=FAIL
#SBATCH --mail-user=fatima.pillosu@ecmwf.int

# INPUTS
VRT_list=${1}
SystemFC_list=${2}

# CODE
python3 06_Compute_AROCt_AROCz_BS.py ${VRT_list} ${SystemFC_list}