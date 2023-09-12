import os
from datetime import datetime, timedelta
from random import choices
import itertools
import numpy as np
from scipy.stats import norm

###############################################################################################
# CODE DESCRIPTION
# 06_Compute_BSrel_Real_Binormal_AROC_Bootstrapping.py computes the values for the Brier Score - Reliability 
# component (BSrel) and the "real" and "binormal" Area Under the ROC curves (AROC and AROCz), including  
# bootstrapped values.
# Code Runtime: the script can take up 30 days to run in serial. It is recommended to run the code in parallel for 
# different forecasting systems and VRE values to bring down the runtime to 4-5 days. 

# INPUT PARAMETERS DESCRIPTION
# DateS (date, in format YYYYMMDD): start date of the considered verification period.
# DateF (date, in format YYYYMMDD): final date of the considered verification period.
# StepF_Start (integer, in hours): first final step of the accumulation periods to consider.
# StepF_Final (integer, in hours): last final step of the accumulation periods to consider.
# Disc_Step (integer, in hours): discretization for the final steps to consider.
# Acc (number, in hours): rainfall accumulation to consider.
# RepetitionsBS (integer, from 0 to infinite): number of repetitions to consider in the bootstrapping.
# VRE_list (list of floats, from 0 to infinite, in mm): list of verifing rainfall events (VRE).
# SystemFC_list (list of strings): list of names of forecasting systems to consider.
# NumEM_list (list of integers): numer of ensemble members in the considered forecasting systems.
# Git_repo (string): repository's local path.
# DirIN (string): relative path containing the counts of EM and OBS exceeding a certain VRE.
# DirOUT_BSrel (string): relative path of the directory containing the BSrel values, including the bootstrapped ones.
# DirOUT_AROC (string): relative path of the directory containing the AROC values, including the bootstrapped ones.

# INPUT PARAMETERS
DateS = datetime(2021, 12, 1, 0)
DateF = datetime(2022, 11, 30, 0)
StepF_Start = 12
StepF_Final = 246
Disc_Step = 6
Acc = 12
RepetitionsBS = 1000
VRE_list = [0.2,10,25,50]
SystemFC_list = ["ENS", "ecpoint_MultipleWT", "ecPoint_SingleWT"]
NumEM_list = [51, 99, 99]
Git_repo = "/ec/vol/ecpoint_dev/mofp/Papers_2_Write/Verif_ecPoint_SingleWT"
DirIN = "Data/Compute/01_Count_EM_OBS_Exceeding_VRE"
DirOUT_BSrel = "Data/Compute/06_BSrel_Bootstrapping"
DirOUT_AROC = "Data/Compute/06_AROC_Bootstrapping"
DirOUT_AROCz = "Data/Compute/06_AROCz_Bootstrapping"
###############################################################################################


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


#####################################
# "Real" Area Under the ROC curve (AROC)   #
#####################################

# Note: the computation of AROC values uses the trapezoidal approximation
def AROC_trapezoidal(count_em, count_obs, NumEM):

      # Computing the probabilistic contingency table
      ct = np.empty([NumEM+1, 4])
      for index in range(NumEM+1):
            count_members = NumEM - index
            OBS_yes_fc = count_obs[np.where(count_em >= count_members)[0]] # observation instances for "yes" forecasts
            OBS_no_fc = count_obs[np.where(count_em < count_members)[0]] # observation instances for "no" forecasts
            ct[index][0] = np.where(OBS_yes_fc > 0)[0].shape[0]  # hits
            ct[index][1] = np.where(OBS_yes_fc == 0)[0].shape[0]  # false alarms
            ct[index][2] = np.where(OBS_no_fc > 0)[0].shape[0]  # misses
            ct[index][3] = np.where(OBS_no_fc == 0)[0].shape[0]  # correct negatives
      ct = ct.astype(int)  # setting all values as integers

      # Computing hit rates (hr) and false alarm rates (far).
      hr = ct[:, 0] / (ct[:, 0] + ct[:, 2])  # hit rates
      far = ct[:, 1] / (ct[:, 1] + ct[:, 3])  # false alarms

      # Adding the points (0,0) and (1,1) to the arrays to ensure the ROC curve is closed.
      hr = np.insert(hr, 0, 0)
      hr = np.insert(hr, -1, 1)
      far = np.insert(far, 0, 0)
      far = np.insert(far, -1, 1)

      # Computing AROC with the trapezoidal approximation, and approximating its value to the second decimal digit.
      aroc = 0
      for i in range(len(hr)-1):
            j = i+1
            a = hr[i]
            b = hr[i+1]
            h = far[i+1] - far[i]
            aroc = aroc + (((a+b)*h) / 2)
      aroc = round(aroc, 2)

      return hr, far, aroc


##########################################
# "Binormal" Area Under the ROC curve (AROCz)   #
##########################################

def binormal_AROC(hr,far):
    
      # Compute the inverse of the HRs and FARs with the binormal approximation
      HRz_inv = norm.ppf(hr) # z-score for HR
      FARz_inv = norm.ppf(far) # z-score for FAR
      ind_finite = np.where(np.isfinite(FARz_inv + HRz_inv)) # index only finite values
      HRz_inv = HRz_inv[ind_finite[0]]
      FARz_inv = FARz_inv[ind_finite[0]]

      # Apply linear regression (1) to define the parameters of the binormal model.
      binormal_params = np.polyfit(FARz_inv,HRz_inv,1) 
      
      # Computing AROCz
      AROCz = norm.cdf( (binormal_params[1]*( (binormal_params[0]**2+1.)/2.)**(-0.5) )/(2.**(0.5)))
    
      return AROCz 


####################################################################################################


print(" ")
print("Computing BSrel, AROC and AROCz, including " + str(RepetitionsBS) + " bootstrapped values")

# Computing the totals number of days contained in the considered verification period
NumTotDays = (DateF-DateS).days + 1

# Creating the list containing the steps to considered in the computations
StepF_list = range(StepF_Start, (StepF_Final+1), Disc_Step)

# Computing the variables that will define the size for the BSrel, AROC, and AROCz variables
m = len(StepF_list)
n = len(range(RepetitionsBS + 1))

# Computing BSrel, AROC, and AROCz for a specific forecasting system
for indSystemFC in range(len(SystemFC_list)):

      # Selecting the forecasting system to consider and its number of ensemble members
      SystemFC = SystemFC_list[indSystemFC]
      NumEM = NumEM_list[indSystemFC]

      # Computing BSrel, AROC, and AROCz for a specific vre
      for vre in VRE_list:

            # Initializing the variable containing the BSrel, AROC, and AROCz values, and the bootstrapped ones
            BSrel_array = np.zeros([m, n+1])
            AROC_array = np.zeros([m, n+1])
            AROCz_array = np.zeros([m, n+1])

            # Computing BSrel, AROC, and AROCz for a specific lead time
            for indStepF in range(len(StepF_list)):

                  # Selecting the StepF to consider
                  StepF = StepF_list[indStepF]
                  print(" - Computing BSrel, AROC, and AROCz for " + SystemFC +", VRE>=" + str(vre) + ", StepF=" + str(StepF))

                  # Storing information about the step computed
                  BSrel_array[indStepF, 0] = StepF
                  AROC_array[indStepF, 0] = StepF
                  AROCz_array[indStepF, 0] = StepF

                  # Reading the daily counts of ensemble members and observations exceeding the considered verifying rainfall event.
                  original_datesSTR_array = [] # list of dates for which the counts are created (not all steps might have one if the forecasts did not exist)
                  Count_EM_original = [] # initializing the variable that will contain the counts of ensemble members exceeding the VRE for the original dates
                  Count_OBS_original = [] # initializing the variable that will contain the counts of observations exceeding the VRE for the original dates
                  TheDate = DateS
                  while TheDate <= DateF:
                        DirIN_temp = Git_repo + "/" + DirIN + "/" + f"{Acc:02d}" + "h/" + SystemFC + "/" + str(vre) + "/" + TheDate.strftime("%Y%m%d%H")
                        FileNameIN_temp = "Count_EM_OBS_" + f"{Acc:02d}" + "h_" + SystemFC + "_" + str(vre) + "_" + TheDate.strftime("%Y%m%d") + "_" + TheDate.strftime("%H") + "_" + f"{StepF:03d}" + ".npy"
                        if os.path.isfile(DirIN_temp + "/" + FileNameIN_temp): # proceed if the files exists
                              original_datesSTR_array.append(TheDate.strftime("%Y%m%d"))
                              Count_EM_OBS = np.load(DirIN_temp + "/" + FileNameIN_temp)
                              Count_EM_original.append(Count_EM_OBS[0].tolist())
                              Count_OBS_original.append(Count_EM_OBS[1].tolist())
                        TheDate += timedelta(days=1)
                  Count_EM_original = np.array(Count_EM_original, dtype=object)
                  Count_OBS_original = np.array(Count_OBS_original, dtype=object)

                  # Computing BSrel, AROC, and AROCz for the original and the bootstrapped values
                  for ind_repBS in range(RepetitionsBS+1):
                        
                        # Selecting whether to compute BSrel, AROC, and AROCz for original or the bootstrapped values
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
                        BSrel_array[indStepF, ind_repBS+1] = BSrel

                        # Computing AROC
                        HR, FAR, AROC = AROC_trapezoidal(Count_EM, Count_OBS, NumEM)
                        AROC_array[indStepF, ind_repBS+1] = AROC

                        # Computing AROCz
                        AROCz = binormal_AROC(HR, FAR)
                        AROCz_array[indStepF, ind_repBS+1] = AROCz

            # Saving BSrel
            print("      - Saving BSrel for " + SystemFC + ", VRE>=" + str(vre))
            DirOUT_temp = Git_repo + "/" + DirOUT_BSrel + "/" + f"{Acc:02d}" + "h"
            FileNameOUT_temp = "BSrel_" + f"{Acc:02d}" + "h_" + SystemFC + "_" + str(vre)
            if not os.path.exists(DirOUT_temp):
                  os.makedirs(DirOUT_temp)
            np.save(DirOUT_temp + "/" + FileNameOUT_temp, BSrel_array)

            # Saving AROC
            print("      - Saving AROC for " + SystemFC + ", VRE>=" + str(vre))
            DirOUT_temp = Git_repo + "/" + DirOUT_AROC + "/" + f"{Acc:02d}" + "h"
            FileNameOUT_temp = "AROC_" + f"{Acc:02d}" + "h_" + SystemFC + "_" + str(vre)
            if not os.path.exists(DirOUT_temp):
                  os.makedirs(DirOUT_temp)
            np.save(DirOUT_temp + "/" + FileNameOUT_temp, AROC_array)

            # Saving AROCz
            print("      - Saving AROCz for " + SystemFC + ", VRE>=" + str(vre))
            DirOUT_temp = Git_repo + "/" + DirOUT_AROCz + "/" + f"{Acc:02d}" + "h"
            FileNameOUT_temp = "AROCz_" + f"{Acc:02d}" + "h_" + SystemFC + "_" + str(vre)
            if not os.path.exists(DirOUT_temp):
                  os.makedirs(DirOUT_temp)
            np.save(DirOUT_temp + "/" + FileNameOUT_temp, AROCz_array)