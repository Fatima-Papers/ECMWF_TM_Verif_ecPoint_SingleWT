import os
import numpy as np
import matplotlib.pyplot as plt

##############################################################################
# CODE DESCRIPTION
# 04_Plot_Real_Binormal_ROC_NoBS.py plots "real" and "binormal" ROC curves with no 
# confidence intervals.
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
Colour_SystemFC_list = ["darkcyan", "orangered", "dimgray"]
Git_repo = "/ec/vol/ecpoint_dev/mofp/Papers_2_Write/Verif_ecPoint_SingleWT"
DirIN_HR_FAR = "Data/Compute/02_Real_Binormal_HR_FAR_NoBS"
DirIN_AROC = "Data/Compute/03_BSrel_AROCt_AROCz_BS"
DirOUT = "Data/Plot/04_Real_Binormal_ROC_NoBS"
##############################################################################


# Plotting the "real" and "binormal" ROC curves for a specific vre
for vre in VRE_list:

      # Setting the output directory
      MainDirOUT = Git_repo + "/" + DirOUT + "/" + f"{Acc:02d}" + "h/" + str(vre)
      if not os.path.exists(MainDirOUT):
            os.makedirs(MainDirOUT)

      # Plotting the "real" and "binormal" ROC curves for a specific lead time
      for StepF in range(StepF_Start, (StepF_Final+1), Disc_Step):

            print(" - Plotting the 'real' and 'binormal' ROC curves for VRE >= " + str(vre) + " mm/" + str(Acc) + "h and StepF = " + str(StepF))

            # Initialize figure that will plot the "real" and "binormal" ROC curves
            plt.figure(figsize=(12,12))

            # Plotting the "real" and "binormal" ROC curves for a specific forecasting system
            for indSystemFC in range(len(SystemFC_list)):
                  
                  # Selecting the forecasting system to plot, and its correspondent colour in the plot
                  SystemFC = SystemFC_list[indSystemFC]
                  Colour_SystemFC = Colour_SystemFC_list[indSystemFC]

                  # Reading the "real" and "binormal" AROC values
                  FileIN_AROCt = Git_repo + "/" + DirIN_AROC + "/" + f"{Acc:02d}" + "h/AROCt/AROCt_" + f"{Acc:02d}" + "h_" + SystemFC + "_" + str(vre) + ".npy"
                  FileIN_AROCz = Git_repo + "/" + DirIN_AROC + "/" + f"{Acc:02d}" + "h/AROCz/AROCz_" + f"{Acc:02d}" + "h_" + SystemFC + "_" + str(vre) + ".npy"
                  AROCt = np.load(FileIN_AROCt)
                  AROCz = np.load(FileIN_AROCz)
                  
                  # Indexing the step to plot for AROCt and AROCz
                  StepF_list = AROCt[:,0].astype(int)
                  ind_StepF = np.where(StepF_list == StepF)[0][0]

                  # Reading the "real" and "binormal" HRs and FARs
                  FileIN_HR = Git_repo + "/" + DirIN_HR_FAR + "/" + f"{Acc:02d}" + "h/" + SystemFC + "/" + str(vre) + "/" + "HR_" +  f"{Acc:02d}" + "h_" + SystemFC + "_" + str(vre) + "_" + f"{StepF:03d}" + ".npy"
                  FileIN_FAR = Git_repo + "/" + DirIN_HR_FAR + "/" + f"{Acc:02d}" + "h/" + SystemFC + "/" + str(vre) + "/" + "FAR_" +  f"{Acc:02d}" + "h_" + SystemFC + "_" + str(vre) + "_" + f"{StepF:03d}" + ".npy"
                  FileIN_HRz = Git_repo + "/" + DirIN_HR_FAR + "/" + f"{Acc:02d}" + "h/" + SystemFC + "/" + str(vre) + "/" + "HRz_" +  f"{Acc:02d}" + "h_" + SystemFC + "_" + str(vre) + "_" + f"{StepF:03d}" + ".npy"
                  FileIN_FARz = Git_repo + "/" + DirIN_HR_FAR + "/" + f"{Acc:02d}" + "h/" + SystemFC + "/" + str(vre) + "/" + "FARz_" +  f"{Acc:02d}" + "h_" + SystemFC + "_" + str(vre) + "_" + f"{StepF:03d}" + ".npy"
                  HR = np.load(FileIN_HR)
                  FAR = np.load(FileIN_FAR)
                  HRz = np.load(FileIN_HRz)
                  FARz = np.load(FileIN_FARz)
                  
                  # Plotting the "real" and "binormal" ROC curves
                  label_real = "ROC, " + SystemFC + " (AROCt = " + str(round(AROCt[ind_StepF,1],3)) + ")"
                  label_binormal = "ROCz, " + SystemFC + " (AROCz = " + str(round(AROCz[ind_StepF,1],3)) + ")"
                  plt.plot(FAR, HR, "o-", color=Colour_SystemFC, label=label_real, linewidth=3)
                  plt.plot(FARz, HRz, "--", color=Colour_SystemFC, label=label_binormal, linewidth=3)
                  
            # Compliting the plot
            plt.plot([0,1], [0,1], "-", color="black", linewidth=3)
            plt.title("ROC curves, Real (ROC) and Binormal (ROCz)\n VRE >= " + str(vre) + "mm/" + str(Acc) + "h, StepF = " + str(StepF), fontsize = 24, pad=20, weight="bold")
            plt.xlabel("False Alarm Rate, FAR [-]", fontsize = 24, labelpad=10)
            plt.ylabel("Hit Rate, HR [-]", fontsize = 24, labelpad=10)
            plt.xlim(0,1)
            plt.xticks(np.arange(0,1.1, 0.1), fontsize = 24)
            plt.ylim(0,1)
            plt.yticks(np.arange(0,1.1, 0.1), fontsize = 24)
            plt.legend(loc="lower right", fontsize=18)
            plt.grid(True, color = "grey", linewidth = 0.5)

            # Saving the "real" and "binormal" ROC curves
            print(" - Saving the 'real' and 'binormal' ROC curves")
            FileNameOUT_temp = "Real_Binormal_ROC_" + f"{Acc:02d}" + "h_" + str(vre) + "_" + f"{StepF:03d}" + ".jpeg"
            plt.savefig(MainDirOUT + "/" + FileNameOUT_temp)
            plt.close()