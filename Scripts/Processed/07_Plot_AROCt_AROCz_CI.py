import os
import numpy as np
import matplotlib.pyplot as plt

#########################################################################################
# CODE DESCRIPTION
# 07_Plot_AROCt_AROCz_CI.py plots the Area Under the ROC curve with the trapezoidal (AROCt) and the 
# binormal (AROCz) approximation. The plots also include confidence intervals (CI).
# Note: runtime negligible.

# INPUT PARAMETERS DESCRIPTION
# Acc (number, in hours): rainfall accumulation to consider.
# VRE_list (list of floats, from 0 to infinite, in mm): list of verifing rainfall events (VRE).
# CL (integer from 0 to 100, in percent): confidence level for the definition of the confidence intervals.
# SystemFC_list (list of strings): list of names of forecasting systems to consider.
# Colour_SystemFC_list (list of strings): colours used to plot the AROC values for different forecasting systems.
# Git_repo (string): repository's local path.
# DirIN (string): relative path containing the real and boostrapped AROC values.
# DirOUT (string): relative path of the directory containing the plots of the real and boostrapped AROC values.

# INPUT PARAMETERS
Acc = 12
VRE_list = [0.2, 10, 25, 50]
CL = 99
SystemFC_list = ["ENS", "ecPoint_MultipleWT", "ecPoint_SingleWT"]
Colour_SystemFC_list = ["darkcyan", "darkorange", "grey"]
Git_repo = "/ec/vol/ecpoint_dev/mofp/Papers_2_Write/ECMWF_TM_Verif_ecPoint_SingleWT"
DirIN = "Data/Compute/03_BSrel_AROCt_AROCz_BS"
DirOUT = "Data/Plot/07_AROCt_AROCz_CI"
#########################################################################################


# Plotting the AROCt and AROCz values for a specific vre
for vre in VRE_list:

      # Setting the figure
      fig, ax = plt.subplots(figsize=(17, 13))
      
      # Plotting the AROCt and AROCz values for a specific forecasting system
      for indSystemFC in range(len(SystemFC_list)):
            
            # Selecting the forecasting system to plot, and its correspondent colour in the plot
            SystemFC = SystemFC_list[indSystemFC]
            Colour_SystemFC = Colour_SystemFC_list[indSystemFC]

            # Reading the steps computed, and the original and bootstrapped AROCt values
            DirIN_temp= Git_repo + "/" + DirIN + "/" + f"{Acc:02d}" + "h/AROCt"
            FileNameIN_temp = "AROCt_" + f"{Acc:02d}" + "h_" + SystemFC + "_" + str(vre) + ".npy"
            StepF = np.load(DirIN_temp + "/" + FileNameIN_temp)[:,0].astype(int)
            aroc = np.load(DirIN_temp + "/" + FileNameIN_temp)[:,1]
            aroc_BS = np.load(DirIN_temp + "/" + FileNameIN_temp)[:,2:]

            # Reading the original and bootstrapped AROCz values
            DirIN_temp= Git_repo + "/" + DirIN + "/" + f"{Acc:02d}" + "h/AROCz"
            FileNameIN_temp = "AROCz_" + f"{Acc:02d}" + "h_" + SystemFC + "_" + str(vre) + ".npy"
            arocz = np.load(DirIN_temp + "/" + FileNameIN_temp)[:,1]
            arocz_BS = np.load(DirIN_temp + "/" + FileNameIN_temp)[:,2:]

            # Computing the confidence intervals from the bootstrapped AROCt values
            alpha = 100 - CL 
            CI_lower = np.nanpercentile(aroc_BS, alpha/2, axis=1)
            CI_upper = np.nanpercentile(aroc_BS, 100 - (alpha/2), axis=1)

            # Computing the confidence intervals from the bootstrapped AROCz values
            alpha = 100 - CL 
            CIz_lower = np.nanpercentile(arocz_BS, alpha/2, axis=1)
            CIz_upper = np.nanpercentile(arocz_BS, 100 - (alpha/2), axis=1)

            # Plotting the AROCt and AROCz values with their CI
            ax.plot(StepF, aroc, "o-", color=Colour_SystemFC, label="AROCt, " + SystemFC, linewidth=2)
            ax.plot(StepF, arocz, "o--", color=Colour_SystemFC, label="AROCz, " + SystemFC, linewidth=2)
            ax.fill_between(StepF, CI_lower, CI_upper, color=Colour_SystemFC, alpha=0.2, edgecolor="none")
            ax.fill_between(StepF, CIz_lower, CIz_upper, color=Colour_SystemFC, alpha=0.2, edgecolor="none")

      # Completing the AROCt and AROCz plots
      DiscStep = ((StepF[-1] - StepF[0]) / (len(StepF)-1))
      ax.set_title("Area Under the ROC curve, Trapezoidal (AROCt) and Binormal (AROCz)\n VRE>=" + str(vre) + "mm/" + str(Acc) + "h, CL=" + str(CL) + "%\n \n ", fontsize=20, pad=20, weight="bold")
      ax.set_xlabel(" \nSteps ad the end of the " + str(Acc) + "-hourly accumulation period [hours]", fontsize=16, labelpad=10)
      ax.set_ylabel("AROCt and AROCz [-]", fontsize=16, labelpad=10)
      ax.set_xlim([StepF[0]-1, StepF[-1]+1])
      ax.set_ylim([0.5,1])
      ax.set_xticks(np.arange(StepF[0], (StepF[-1]+1), DiscStep))
      ax.set_yticks(np.arange(0.5,1.01, 0.1))
      ax.xaxis.set_tick_params(labelsize=16, rotation=90)
      ax.yaxis.set_tick_params(labelsize=16)
      ax.legend(loc="upper center", bbox_to_anchor=(0.5, 1.085), ncol=3, fontsize=16, frameon=False)
      ax.grid()

      # Saving the AROCt and AROCz plots
      DirOUT_temp= Git_repo + "/" + DirOUT + "/" + f"{Acc:02d}" + "h"
      FileNameOUT_temp = "AROCt_AROCz_" + f"{Acc:02d}" + "h_" + SystemFC + "_" + str(vre) + ".jpeg"
      if not os.path.exists(DirOUT_temp):
            os.makedirs(DirOUT_temp)
      plt.savefig(DirOUT_temp + "/" + FileNameOUT_temp)
      plt.close() 