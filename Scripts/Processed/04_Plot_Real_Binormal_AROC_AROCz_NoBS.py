import os as os
import numpy as np
import matplotlib.pyplot as plt

##############################################################################
# CODE DESCRIPTION
# 04_Plot_Real_Binormal_AROC_AROCz_NoBS.py plots "real" and "binormal" AROC values with 
# no confidence intervals.
# Code runtime: negligible.

# INPUT PARAMETERS DESCRIPTION
# Acc (number, in hours): rainfall accumulation to consider.
# VRE_list (list of floats, from 0 to infinite, in mm): list of verifing rainfall events (VRE).
# SystemFC_list (list of strings): list of names of forecasting systems to consider.
# Colour_SystemFC_list (list of strings): list of colours to assign to each forecasting system.
# Git_repo (string): repository's local path.
# DirIN (string): relative path of the input directoy containing the pre-computed AROCs.
# DirOUT (string): relative path of the output directory containing the AROC plots.

# INPUT PARAMETERS
Acc = 12
VRE_list = [0.2, 10, 25, 50]
SystemFC_list = ["ENS", "ecPoint_MultipleWT", "ecPoint_SingleWT"]
Colour_SystemFC_list = ["darkcyan", "darkorange", "grey"]
Git_repo = "/ec/vol/ecpoint_dev/mofp/Papers_2_Write/ECMWF_TM_Verif_ecPoint_SingleWT"
DirIN = "Data/Compute/02_Real_Binormal_HR_FAR_AROC_NoBS"
DirOUT = "Data/Plot/04_Real_Binormal_AROC_NoBS"
##############################################################################


# Setting the output directory
MainDirOUT = Git_repo + "/" + DirOUT + "/" + f"{Acc:02d}" + "h"
if not os.path.exists(MainDirOUT):
      os.makedirs(MainDirOUT)

# Plotting the "real" and the "binormal" AROC for a specific vre
for vre in VRE_list:

      print(" - Plotting the 'real' and 'binormal' AROC for VRE >= " + str(vre) + " mm/" + str(Acc) + "h")

      # Setting the figure
      fig, ax = plt.subplots(figsize=(17, 13))

      # Plotting the "real" and the "binormal" AROC for a specific forecasting system
      for indSystemFC in range(len(SystemFC_list)):
            
            # Selecting the forecasting system to consider and the colour to associate it in the plot
            SystemFC = SystemFC_list[indSystemFC]
            Colour_SystemFC = Colour_SystemFC_list[indSystemFC]
            
            # Reading the "real" and "binormal" AROC values
            FileIN_AROC = Git_repo + "/" + DirIN + "/" + str(Acc) + "h/AROC_" + str(Acc) + "h_" + SystemFC + "_" + str(vre) + ".npy"
            FileIN_AROCz = Git_repo + "/" + DirIN + "/" + str(Acc) + "h/AROCz_" + str(Acc) + "h_" + SystemFC + "_" + str(vre) + ".npy"
            AROC = np.load(FileIN_AROC)
            AROCz = np.load(FileIN_AROCz)
            
            # Plotting the "real" and "binormal" AROC values
            StepF = AROC[:,0]
            plt.plot(StepF, AROC[:,1], "-o", color=Colour_SystemFC, label="AROC, " + SystemFC)
            plt.plot(StepF, AROCz[:,1], "--o", color=Colour_SystemFC, label="AROCz, " + SystemFC)

      # Completing the plot 
      DiscStep = ((StepF[-1] - StepF[0]) / (len(StepF)-1))
      ax.set_title("Area Under the ROC curve, Real (AROC) and Binormal (AROCz)\n VRE>=" + str(vre) + "mm/" + str(Acc) + "h\n \n ", fontsize=20, pad=20, weight="bold")
      ax.set_xlabel(" \nSteps ad the end of the " + str(Acc) + "-hourly accumulation period [hours]", fontsize=16, labelpad=10)
      ax.set_ylabel("AROC and AROCz [-]", fontsize=16, labelpad=10)
      ax.set_xlim([StepF[0]-1, StepF[-1]+1])
      ax.set_ylim([0.5,1])
      ax.set_xticks(np.arange(StepF[0], (StepF[-1]+1), DiscStep))
      ax.set_yticks(np.arange(0.5,1.01, 0.1))
      ax.xaxis.set_tick_params(labelsize=16, rotation=90)
      ax.yaxis.set_tick_params(labelsize=16)
      ax.legend(loc="upper center", bbox_to_anchor=(0.5, 1.085), ncol=3, fontsize=16, frameon=False)
      ax.grid()
      
      # Saving the "real" and "binormal" AROC plots
      print(" - Saving the 'real' and 'binormal' AROC plot")
      FileNameOUT_temp = "Real_Binormal_AROC_NoBS_" + f"{Acc:02d}" + "h_"+ str(vre) + ".jpeg"
      plt.savefig(MainDirOUT + "/" + FileNameOUT_temp)
      plt.close()