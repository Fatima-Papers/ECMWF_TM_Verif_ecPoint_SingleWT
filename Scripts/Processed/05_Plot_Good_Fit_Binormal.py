import os
import numpy as np
import matplotlib.pyplot as plt

##############################################################################
# CODE DESCRIPTION
# 05_Plot_Goodness_Fit_Test_Binormal.py plots the diagrams that show whether the binormal 
# curve approximates well the real ROC curve. 
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
VRE_list = [0.2,10, 25, 50]
SystemFC_list = ["ENS", "ecPoint_MultipleWT", "ecPoint_SingleWT"]
Colour_SystemFC_list = ["darkcyan", "darkorange", "grey"]
Git_repo = "/ec/vol/ecpoint_dev/mofp/Papers_2_Write/ECMWF_TM_Verif_ecPoint_SingleWT"
DirIN = "Data/Compute/02_Real_Binormal_HR_FAR_NoBS"
DirOUT = "Data/Plot/05_Goodness_Fit_Test_Binormal"
##############################################################################

# Plotting the goodness fit test for a specific vre
for vre in VRE_list:

      # Setting the output directory
      MainDirOUT = Git_repo + "/" + DirOUT + "/" + f"{Acc:02d}" + "h/" + str(vre)
      if not os.path.exists(MainDirOUT):
            os.makedirs(MainDirOUT)

      # Plotting the goodness fit test for a specific lead time
      for StepF in range(StepF_Start, (StepF_Final+1), Disc_Step):

            print(" - Plotting the 'real' and 'binormal' ROC curves for VRE >= " + str(vre) + " mm/" + str(Acc) + "h and StepF = " + str(StepF))

            # Initialize figure that will plot the goodness fit test
            fig, axs = plt.subplots(1,3, figsize=(27, 14))

            # Plotting the goodness fit test for a specific forecasting system
            ind_SystemFC = 0
            for indSystemFC in range(len(SystemFC_list)):
                  
                  # Selecting the forecasting system to plot, and its correspondent colour in the plot
                  SystemFC = SystemFC_list[indSystemFC]
                  Colour_SystemFC = Colour_SystemFC_list[indSystemFC]

                  # Reading the input files that contain the variables to run the goodness fit test
                  DirIN_temp = Git_repo + "/" + DirIN + "/" + f"{Acc:02d}" + "h/" + SystemFC + "/" + str(vre)
                  FileIN_x_LR = "x_LR_" + f"{Acc:02d}" + "h_" + SystemFC + "_" + str(vre) + "_" + f"{StepF:03d}" + ".npy"
                  FileIN_y_LR = "y_LR_" + f"{Acc:02d}" + "h_" + SystemFC + "_" + str(vre) + "_" + f"{StepF:03d}" + ".npy"
                  FileIN_HRz_inv = "HRz_inv_" + f"{Acc:02d}" + "h_" + SystemFC + "_" + str(vre) + "_" + f"{StepF:03d}" + ".npy"
                  FileIN_FARz_inv = "FARz_inv_" + f"{Acc:02d}" + "h_" + SystemFC + "_" + str(vre) + "_" + f"{StepF:03d}" + ".npy"
                  x_LR = np.load(DirIN_temp + "/" + FileIN_x_LR)
                  y_LR = np.load(DirIN_temp + "/" + FileIN_y_LR)
                  HRz_inv = np.load(DirIN_temp + "/" + FileIN_HRz_inv)
                  FARz_inv = np.load(DirIN_temp + "/" + FileIN_FARz_inv)

                  # Plotting the goodness fit test
                  axs[ind_SystemFC].plot(x_LR, y_LR, "b-")
                  axs[ind_SystemFC].plot(FARz_inv, HRz_inv, "ro")
                  axs[ind_SystemFC].set_title(SystemFC, fontsize=24, pad = 10)
                  axs[ind_SystemFC].set_xlabel("Z-score of False Alarm Rate", fontsize=24, labelpad=15)
                  axs[ind_SystemFC].set_ylabel("Z-score of Hit Rate", fontsize=24)
                  axs[ind_SystemFC].xaxis.set_tick_params(labelsize=24)
                  axs[ind_SystemFC].yaxis.set_tick_params(labelsize=24)
                  
                  ind_SystemFC = ind_SystemFC + 1

            # Completing plot
            fig.suptitle("Goodness fit test for binormal approximation of ROC curve\n VRE>=" + str(vre) + "mm/" + str(Acc) + "h, StepF = " + str(StepF) + "\n \n ", fontsize=24, weight="bold")
            
            # Saving the "real" and "binormal" ROC curves
            print(" - Saving the plot")
            FileNameOUT_temp = "Goodness_Fit_Test_Binormal_" + f"{Acc:02d}" + "h_" + str(vre) + "_" + f"{StepF:03d}" + ".jpeg"
            plt.savefig(MainDirOUT + "/" + FileNameOUT_temp)
            plt.close()