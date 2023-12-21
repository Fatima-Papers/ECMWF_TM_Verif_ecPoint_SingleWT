import os
import sys
from datetime import datetime, timedelta
import numpy as np
import metview as mv 

########################################################################################
# CODE DESCRIPTION
# 01_Compute_Count_EM_OBS_Exceeding_VRT.py computes the count of ensemble members and 
# observations exceeding the considered verifying rainfall threshold. 
# Code runtime: the script can take up to 3 days to run in serial. It is recommended to run separate months 
# in parallel to take down the runtime to 6 hours. 

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
# DirIN_FC (string): relative path of the directory containing the rainfall forecasts.
# DirIN_OBS (string): relative path containing the rainfall observations.
# DirOUT (string): relative path of the directory containing the counts.

# INPUT PARAMETERS
DateS = sys.argv[1]
DateF = sys.argv[2]
StepF_Start = 12
StepF_Final = 246
Disc_Step = 6
Acc = 12
VRT_list = [0.2, 10, 50]
SystemFC_list = ["ENS", "ecPoint_SingleWT", "ecPoint_SingleWT"]
Git_repo="/ec/vol/ecpoint_dev/mofp/Papers_2_Write/Verif_ecPoint_SingleWT"
DirIN_FC = "Data/Raw/FC"
DirIN_OBS = "Data/Raw/OBS"
DirOUT = "Data/Compute/01_Count_EM_OBS_Exceeding_VRT"
########################################################################################

# Converting the strings into datetime objects
DateS = datetime.strptime(DateS, "%Y%m%d")
DateF = datetime.strptime(DateF, "%Y%m%d")

# Computing the counts for a specific forecasting system
for SystemFC in SystemFC_list:

      # Computing the counts for a specific date
      TheDate = DateS
      while TheDate <= DateF:

            # Computing the counts for a specific lead time
            for StepF in range(StepF_Start, (StepF_Final+1), Disc_Step):
                  
                  # Computing the beginning of the accumulation period
                  StepS = StepF - Acc
                  
                  print("Computing the counts for " + SystemFC + ", FC: " + TheDate.strftime("%Y-%m-%d") + " at " + TheDate.strftime("%H") + " UTC, (t+" + str(StepS) + ",t+", str(StepF) + ")")
                  
                  # Reading the rainfall forecasts
                  tp = [] # variable needed to asses whether the forecasts for the considered date exist
                  if SystemFC == "ENS": # Note: converting the forecasts in accumulated rainfall over the considered period. Converting also their units from m to mm.
                        FileIN_FC_temp1= Git_repo + "/" + DirIN_FC + "/" + SystemFC + "/" + TheDate.strftime("%Y%m%d%H") + "/tp_" + TheDate.strftime("%Y%m%d") + "_" + TheDate.strftime("%H") + "_" + f"{StepS:03d}" + ".grib"
                        FileIN_FC_temp2= Git_repo + "/" + DirIN_FC + "/" + SystemFC + "/" + TheDate.strftime("%Y%m%d%H") + "/tp_" + TheDate.strftime("%Y%m%d") + "_" + TheDate.strftime("%H") + "_" + f"{StepF:03d}" + ".grib"
                        if os.path.isfile(FileIN_FC_temp1) and os.path.isfile(FileIN_FC_temp2):
                              tp1 = mv.read(FileIN_FC_temp1)
                              tp2 = mv.read(FileIN_FC_temp2)
                              tp = (tp2-tp1) * 1000
                  elif SystemFC == "ecPoint_MultipleWT" or SystemFC == "ecPoint_SingleWT": # Note: the forecasts are already accumulated over the considered period, and are already expressed in mm. The forecasts are stored in files whose name indicates the end of the accumulated period.
                        FileIN_FC_temp= Git_repo + "/" + DirIN_FC + "/" + SystemFC + "/" + TheDate.strftime("%Y%m%d%H") + "/Pt_BiasCorr_RainPERC/Pt_BC_PERC_" + f"{Acc:03d}" + "_" + TheDate.strftime("%Y%m%d") + "_" + TheDate.strftime("%H") + "_" + f"{StepF:03d}" + ".grib"
                        if os.path.isfile(FileIN_FC_temp):
                              tp = mv.read(FileIN_FC_temp)

                  # Checking that the rainfall forecasts exist for the considered date.
                  if len(tp) != 0:
                        
                        NumEM = int(mv.count(tp))

                        # Defining the valid time for the accumulation period
                        ValidTimeF = TheDate + timedelta(hours=StepF)

                        # Computing the counts for a specific date
                        FileIN_OBS_temp = Git_repo + "/" + DirIN_OBS + "/" + ValidTimeF.strftime("%Y%m%d") + "/tp" + f"{Acc:02d}" + "_obs_" + ValidTimeF.strftime("%Y%m%d%H") + ".geo"
                        if os.path.isfile(FileIN_OBS_temp): # Checking that the rainfall observations exist for the considered date.
                              
                              # Reading the rainfall observations
                              # Note: the rainfall observations are already accumulated, and are stored in files whose name indicates the end of the accumulated period.
                              obs = mv.read(FileIN_OBS_temp)
                              
                              # Extracting the forecasts for the nearest grid-boxes to the observations' location
                              tp_at_obs = []
                              for ind_EM in range(NumEM): 
                                    tp_at_obs.append(mv.values(mv.nearest_gridpoint(tp[ind_EM],obs)))
                              tp_at_obs = np.array(tp_at_obs)

                              # Computing the counts for a specific VRT
                              for VRT in VRT_list:

                                    # Counting the ensemble members exceeding the VRT, and converting the observations into a field of 1s and 0s
                                    countEM_exceeding_VRT = np.sum((tp_at_obs >= VRT), axis=0)
                                    countOBS_exceeding_VRT = mv.values(obs >= VRT)
                                    
                                    # Merging the arrays containing the counts of ensemble members and observations exceeding the VRT
                                    count_EM_OBS_exceeding_VRT = np.vstack([countEM_exceeding_VRT, countOBS_exceeding_VRT])

                                    # Saving the counts
                                    DirOUT_temp= Git_repo + "/" + DirOUT + "/" + f"{Acc:02d}" + "h/" + SystemFC + "/" + str(VRT) + "/" + TheDate.strftime("%Y%m%d%H")
                                    FileNameOUT_temp = "Count_EM_OBS_" + f"{Acc:02d}" + "h_" + SystemFC + "_" + str(VRT) + "_" + TheDate.strftime("%Y%m%d") + "_" + TheDate.strftime("%H") + "_" + f"{StepF:03d}"
                                    if not os.path.exists(DirOUT_temp):
                                          os.makedirs(DirOUT_temp)
                                    np.save(DirOUT_temp + "/" + FileNameOUT_temp, count_EM_OBS_exceeding_VRT)

            TheDate += timedelta(days=1)         