import os
import numpy as np
import matplotlib.pyplot as plt

##############################################################################
# CODE DESCRIPTION
# 05_Plot_Good_Fit_Binormal.py plots the 
# Code runtime: the code takes 1 minute to run in serial.

# INPUT PARAMETERS DESCRIPTION
# StepF_Start (integer, in hours): first final step of the accumulation periods to consider.
# StepF_Final (integer, in hours): last final step of the accumulation periods to consider.
# Disc_Step (integer, in hours): discretization for the final steps to consider.
# Acc (number, in hours): rainfall accumulation to consider.
# VRE_list (list of floats, from 0 to infinite, in mm): list of verifing rainfall events (VRE).
# SystemFC_list (list of strings): list of names of forecasting systems to consider.
# Colour_SystemFC_list (list of strings): list of colours to assign to each forecasting system.
# Git_repo (string): repository's local path.
# DirIN (string): relative path of the input directoy containing the pre-computed HRs and FARs.
# DirOUT (string): relative path of the directory containing the ROC curve plots.

# INPUT PARAMETERS
StepF_Start =12
StepF_Final = 246
Disc_Step = 6
Acc = 12
VRE_list = [0.2,10,25,50]
SystemFC_list = ["ENS", "ecPoint_MultipleWT", "ecPoint_SingleWT"]
Colour_SystemFC_list = ["darkcyan", "darkorange", "grey"]
Git_repo = "/ec/vol/ecpoint_dev/mofp/Papers_2_Write/ECMWF_TM_Verif_ecPoint_SingleWT"
DirIN_HR_FAR = "Data/Compute/02_Real_Binormal_HR_FAR_NoBS"
DirIN_AROC = "Data/Compute/03_BSrel_AROCt_AROCz_BS"
DirOUT = "Data/Plot/04_Real_Binormal_ROC_NoBS"
##############################################################################


x_LR = np.load("/ec/vol/ecpoint_dev/mofp/Papers_2_Write/ECMWF_TM_Verif_ecPoint_SingleWT/Data/Compute/02_Real_Binormal_HR_FAR_NoBS/12h/ecPoint_MultipleWT/0.2/x_LR_12h_ecPoint_MultipleWT_0.2_012.npy")
y_LR = np.load("/ec/vol/ecpoint_dev/mofp/Papers_2_Write/ECMWF_TM_Verif_ecPoint_SingleWT/Data/Compute/02_Real_Binormal_HR_FAR_NoBS/12h/ecPoint_MultipleWT/0.2/y_LR_12h_ecPoint_MultipleWT_0.2_012.npy")
HRz = 


print(x_LR.shape)


plt.plot(x_LR, y_LR, "-")
plt.show()