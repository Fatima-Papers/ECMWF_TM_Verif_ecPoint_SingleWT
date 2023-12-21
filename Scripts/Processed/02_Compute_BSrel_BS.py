import os
import sys
from datetime import datetime, timedelta
from random import choices
import itertools
import numpy as np

########################################################################################
# CODE DESCRIPTION
# 02_Compute_BSrel.py computes the values of the Brier Score - Reliability component (BSrel), including 
# bootstrapped (BS) values.
# Code Runtime: the script can take up 10 days to run in serial. It is recommended to run the code in parallel  
# for different forecasting systems and VRT values to bring down the runtime to 1 day.

# INPUT PARAMETERS DESCRIPTION
# DateS (date, in format YYYYMMDD): start date of the considered verification period.
# DateF (date, in format YYYYMMDD): final date of the considered verification period.
# StepF_Start (integer, in hours): first final step of the accumulation periods to consider.
# StepF_Final (integer, in hours): last final step of the accumulation periods to consider.
# Disc_Step (integer, in hours): discretization for the final steps to consider.
# Acc (number, in hours): rainfall accumulation to consider.
# RepetitionsBS (integer, from 0 to infinite): number of repetitions to consider in the bootstrapping.
# VRT_list (list of floats, from 0 to infinite, in mm): list of verifing rainfall events (VRT).
# SystemFC_list (list of strings): list of names of forecasting systems to consider.
# Git_repo (string): repository's local path.
# DirIN (string): relative path containing the counts of EM and OBS exceeding a certain VRT.
# DirOUT (string): relative path of the directory containing the BSrel values, including the bootstrapped ones.

# INPUT PARAMETERS
DateS = datetime(2021, 12, 1, 0)
DateF = datetime(2022, 11, 30, 0)
StepF_Start = 12
StepF_Final = 246
Disc_Step = 6
Acc = 12
RepetitionsBS = 1000
VRT_list = sys.argv[1]
SystemFC_list = sys.argv[2]
Git_repo = "/ec/vol/ecpoint_dev/mofp/Papers_2_Write/Verif_ecPoint_SingleWT"
DirIN = "Data/Compute/01_Count_EM_OBS_Exceeding_VRT"
DirOUT = "Data/Compute/02_BSrel_BS"
########################################################################################


# COSTUME FUNCTIONS

#####################################
# Brier Score - Reliability component (BSrel) #
#####################################

# Note: To compute the BSrel values, we are using the equation present in:
# Ferro, C.A. and Fricker, T.E., 2012. A bias‐corrected decomposition of the Brier score. Quarterly Journal of the Royal Meteorological Society, 138(668), pp.1954-1960. https://doi.org/10.1002/qj.1924
def BSrel_Ferro(count_em, count_obs, NumEM):

      n = len(count_em) # sample size
      Count_EM = np.arange(0, NumEM+1) # possible counts of ensemble members exceeding the VRT (i.e. from 0 to NumEM)
      Prob_Thr = Count_EM/NumEM  # probability thresholds offered by the considered ensemble

      Nk = np.array([len(count_em[count_em == Count_EM_k]) for Count_EM_k in Count_EM])
      Ok = np.array([sum(count_obs[count_em == Count_EM_k]) for Count_EM_k in Count_EM])
      
      Ok = Ok[Nk != 0]
      Prob_Thr = Prob_Thr[Nk != 0]
      Nk = Nk[Nk != 0]
      
      BSrel = np.sum((Nk/n) * ((Prob_Thr - (Ok/Nk))**2))

      return BSrel

####################################################################################################


# Reading the external input variables
VRT_list_temp = []
VRT_list = VRT_list.split(',')
for elem in VRT_list:
      if float(elem) < 1:
            VRT_list_temp.append(float(elem))
      else:
            VRT_list_temp.append(int(elem))
VRT_list = VRT_list_temp
SystemFC_list  = SystemFC_list.split(',')

# Defining the list of StepF to consider
StepF_list = range(StepF_Start, (StepF_Final+1), Disc_Step)
m = len(StepF_list)

# Computing BSrel for a specific forecasting system
for indSystemFC in range(len(SystemFC_list)):

      # Selecting the forecasting system to consider and its number of ensemble members
      SystemFC = SystemFC_list[indSystemFC]
      
      # Defining the n. of ensemble members for the forecasting system
      if SystemFC == "ENS":
            NumEM = 51
      else:
            NumEM = 99

      # Computing BSrel for a specific VRT
      for VRT in VRT_list:

            # Initializing the variable containing the BSrel values, and the bootstrapped ones
            BSrel_array = np.zeros([m, RepetitionsBS+2])

            # Computing BSrel for a specific lead time
            for ind_StepF in range(m):

                  StepF = StepF_list[ind_StepF]
                  print("Computing and saving BSrel for " + SystemFC +", VRT>=" + str(VRT) + ", StepF=" + str(StepF))

                  # Storing information about the step computed
                  BSrel_array[ind_StepF, 0] = StepF

                  # Reading the daily counts of ensemble members and observations exceeding the considered verifying rainfall event
                  original_datesSTR_array = [] # list of dates for which the counts are created (not all steps might have one if the forecasts did not exist)
                  Count_EM_original = [] # initializing the variable that will contain the counts of ensemble members exceeding the VRT for the original dates
                  Count_OBS_original = [] # initializing the variable that will contain the counts of observations exceeding the VRT for the original dates
                  TheDate = DateS
                  while TheDate <= DateF:
                        DirIN_temp = Git_repo + "/" + DirIN + "/" + f"{Acc:02d}" + "h/" + SystemFC + "/" + str(VRT) + "/" + TheDate.strftime("%Y%m%d%H")
                        FileNameIN_temp = "Count_EM_OBS_" + f"{Acc:02d}" + "h_" + SystemFC + "_" + str(VRT) + "_" + TheDate.strftime("%Y%m%d") + "_" + TheDate.strftime("%H") + "_" + f"{StepF:03d}" + ".npy"
                        if os.path.isfile(DirIN_temp + "/" + FileNameIN_temp): # proceed if the files exists
                              original_datesSTR_array.append(TheDate.strftime("%Y%m%d"))
                              Count_EM_OBS = np.load(DirIN_temp + "/" + FileNameIN_temp)
                              Count_EM_original.append(Count_EM_OBS[0].tolist())
                              Count_OBS_original.append(Count_EM_OBS[1].tolist())
                        TheDate += timedelta(days=1)
                  Count_EM_original = np.array(Count_EM_original, dtype=object)
                  Count_OBS_original = np.array(Count_OBS_original, dtype=object)

                  # Computing BSrel for the original and the bootstrapped values
                  for ind_repBS in range(RepetitionsBS+1):
                        
                        # Selecting whether to compute BSrel, AROCt, and AROCz for original or the bootstrapped values
                        if ind_repBS == 0:  # original
                              Count_EM = Count_EM_original
                              Count_OBS = Count_OBS_original
                        else:  # bootstrapped
                              NumDays = len(original_datesSTR_array)
                              datesBS_array = np.array(choices(population=original_datesSTR_array, k=NumDays)) # list of bootstrapped dates
                              indBS = np.searchsorted(original_datesSTR_array, datesBS_array) # indexes of the bootstrapped dates
                              Count_EM = Count_EM_original[indBS] # indexing the bootstrapped counts
                              Count_OBS = Count_OBS_original[indBS] # indexing the bootstrapped counts

                        # Expand the list of lists into a unique array
                        Count_EM = np.array(list(itertools.chain.from_iterable(Count_EM.tolist())))
                        Count_OBS = np.array(list(itertools.chain.from_iterable(Count_OBS.tolist())))
                        
                        # Computing BSrel
                        BSrel = BSrel_Ferro(Count_EM, Count_OBS, NumEM)
                        BSrel_array[ind_StepF, ind_repBS+1] = BSrel

            # Saving BSrel
            DirOUT_temp = Git_repo + "/" + DirOUT + "/" + f"{Acc:02d}" + "h/BSrel/"
            FileNameOUT_temp = "BSrel_" + f"{Acc:02d}" + "h_" + SystemFC + "_" + str(VRT)
            if not os.path.exists(DirOUT_temp):
                  os.makedirs(DirOUT_temp)
            np.save(DirOUT_temp + "/" + FileNameOUT_temp, BSrel_array)