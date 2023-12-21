#!/bin/bash

#SBATCH --job-name=Count_EM_OBS_Exceeding_VRT
#SBATCH --output=LogATOS/Count_EM_OBS_Exceeding_VRT-%J.out
#SBATCH --error=LogATOS/Count_EM_OBS_Exceeding_VRT-%J.out
#SBATCH --cpus-per-task=64
#SBATCH --mem=128G
#SBATCH --qos=nf
#SBATCH --mail-type=FAIL
#SBATCH --mail-user=fatima.pillosu@ecmwf.int

# INPUTS
DateS=${1}
DateF=${2}

# CODE
python3 01_Compute_Count_EM_OBS_Exceeding_VRT.py ${DateS} ${DateF}