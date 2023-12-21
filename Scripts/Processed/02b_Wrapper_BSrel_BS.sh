#!/bin/bash

sbatch 02a_SubmitATOS_BSrel_BS.sh 0.2 ENS
sbatch 02a_SubmitATOS_BSrel_BS.sh 10 ENS
sbatch 02a_SubmitATOS_BSrel_BS.sh 50 ENS
sbatch 02a_SubmitATOS_BSrel_BS.sh 0.2 ecPoint_MultipleWT
sbatch 02a_SubmitATOS_BSrel_BS.sh 10 ecPoint_MultipleWT
sbatch 02a_SubmitATOS_BSrel_BS.sh 50 ecPoint_MultipleWT
sbatch 02a_SubmitATOS_BSrel_BS.sh 0.2 ecPoint_SingleWT
sbatch 02a_SubmitATOS_BSrel_BS.sh 10 ecPoint_SingleWT
sbatch 02a_SubmitATOS_BSrel_BS.sh 50 ecPoint_SingleWT
