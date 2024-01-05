#!/bin/bash

sbatch 06a_SubmitATOS_AROCt_AROCz_BS.sh 0.2 ENS
sbatch 06a_SubmitATOS_AROCt_AROCz_BS.sh 10 ENS
sbatch 06a_SubmitATOS_AROCt_AROCz_BS.sh 50 ENS
sbatch 06a_SubmitATOS_AROCt_AROCz_BS.sh 0.2 ecPoint_MultipleWT
sbatch 06a_SubmitATOS_AROCt_AROCz_BS.sh 10 ecPoint_MultipleWT
sbatch 06a_SubmitATOS_AROCt_AROCz_BS.sh 50 ecPoint_MultipleWT
sbatch 06a_SubmitATOS_AROCt_AROCz_BS.sh 0.2 ecPoint_SingleWT
sbatch 06a_SubmitATOS_AROCt_AROCz_BS.sh 10 ecPoint_SingleWT
sbatch 06a_SubmitATOS_AROCt_AROCz_BS.sh 50 ecPoint_SingleWT