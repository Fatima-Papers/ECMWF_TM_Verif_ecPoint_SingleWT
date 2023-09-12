import os
import numpy as np
import matplotlib.pyplot as plt

##############################################################################
# CODE DESCRIPTION
# 04_Plot_Real_Binormal_ROC_NoBS.py plots "real" and "binormal" ROC curves with no 
# confidence intervals.
# Code runtime: the code takes 5 minutes to run in serial.

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
DirIN = "Data/Compute/02_Real_Binormal_HR_FAR_AROC_NoBS"
DirOUT = "Data/Plot/04_Real_Binormal_ROC_NoBS"
##############################################################################


# Setting the output directory
MainDirOUT = Git_repo + "/" + DirOUT + "/" + f"{Acc:02d}" + "h"
if not os.path.exists(MainDirOUT):
      os.makedirs(MainDirOUT)

# Plotting the "real" and "binormal" ROC curves for a specific vre
for vre in VRE_list:

      # Plotting the "real" and "binormal" ROC curves for a specific lead time
      indStepF = 0
      for StepF in range(StepF_Start, (StepF_Final+1), Disc_Step):

            print(" - Plotting the 'real' and 'binormal' ROC curves for VRE >= " + str(vre) + " mm/" + str(Acc) + "h and StepF = " + str(StepF))

            # Initialize figure that will plot the "real" and "binormal" ROC curves
            plt.figure(figsize=(10,10))

            # Plotting the "real" and "binormal" ROC curves for a specific forecasting system
            for indSystemFC in range(len(SystemFC_list)):
                  
                  # Selecting the forecasting system to plot, and its correspondent colour in the plot
                  SystemFC = SystemFC_list[indSystemFC]
                  Colour_SystemFC = Colour_SystemFC_list[indSystemFC]

                  # Reading the "real" and "binormal" AROC values
                  FileIN_AROC = Git_repo + "/" + DirIN + "/" + f"{Acc:02d}" + "h/" + SystemFC + "/" + str(vre) + "/AROC_" + f"{Acc:02d}" + "h_" + SystemFC + "_" + str(vre) + ".npy"
                  FileIN_AROCz = Git_repo + "/" + DirIN + "/" + f"{Acc:02d}" + "h/AROCz_" + f"{Acc:02d}" + "h_" + SystemFC + "_" + str(vre) + ".npy"
                  AROC = np.load(FileIN_AROC)
                  AROCz = np.load(FileIN_AROCz)

                  # Reading the "real" and "binormal" HRs and FARs
                  FileIN_HR = Git_repo + "/" + DirIN + "/" + str(Acc) + "h/HR_" + str(Acc) + "h_" + SystemFC + "_" + str(vre) + "_" + f"{StepF:03d}" + ".npy"
                  FileIN_FAR = Git_repo + "/" + DirIN + "/" + str(Acc) + "h/FAR_" + str(Acc) + "h_" + SystemFC + "_" + str(vre) + "_" + f"{StepF:03d}" + ".npy"
                  FileIN_HRz = Git_repo + "/" + DirIN + "/" + str(Acc) + "h/HRz_" + str(Acc) + "h_" + SystemFC + "_" + str(vre) + "_" + f"{StepF:03d}" + ".npy"
                  FileIN_FARz = Git_repo + "/" + DirIN + "/" + str(Acc) + "h/FARz_" + str(Acc) + "h_" + SystemFC + "_" + str(vre) + "_" + f"{StepF:03d}" + ".npy"
                  HR = np.load(FileIN_HR)
                  FAR = np.load(FileIN_FAR)
                  HRz = np.load(FileIN_HRz)
                  FARz = np.load(FileIN_FARz)
                  
                  # Plotting the "real" and "binormal" ROC curves
                  label_real = "ROC, " + SystemFC + " (AROCt = " + str(round(AROC[indStepF,1],3)) + ")"
                  label_binormal = "ROCz, " + SystemFC + " (AROCz = " + str(round(AROCz[indStepF,1],3)) + ")"
                  plt.plot(FAR, HR, "o-", color=Colour_SystemFC, label=label_real, linewidth=2)
                  plt.plot(FARz, HRz, "--", color=Colour_SystemFC, label=label_binormal, linewidth=2)
            
            indStepF = indStepF + 1

            # Completing the plot
            plt.plot([0,1], [0,1], "-", color="black", linewidth=3)
            plt.title("ROC curves, Real (ROC) and Binormal (ROCz)\n VRE >= " + str(vre) + "mm/" + str(Acc) + "h, StepF = " + str(StepF), fontsize = 20, pad=20, weight="bold")
            plt.xlabel(" \n False Alarm Rate [-]", fontsize = 16)
            plt.ylabel("Hit Rate [-]\n ", fontsize = 16)
            plt.xlim(0,1)
            plt.xticks(np.arange(0,1.1, 0.1), fontsize = 16)
            plt.ylim(0,1)
            plt.yticks(np.arange(0,1.1, 0.1), fontsize = 16)
            plt.legend(loc="lower right", fontsize=15)
            plt.grid(True, color = "grey", linewidth = 0.5)

            # Saving the "real" and "binormal" ROC curves
            print(" - Saving the 'real' and 'binormal' AROC plot")
            FileNameOUT_temp = "Real_Binormal_ROC_NoBS_" + f"{Acc:02d}" + "h_" + str(vre) + "_" + f"{StepF:03d}" + ".jpeg"
            plt.savefig(MainDirOUT + "/" + FileNameOUT_temp)
            plt.close()