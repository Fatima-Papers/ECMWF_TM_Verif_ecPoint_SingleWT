import os
from datetime import datetime, timedelta
import matplotlib.pyplot as plt
import itertools
import numpy as np

###################################################################################################
# CODE DESCRIPTION
# 05_Plot_BSrel_NoBS.py plots the Brier Score (Reliability) with no confidence intervals.
# Code runtime: the script takes up to 1 hour to run in serial.

# INPUT PARAMETERS DESCRIPTION
# DateS (date, in format YYYYMMDD): start date of the considered verification period.
# DateF (date, in format YYYYMMDD): final date of the considered verification period.
# StepF_Start (integer, in hours): first final step of the accumulation periods to consider.
# StepF_Final (integer, in hours): last final step of the accumulation periods to consider.
# Disc_Step (integer, in hours): discretization for the final steps to consider.
# Acc (number, in hours): rainfall accumulation to consider.
# VRE_list (list of floats, from 0 to infinite, in mm): list of verifing rainfall events (VRE).
# SystemFC_list (list of strings): list of names of forecasting systems to consider.
# NumEM_list (list of integers): numer of ensemble members in the considered forecasting systems.
# Colour_SystemFC_list (list of strings): list of colours to assign to each forecasting system.
# Git_repo (string): repository's local path.
# DirIN (string): relative path of the input directory  containing the counts of FC members and OBS exceeding a certain VRE.
# DirOUT (string): relative path of the output directory containing the BSrel plots.

# INPUT PARAMETERS
DateS = datetime(2021, 12, 1, 0)
DateF = datetime(2022, 11, 30, 0)
StepF_Start = 12
StepF_Final = 246
Disc_Step = 6
Acc = 12
VRE_list = [0.2,10,25,50]
SystemFC_list = ["ENS", "ecPoint_MultipleWT", "ecPoint_SingleWT"]
NumEM_list = [51, 99, 99]
Colour_SystemFC_list = ["darkcyan", "darkorange", "grey"]
Git_repo = "/ec/vol/ecpoint_dev/mofp/Papers_2_Write/ECMWF_TM_Verif_ecPoint_SingleWT"
DirIN = "Data/Compute/01_Count_EM_OBS_Exceeding_VRE"
DirOUT = "Data/Plot/05_BSrel_NoBS"
###################################################################################################


# COSTUME FUNCTIONS

#####################################
# Brier Score - Reliability component (BSrel) #
#####################################

# Note: To compute the BSrel values, we are using the equation present in:
# Ferro, C.A. and Fricker, T.E., 2012. A bias‐corrected decomposition of the Brier score.
# Quarterly Journal of the Royal Meteorological Society, 138(668), pp.1954-1960.
# https://doi.org/10.1002/qj.1924
def BSrel_Ferro(count_em, count_obs, NumEM):

      n = len(count_em) # sample size
      Count_EM = np.arange(0, NumEM+1) # possible counts of ensemble members exceeding the VRE (i.e. from 0 to NumEM)
      Prob_Thr = Count_EM/NumEM  # probability thresholds offered by the considered ensemble

      BSrel = 0  # initializing the variable containing the BSrel value
      for indCount in Count_EM:
            Count_EM_k = Count_EM[indCount]  # kth possible ensemble member count
            Prob_Thr_k = Prob_Thr[indCount] # probability threshold associated to the kth ensemble member count
            Nk = len(count_em[count_em == Count_EM_k]) # number of times the kth forecast count was issued
            Ok = sum(count_obs[count_em == Count_EM_k]) # number of events that occurred when the kth forecast count was issued
            if Nk > 0:  # to avoid diving by zero
                  BSrel = BSrel + ((Nk/n) * (((Ok/Nk) - Prob_Thr_k)**2))

      return BSrel

###########################################################################################################


# Setting the output directory
MainDirOUT = Git_repo + "/" + DirOUT + "/" + f"{Acc:02d}" + "h"
if not os.path.exists(MainDirOUT):
      os.makedirs(MainDirOUT)

# Creating the list containing the considered steps
StepF_list = range(StepF_Start, (StepF_Final+1), Disc_Step)
m = len(StepF_list)

# Computing the BSrel for a specific vre
for vre in VRE_list:

      # Initializing the variable containing the BSrel
      BSrel_array = np.zeros([m,2])

      # Initialize the figure to plot BSrel
      plt.figure(figsize=(17,13))

      # Computing the BSrel for a specific forecasting system
      for indSystemFC in range(len(SystemFC_list)):
            
            # Selecting the forecasting system to consider, the number of its ensemble members, and the colour to assign in the plot to the forecasting system
            SystemFC = SystemFC_list[indSystemFC]
            NumEM = NumEM_list[indSystemFC]
            Colour_SystemFC = Colour_SystemFC_list[indSystemFC]
            
            # Computing the BSrel for a specific lead time
            for indStepF in range(len(StepF_list)):

                  # Selecting the StepF to consider
                  StepF = StepF_list[indStepF]
                  
                  # Storing information about the considered step
                  BSrel_array[indStepF, 0] = StepF
            
                  print(" - Computing the BSrel for " + SystemFC +", VRE>=" + str(vre) + "mm/" + str(Acc) + "h, StepF=" + str(StepF))

                  # Reading the daily counts of ensemble members and observations exceeding the considered verifying rainfall event.
                  Count_EM_original = [] # initializing the variable that will contain the counts of ensemble members exceeding the VRE for the original dates
                  Count_OBS_original = [] # initializing the variable that will contain the counts of observations exceeding the VRE for the original dates
                  TheDate = DateS
                  while TheDate <= DateF:
                        DirIN_temp = Git_repo + "/" + DirIN + "/" + f"{Acc:02d}" + "h/" + SystemFC + "/" + str(vre) + "/" + TheDate.strftime("%Y%m%d%H")
                        FileNameIN_temp = "Count_EM_OBS_" + f"{Acc:02d}" + "h_" + SystemFC + "_" + str(vre) + "_" + TheDate.strftime("%Y%m%d") + "_" + TheDate.strftime("%H") + "_" + f"{StepF:03d}" + ".npy"
                        if os.path.isfile(DirIN_temp + "/" + FileNameIN_temp): # proceed if the files exists
                              Count_EM_OBS = np.load(DirIN_temp + "/" + FileNameIN_temp)
                              Count_EM_original.append(Count_EM_OBS[0].tolist())
                              Count_OBS_original.append(Count_EM_OBS[1].tolist())
                        TheDate += timedelta(days=1)
                  Count_EM_original = np.array(Count_EM_original, dtype=object)
                  Count_OBS_original = np.array(Count_OBS_original, dtype=object)

                  # Expand the list of lists into a unique array
                  Count_EM_original = np.array(list(itertools.chain.from_iterable(Count_EM_original.tolist())))
                  Count_OBS_original = np.array(list(itertools.chain.from_iterable(Count_OBS_original.tolist())))

                  # Computing BSrel
                  BSrel = BSrel_Ferro(Count_EM_original, Count_OBS_original, NumEM)
                  BSrel_array[indStepF, 1] = BSrel

            # Plotting BSrel
            plt.plot(BSrel_array[:,0], BSrel_array[:,1], "-o", color=Colour_SystemFC, label=SystemFC)
            
      # Complete the BSrel plot
      plt.title("Brier Score - Reliability Component (BSrel)\n VRE >= " + str(vre) + " mm/" + str(Acc) + "h\n", fontsize = 24, pad=20, weight="bold")
      plt.xlabel(" \n Steps at the end of the " + str(Acc) + "-hourly accumulation period [hours]", fontsize = 16, labelpad=20)
      plt.ylabel("BSrel [-] \n ", fontsize = 16, labelpad=10)
      plt.xlim((StepF_Start-1,StepF_Final+1))
      plt.xticks(BSrel_array[:,0], fontsize = 16, rotation = 90)
      plt.yticks(fontsize = 16)
      plt.legend(loc="upper center", bbox_to_anchor=(0.5, 1.05), ncol=3, fontsize=16, frameon=False) 
      plt.grid()

      # Saving the BSrel plot
      print(" - Saving the BSrel plot")
      FileNameOUT_temp = "BSrel_NoBS_" + f"{Acc:02d}" + "h_"+ str(vre) + ".jpeg"
      plt.savefig(MainDirOUT + "/" + FileNameOUT_temp)
      plt.close()