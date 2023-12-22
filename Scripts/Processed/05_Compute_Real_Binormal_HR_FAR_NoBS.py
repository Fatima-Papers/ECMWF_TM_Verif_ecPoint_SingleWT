import os as os
from datetime import datetime, timedelta
import numpy as np
from scipy.stats import norm

##########################################################################################################
# CODE DESCRIPTION
# 05_Compute_Real_Binormal_HR_FAR.py computes real and binormal hit rates (HRs) and false alarm rates (FARs). 
# Code runtime: the code take up to 8 hours to run in serial.

# INPUT PARAMETERS DESCRIPTION
# DateS (date, in format YYYYMMDD): start date of the considered verification period.
# DateF (date, in format YYYYMMDD): final date of the considered verification period.
# StepF_Start (integer, in hours): first final step of the accumulation periods to consider.
# StepF_Final (integer, in hours): last final step of the accumulation periods to consider.
# Disc_Step (integer, in hours): discretization for the final steps to consider.
# Acc (integer, in hours): rainfall accumulation to consider.
# VRT_list (list of floats, from 0 to infinite, in mm): list of verifing rainfall events (VRT).
# SystemFC_list (list of strings): list of names of forecasting systems to consider.
# Git_repo (string): repository's local path.
# DirIN (string): relative path of the input directory containing the counts of FC memebers and OBS exceeding the considered VRT.
# DirOUT (string): relative path of the output directory containing the real and binormal HRs, FARs, and AROCs.

# INPUT PARAMETERS
DateS = datetime(2021, 12, 1, 0)
DateF = datetime(2022, 11, 30, 0)
StepF_Start = 12
StepF_Final = 246
Disc_Step = 6
Acc = 12
VRT_list = [0.2, 10, 25, 50]
SystemFC_list = ["ENS", "ecPoint_MultipleWT", "ecPoint_SingleWT"]
Git_repo = "/ec/vol/ecpoint_dev/mofp/Papers_2_Write/Verif_ecPoint_SingleWT"
DirIN = "Data/Compute/01_Count_EM_OBS_Exceeding_VRT"
DirOUT = "Data/Compute/05_Real_Binormal_HR_FAR_NoBS"
##########################################################################################################


# COSTUME PYTHON FUNCTIONS

#######################################################
# Computation of 'real' Hit Rates (HR) and False Alarm Rates (FAR) #
#######################################################

def real_HR_FAR(count_em, count_obs, NumEM):

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

      return hr, far
        
#######################################################################
# Computation of hit rates (HRz) and false alarm rates (FARz) with the binormal model #
#######################################################################

def binormal_HR_FAR(hr, far):
    
      # Compute the inverse of the HRs and FARs with the binormal approximation
      HRz_inv = norm.ppf(hr) # z-score for HR
      FARz_inv = norm.ppf(far) # z-score for FAR
      ind_finite = np.where(np.isfinite(FARz_inv + HRz_inv)) # index only finite values
      HRz_inv = HRz_inv[ind_finite[0]]
      FARz_inv = FARz_inv[ind_finite[0]]

      # Apply linear regression (1) to define the parameters of the binormal model.
      binormal_params = np.polyfit(FARz_inv,HRz_inv,1) 
      
      # Compute the HRs and FARs with the binormal approximation
      x = np.arange(-10,10,0.1) # sample the z-space
      predict = np.poly1d(binormal_params)
      y = predict(x)
      HRz = norm.cdf(y)
      FARz = norm.cdf(x)
    
      return HRz, FARz

##################################################################################################


# Computing the "real" and "binormal" HRs and FAR for a specific forecasting system
for SystemFC in SystemFC_list:
      
      # Selecting the number of ensemble members for the forecasting system
      if SystemFC == "ENS":
            NumEM = 51
      else:
            NumEM = 99

      # Computing the "real" and "binormal" HRs and FARs for a specific VRT
      for VRT in VRT_list:

            # Computing the "real" and "binormal" HRs and FARs for a specific lead time
            for StepF in range(StepF_Start, (StepF_Final+1), Disc_Step):

                  print(" - Computing and saving the 'real' and 'binormal' HRs and FARs for " + SystemFC +", VRT>=" + str(VRT) + ", StepF=" + str(StepF))

                  # Reading the daily counts of ensemble members and observations exceeding the considered verifying rainfall threshold.
                  Count_EM_original = [] # initializing the variable that will contain the counts of ensemble members exceeding the VRT for the original dates
                  Count_OBS_original = [] # initializing the variable that will contain the counts of observations exceeding the VRT for the original dates
                  TheDate = DateS
                  while TheDate <= DateF:
                        DirIN_temp = Git_repo + "/" + DirIN + "/" + f"{Acc:02d}" + "h/" + SystemFC + "/" + "_" + str(VRT) + "/" + TheDate.strftime("%Y%m%d%H")
                        FileNameIN_temp = "Count_EM_OBS_" + f"{Acc:02d}" + "h_" + SystemFC + "_" + str(VRT) + "_" + TheDate.strftime("%Y%m%d") + "_" + TheDate.strftime("%H") + "_" + f"{StepF:03d}" + ".npy"
                        if os.path.isfile(DirIN_temp + "/" + FileNameIN_temp): # proceed if the files exists
                              Count_EM_OBS = np.load(DirIN_temp + "/" + FileNameIN_temp)
                              Count_EM_original.extend(Count_EM_OBS[0].tolist())
                              Count_OBS_original.extend(Count_EM_OBS[1].tolist())
                        TheDate += timedelta(days=1)
                  Count_EM_original = np.array(Count_EM_original, dtype=object)
                  Count_OBS_original = np.array(Count_OBS_original, dtype=object)

                  # Computing the "real" HRs and FARs
                  HR, FAR = real_HR_FAR(Count_EM_original, Count_OBS_original, NumEM)
                  
                  # Computing the "binormal" HRs and FARs
                  HRz, FARz = binormal_HR_FAR(HR,FAR)

                  # Saving the "real" and "binormal" HRs and FARs, and the variables that determine the good of fitness of binormal model for fitting the "real" ROC curve
                  MainDirOUT = Git_repo + "/" + DirOUT + "/" + f"{Acc:02d}" + "h" + "/" + SystemFC +  "/" + VRT_Oper + "_" + str(VRT)
                  if not os.path.exists(MainDirOUT):
                        os.makedirs(MainDirOUT)
                  
                  FileNameOUT_temp = "HR_" + f"{Acc:02d}" + "h_" + SystemFC +  "_" + VRT_Oper + "_" + str(VRT) + "_" + f"{StepF:03d}"
                  np.save(MainDirOUT + "/" +  FileNameOUT_temp, HR) 
                  FileNameOUT_temp = "FAR_" + f"{Acc:02d}" + "h_" + SystemFC + "_" + VRT_Oper + "_" + str(VRT) + "_" + f"{StepF:03d}"
                  np.save(MainDirOUT + "/" +  FileNameOUT_temp, FAR)
                  
                  FileNameOUT_temp = "HRz_" + f"{Acc:02d}" + "h_" + SystemFC + "_" + VRT_Oper + "_" + str(VRT) + "_" + f"{StepF:03d}"
                  np.save(MainDirOUT + "/" +  FileNameOUT_temp, HRz) 
                  FileNameOUT_temp = "FARz_" + f"{Acc:02d}" + "h_" + SystemFC + "_" + VRT_Oper + "_" + str(VRT) + "_" + f"{StepF:03d}"
                  np.save(MainDirOUT + "/" +  FileNameOUT_temp, FARz)                 