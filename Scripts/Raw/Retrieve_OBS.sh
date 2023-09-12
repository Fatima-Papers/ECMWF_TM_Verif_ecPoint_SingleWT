#!/bin/bash

##################################################################
# CODE DESCRIPTION
# Retrieve_OBS.sh retrieves rainfall observations from STVL
# Files contain rainfall observation from global rain gauges, 
# for the considered accumulation period , 
# ending at the time (in UTC) indicated in the file name.

# INPUT PARAMETERS DESCRIPTION
# DateS (date, in YYYYMMDD format): first date of observations to retrieve
# DateF (date, in YYYYMMDD format): last date of observations to retrieve
# Acc (number, in H format, in hours): observations' accumulation period 
# Git_repo (string): repository's local path
# DirOUT (string): relative path where to store the retrieved observations

# INPUT PARAMETERS
DateS=20211201
DateF=20221210
Acc=12
Git_repo="/ec/vol/ecpoint_dev/mofp/Papers_2_Write/Verif_ecPoint_SingleWT"
DirOUT="Data/Raw/OBS"
##################################################################


# --- DO NOT MODIFY --- #


# Setting general variables
MainDir=${Git_repo}/${DirOUT}
DateS=$(date -d ${DateS} +%Y%m%d)
DateF=$(date -d ${DateF} +%Y%m%d)
AccSTR=$(printf %03d ${Acc})

# Retrieving observations from STVL
TheDate=${DateS}
while [[ ${TheDate} -le ${DateF} ]]; do
    mkdir -p ${MainDir}/${TheDate}
    /home/moz/bin/stvl_getgeo --sources synop hdobs efas --parameter tp --period ${Acc} --dates ${TheDate} --times 00 06 12 18 --columns value_0 --outdir ${MainDir}/${TheDate} --flattree
    TheDate=$(date -d"${TheDate} + 1 day" +"%Y%m%d")
done
