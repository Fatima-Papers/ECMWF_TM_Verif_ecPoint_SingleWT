import os
from datetime import datetime, timedelta
import numpy as np
import matplotlib.pyplot as plt

#########################################################################################
# CODE DESCRIPTION
# 04_Plot_Reliability_Sharpness_Diagrams_NoBS.py plots reliability and sharpness diagrams.
# Code Runtime: the script can take up 2 hours to run in serial.

# INPUT PARAMETERS DESCRIPTION
# DateS (date, in format YYYYMMDD): start date of the considered verification period.
# DateF (date, in format YYYYMMDD): final date of the considered verification period.
# StepF_Start (integer, in hours): first final step of the accumulation periods to consider.
# StepF_Final (integer, in hours): last final step of the accumulation periods to consider.
# Disc_Step (integer, in hours): discretization for the final steps to consider.
# Acc (number, in hours): rainfall accumulation to consider.
# VRT_list (list of floats, from 0 to infinite, in mm): list of verifing rainfall events (VRT).
# SystemFC_list (list of strings): list of names of forecasting systems to consider.
# Colour_SystemFC_list (list of strings): colours used to plot the BSrel values for different forecasting systems.
# Git_repo (string): repository's local path.
# DirIN (string): relative path containing the counts of EM and OBS exceeding a certain VRT.
# DirOUT (string): relative path of the directory containing the reliability and sharpness diagrams.

# INPUT PARAMETERS
DateS = datetime(2021, 12, 1, 0)
DateF = datetime(2022, 11, 30, 0)
StepF_Start = 12
StepF_Final = 246
Disc_Step = 6
Acc = 12
VRT_list = [0.2, 10, 50]
SystemFC_list = ["ENS", "ecPoint_MultipleWT", "ecPoint_SingleWT"]
Colour_SystemFC_list = ["darkcyan", "orangered", "dimgray"]
Git_repo = "/ec/vol/ecpoint_dev/mofp/Papers_2_Write/Verif_ecPoint_SingleWT"
DirIN = "Data/Compute/01_Count_EM_OBS_Exceeding_VRT"
DirOUT = "Data/Plot/04_Reliability_Sharpness_Diagrams_NoBS"
#########################################################################################

# Create the probability bins for the diagrams
disc = 0.01
prob_ThrL_list = np.arange(0 - disc/2, 1, disc)
prob_ThrH_list = np.arange(0 + disc/2, 1 + disc, disc)

# Computing the reliability and sharpness diagrams for a specific VRT
for VRT in VRT_list:

      # Computing the reliability and sharpness diagrams for a specific StepF
      for StepF in range(StepF_Start, (StepF_Final+1), Disc_Step):
            
            print("Creating reliability and sharpness diagrams for VRT>=" + str(VRT) + ", StepF=" + str(StepF))

            # Initialize figures that will plot the reliability and the sharpness diagrams
            fig1, ax1 = plt.subplots(figsize=(10, 10)) # reliability diagram
            fig2, ax2 = plt.subplots(figsize=(10, 10)) # zoomed reliability diagram
            fig3, ax3 = plt.subplots(figsize=(10, 10)) # sharpness diagram

            # Computing the reliability and sharpness diagrams for a specific forecasting system
            for ind_SystemFC in range(len(SystemFC_list)):
                  
                  SystemFC = SystemFC_list[ind_SystemFC]
                  Colour_SystemFC = Colour_SystemFC_list[ind_SystemFC]

                  if SystemFC == "ENS":
                        NumEM = 51
                  else:
                        NumEM = 99

                  # Reading the daily counts of ensemble members and observations exceeding the considered verifying rainfall threshold.
                  Count_EM_original = [] # initializing the variable that will contain the counts of ensemble members exceeding the VRT for the original dates
                  Count_OBS_original = [] # initializing the variable that will contain the counts of observations exceeding the VRT for the original dates
                  TheDate = DateS
                  while TheDate <= DateF:
                        DirIN_temp = Git_repo + "/" + DirIN + "/" + f"{Acc:02d}" + "h/" + SystemFC + "/" + str(VRT) + "/" + TheDate.strftime("%Y%m%d%H")
                        FileNameIN_temp = "Count_EM_OBS_" + f"{Acc:02d}" + "h_" + SystemFC + "_" + str(VRT) + "_" + TheDate.strftime("%Y%m%d") + "_" + TheDate.strftime("%H") + "_" + f"{StepF:03d}" + ".npy"
                        if os.path.isfile(DirIN_temp + "/" + FileNameIN_temp): # proceed if the files exists
                              Count_EM_OBS = np.load(DirIN_temp + "/" + FileNameIN_temp)
                              Count_EM_original.extend(Count_EM_OBS[0].tolist())
                              Count_OBS_original.extend(Count_EM_OBS[1].tolist())
                        TheDate += timedelta(days=1)
                  Count_EM_original = np.array(Count_EM_original, dtype=object)
                  Count_OBS_original = np.array(Count_OBS_original, dtype=object)

                  # Calculating the forecast probabilities
                  Prob_EM = Count_EM_original / NumEM

                  # Defining the forecasts and observation absolute/relative frequencies
                  abs_freq_fc = []
                  rel_freq_fc = []
                  rel_freq_obs = []
                  for ind_prob in range(len(prob_ThrL_list)):
                        
                        prob_ThrL = prob_ThrL_list[ind_prob]
                        prob_ThrH = prob_ThrH_list[ind_prob]

                        if ind_prob < NumEM:
                              ind_prob_em_obs = np.where((Prob_EM >= prob_ThrL) & (Prob_EM < prob_ThrH))[0]
                        else:
                              ind_prob_em_obs = np.where((Prob_EM >= prob_ThrL) & (Prob_EM <= prob_ThrH))[0]
                  
                        if len(ind_prob_em_obs) > 0: # to avoid dividing by zero
                              rel_freq_fc. append((prob_ThrL + prob_ThrH) / 2)
                              rel_freq_obs.append(np.sum(Count_OBS_original[ind_prob_em_obs]) / len(Prob_EM[ind_prob_em_obs]))
                              abs_freq_fc.append(len(Count_EM_original[ind_prob_em_obs]))

                  # Plotting the reliability and sharpness diagrams
                  ax1.plot(rel_freq_fc, rel_freq_obs, "-", color=Colour_SystemFC, label=SystemFC, linewidth=4)
                  ax2.plot(rel_freq_fc, rel_freq_obs, "-", color=Colour_SystemFC, label=SystemFC, linewidth=2)
                  ax3.plot(rel_freq_fc, abs_freq_fc, "-", color=Colour_SystemFC, label=SystemFC, linewidth=2)
            
            # Set the reliability diagram
            ax1.plot([0,1], [0,1], "-", color="black", linewidth=3)
            ax1.set_title("Reliability diagram\n VRT>=" + str(VRT) + "mm/" + str(Acc) + "h, StepF=" + str(StepF) + "\n ", fontsize=18, pad=20, weight="bold")
            ax1.set_xlabel("Forecast probabilities", fontsize=16, labelpad=10)
            ax1.set_ylabel("Observation relative frequency", fontsize=16, labelpad=10)
            ax1.set_xlim([0,1])
            ax1.set_ylim([0,1])
            ax1.set_xticks(np.arange(0, 1.1, 0.5))
            ax1.set_yticks(np.arange(0, 1.1, 0.5))
            ax1.xaxis.set_tick_params(labelsize=24)
            ax1.yaxis.set_tick_params(labelsize=24)
            ax1.legend(loc="upper center", bbox_to_anchor=(0.5, 1.07), ncol=3, fontsize=16, frameon=False)

            # Set the zoomed reliability diagram
            ax2.plot([0,1], [0,1], "-", color="black", linewidth=3)
            ax2.set_title("Reliability diagram\n VRT>=" + str(VRT) + "mm/" + str(Acc) + "h, StepF=" + str(StepF) + "\n ", fontsize=18, pad=20, weight="bold")
            ax2.set_xlabel("Forecast probabilities", fontsize=16, labelpad=10)
            ax2.set_ylabel("Observation relative frequency", fontsize=16, labelpad=10)
            ax2.set_xlim([0,0.1])
            ax2.set_ylim([0,0.1])
            ax2.set_xticks(np.arange(0, 0.11, 0.01))
            ax2.set_yticks(np.arange(0, 0.11, 0.01))
            ax2.xaxis.set_tick_params(labelsize=16)
            ax2.yaxis.set_tick_params(labelsize=16)
            ax2.legend(loc="upper center", bbox_to_anchor=(0.5, 1.07), ncol=3, fontsize=16, frameon=False)
            ax2.grid()

            # Set the sharpness diagram
            ax3.set_yscale('log')
            ax3.set_title("Sharpness diagram\n VRT>=" + str(VRT) + "mm/" + str(Acc) + "h, StepF=" + str(StepF) + "\n ", fontsize=18, pad=20, weight="bold")
            ax3.set_xlabel("Forecast probabilities", fontsize=16, labelpad=10)
            ax3.set_ylabel("Forecast absolute frequency", fontsize=16, labelpad=10)
            ax3.set_xlim([0,1])
            ax3.set_ylim([0,10000000])
            ax3.set_xticks(np.arange(0, 1.1, 0.1))
            ax3.xaxis.set_tick_params(labelsize=16)
            ax3.yaxis.set_tick_params(labelsize=16)
            ax3.legend(loc="upper center", bbox_to_anchor=(0.5, 1.07), ncol=3, fontsize=16, frameon=False)
            ax3.grid()

            # Saving the reliability and sharpness diagrams
            DirOUT_temp= Git_repo + "/" + DirOUT + "/" + f"{Acc:02d}" + "h/" + str(VRT) 
            if not os.path.exists(DirOUT_temp):
                  os.makedirs(DirOUT_temp)
            FileNameOUT_Reliability = "Reliability_" + f"{Acc:02d}" + "h_" + str(VRT) + "_" + f"{StepF:02d}" + ".jpeg"
            FileNameOUT_Reliability_Zoom = "Reliability_Zoom_" + f"{Acc:02d}" + "h_" + str(VRT) + "_" + f"{StepF:02d}" + ".jpeg"
            FileNameOUT_Sharpness = "Sharpness_" + f"{Acc:02d}" + "h_" + str(VRT) + "_" + f"{StepF:02d}" + ".jpeg"
            fig1.savefig(DirOUT_temp + "/" + FileNameOUT_Reliability)
            fig2.savefig(DirOUT_temp + "/" + FileNameOUT_Reliability_Zoom)
            fig3.savefig(DirOUT_temp + "/" + FileNameOUT_Sharpness)
