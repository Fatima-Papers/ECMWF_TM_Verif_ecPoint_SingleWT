#!/bin/bash

#############################################################################
# CODE DESCRIPTION
# Retrieve_ecPoint retrieves ecPoint-Rainfall forecasts from ECFS. Files contain global rainfall 
# forecasts for the considered accumulation period, ending at the time step indicated in the 
# file name.

# INPUT PARAMETERS DESCRIPTION
# BaseDateS (date, in YYYYMMDD format): first forecast's basedate to retrieve
# BaseDateF (date, in YYYYMMDD format): last forecast's basedate to retrieve
# BaseTime (time, in H format, in UTC time): forecast's basetime to retrieve 
# Acc (number, in H format, in hours): observations' accumulation period 
# CodeVers (string): version of the code that was used to compute the forecasts.
#                                  See which code versions are available in the following webpage:
#                                  https://confluence.ecmwf.int/display/EVAL/Forecasts+Code
# CalVers (string): version of the calibration that was used to compute the forecasts.
#                              See which calibration versions are available in the following webpage:
#                              https://confluence.ecmwf.int/display/EVAL/1.+ecPoint-Rainfall%3A+Developed+or+Under-Development+Calibrations                               
# Git_repo (string): repository's local path
# DirOUT (string): relative path where to store the retrieved forecasts

# INPUT PARAMETERS
BaseDateS=20211201
BaseDateF=20221130
BaseTime=0
Acc=12
CodeVers="2.0.0"
CalVers="1.1.0"
Git_repo="/ec/vol/ecpoint_dev/mofp/Papers_2_Write/ECMWF_TM_Verif_ecPoint_SingleWT"
DirOUT="Data/Raw/FC/ecPoint_MultipleWT"
#############################################################################


# --- DO NOT MODIFY --- #


# Setting general variables
BaseDateS=$(date -d ${BaseDateS} +%Y%m%d)
BaseDateF=$(date -d ${BaseDateF} +%Y%m%d)
BaseTimeSTR=$(printf %02d ${BaseTime})
AccSTR=$(printf %03d ${Acc})

# Setting directories
EcfsDir="ec:/ecpoint/forecasts/Oper/ECMWF_ENS/Rainfall/${AccSTR}/Code${CodeVers}_Cal${CalVers}"
LocalDir=${Git_repo}/${DirOUT}
mkdir -p ${LocalDir}

# Retrieving forecasts from ECFS
BaseDate=${BaseDateS}
while [[ ${BaseDate} -le ${BaseDateF} ]]; do
    
    echo " "
    echo "Retrieving forecast for ${BaseDate}"
   ecfsdir ${EcfsDir}/${BaseDate}${BaseTimeSTR} ${LocalDir}/${BaseDate}${BaseTimeSTR}

    BaseDate=$(date -d"${BaseDate} + 1 day" +"%Y%m%d")

done
