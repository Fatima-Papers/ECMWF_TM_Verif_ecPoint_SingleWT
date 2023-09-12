import os as os
from datetime import datetime, timedelta
import itertools
import numpy as np
from scipy.stats import norm
from sklearn.metrics import r2_score

##########################################################################################################
# CODE DESCRIPTION
# 02_Compute_Real_Binormal_HR_FAR_AROC_NoBS.py computes real and binormal HRs, FARs, and AROCs. 
# Code runtime: the code take up to 90 minutes to run in serial.

# INPUT PARAMETERS DESCRIPTION
# DateS (date, in format YYYYMMDD): start date of the considered verification period.
# DateF (date, in format YYYYMMDD): final date of the considered verification period.
# StepF_Start (integer, in hours): first final step of the accumulation periods to consider.
# StepF_Final (integer, in hours): last final step of the accumulation periods to consider.
# Disc_Step (integer, in hours): discretization for the final steps to consider.
# Acc (integer, in hours): rainfall accumulation to consider.
# VRE_list (list of floats, from 0 to infinite, in mm): list of verifing rainfall events (VRE).
# SystemFC_list (list of strings): list of names of forecasting systems to consider.
# NumEM_list (list of integers): list of the number of ensemble members in each forecasting system.
# Git_repo (string): repository's local path.
# DirIN (string): relative path of the input directory containing the counts of FC memebers and OBS exceeding the considered VRE.
# DirOUT (string): relative path of the output directory containing the real and binormal HRs, FARs, and AROCs.

# INPUT PARAMETERS
DateS = datetime(2021, 12, 1, 0)
DateF = datetime(2022, 11, 30, 0)
StepF_Start = 12
StepF_Final = 246
Disc_Step = 6
Acc = 12
VRE_list = [0.2, 10, 25, 50]
SystemFC_list = ["ENS", "ecPoint_MultipleWT", "ecPoint_SingleWT"]
NumEM_list = [51, 99, 99]
Git_repo = "/ec/vol/ecpoint_dev/mofp/Papers_2_Write/ECMWF_TM_Verif_ecPoint_SingleWT"
DirIN = "Data/Compute/01_Count_EM_OBS_Exceeding_VRE"
DirOUT = "Data/Compute/02_Real_Binormal_HR_FAR_AROC_NoBS"
##########################################################################################################


# COSTUME PYTHON FUNCTIONS

#####################################################################################
# Computation of 'real' Hit Rates (HR), False Alarm Rates (FAR), and Areas under the ROC curve (AROC) #
#####################################################################################

def HR_FAR_AROC(count_em, count_obs, NumEM):

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

      # Computing the AROC with the trapezoidal approximation, and approximating its value to the second decimal digit.
      aroc = 0
      for i in range(len(hr)-1):
            j = i+1
            a = hr[i]
            b = hr[i+1]
            h = far[i+1] - far[i]
            aroc = aroc + (((a+b)*h) / 2)
      aroc = round(aroc, 2)

      return hr, far, aroc
        
#######################################################################
# Computation of hit rates (HRz) and false alarm rates (FARz) with the binormal model #
#######################################################################

def binormal_HR_FAR(hr,far):
    
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

      # Test the goodness of fit of binormal model for fitting the "real" ROC curve
      x_LR = FARz_inv
      y_LR = predict(x_LR)
      r2 = r2_score(HRz_inv,y_LR)
    
      AROCz = norm.cdf( (binormal_params[1]*( (binormal_params[0]**2+1.)/2.)**(-0.5) )/(2.**(0.5)))
    
      return HRz_inv, FARz_inv, x_LR, y_LR, r2, HRz, FARz, AROCz 

##################################################################################################

# Setting the output directory
MainDirOUT = Git_repo + "/" + DirOUT + "/" + f"{Acc:02d}" + "h"
if not os.path.exists(MainDirOUT):
      os.makedirs(MainDirOUT)

# Creating the list containing the considered steps
StepF_list = range(StepF_Start, (StepF_Final+1), Disc_Step)
m = len(StepF_list)

# Computing the "real" and "binormal" HRs, FAR, and AROCs for a specific forecasting system
for indSystemFC in range(len(SystemFC_list)):
      
      # Selecting the forecasting system to consider, and the number of ensemble members
      SystemFC = SystemFC_list[indSystemFC]
      NumEM = NumEM_list[indSystemFC]

      # Computing the "real" and "binormal" HRs, FAR, and AROCs for a specific vre
      for vre in VRE_list:

            # Initializing the variable containing the "real" and "binormal" HRs, FAR, and AROCs
            AROC_array = np.zeros([m,2])
            AROCz_array = np.zeros([m,2])

            # Computing the "real" and "binormal" HRs, FAR, and AROCs for a specific lead time
            for indStepF in range(len(StepF_list)):

                  # Selecting the StepF to consider
                  StepF = StepF_list[indStepF]
                  
                  # Storing information about the considered step
                  AROC_array[indStepF, 0] = StepF
                  AROCz_array[indStepF, 0] = StepF

                  print(" - Computing and saving the 'real' and 'binormal' HR, FAR, and AROC for " + SystemFC +", VRE>=" + str(vre) + ", StepF=" + str(StepF))

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
                  
                  # Computing the "real" HR, FAR, and AROC
                  HR, FAR, AROC = HR_FAR_AROC(Count_EM_original, Count_OBS_original, NumEM)
                  AROC_array[indStepF,1] = AROC
                  
                  # Computing the "binormal" HR, FAR, and AROC
                  _, _, _, _, _, HRz, FARz, AROCz  = binormal_HR_FAR(HR,FAR)
                  AROCz_array[indStepF,1] = AROCz

                  # Saving the "real" and "binormal" HRs and FARs
                  FileNameOUT_temp = "HR_" + f"{Acc:02d}" + "h_" + SystemFC + "_" + str(vre) + "_" + f"{StepF:03d}"
                  np.save(MainDirOUT + "/" +  FileNameOUT_temp, HR) 
                  FileNameOUT_temp = "FAR_" + f"{Acc:02d}" + "h_" + SystemFC + "_" + str(vre) + "_" + f"{StepF:03d}"
                  np.save(MainDirOUT + "/" +  FileNameOUT_temp, FAR)
                  FileNameOUT_temp = "HRz_" + f"{Acc:02d}" + "h_" + SystemFC + "_" + str(vre) + "_" + f"{StepF:03d}"
                  np.save(MainDirOUT + "/" +  FileNameOUT_temp, HRz) 
                  FileNameOUT_temp = "FARz_" + f"{Acc:02d}" + "h_" + SystemFC + "_" + str(vre) + "_" + f"{StepF:03d}"
                  np.save(MainDirOUT + "/" +  FileNameOUT_temp, FARz)

            # Saving the "real" and "binormal" AROCs
            FileNameOUT_temp = "AROC_" + f"{Acc:02d}" + "h_" + SystemFC + "_" + str(vre)
            np.save(MainDirOUT + "/" +  FileNameOUT_temp, AROC_array)
            FileNameOUT_temp = "AROCz_" + f"{Acc:02d}" + "h_" + SystemFC + "_" + str(vre)
            np.save(MainDirOUT + "/" +  FileNameOUT_temp, AROCz_array) 