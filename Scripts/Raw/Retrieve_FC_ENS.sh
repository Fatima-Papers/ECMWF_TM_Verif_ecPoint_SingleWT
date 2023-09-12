#!/bin/bash

##################################################################
# CODE DESCRIPTION
# Retrieve_ENS.sh retrieves raw ECMWF ENS rainfall forecasts from MARS.
# Files contain cumulative global rainfall forecasts 
# up to the step indicated in the file name.

# INPUT PARAMETERS DESCRIPTION
# BaseDateS (date, in YYYYMMDD format): first forecast's basedate to retrieve
# BaseDateF (date, in YYYYMMDD format): last forecast's basedate to retrieve
# BaseTime (time, in H format, in UTC time): forecast's basetime to retrieve 
# StepS (number, in hours): first forecast's step to retrieve
# StepF (number, in hours): last forecast's step to retrieve
# DiscStep (number, in hours): discretization to retrieve forecasts' steps
# Git_repo (string): repository's local path
# DirOUT (string): relative path where to store the retrieved forecasts

# INPUT PARAMETERS
BaseDateS=20211201
BaseDateF=20221130
BaseTime=0
StepS=0
StepF=246
DiscStep=6
Git_repo="/ec/vol/ecpoint_dev/mofp/Papers_2_Write/Verif_ecPoint_SingleWT"
DirOUT="Data/Raw/FC/ENS"
##################################################################


# --- DO NOT MODIFY --- #


# Setting general variables
MainDir=${Git_repo}/${DirOUT}
BaseDateS=$(date -d ${BaseDateS} +%Y%m%d)
BaseDateF=$(date -d ${BaseDateF} +%Y%m%d)
BaseTimeSTR=$(printf %02d ${BaseTime})

# Retrieving forecasts from MARS
BaseDate=${BaseDateS}
while [[ ${BaseDate} -le ${BaseDateF} ]]; do
    MainDir_temp="${MainDir}/${BaseDate}${BaseTimeSTR}"
    mkdir -p ${MainDir_temp}
mars <<EOF
    retrieve,
        class=od,
        date=${BaseDate},
        expver=1,
        levtype=sfc,
        param=228.128,
        step=${StepS}/to/${StepF}/by/${DiscStep},
        stream=enfo,
        time=${BaseTime},
        type=cf,
        target="${MainDir_temp}/tp_${BaseDate}_${BaseTimeSTR}_[step].grib"
    retrieve,
        type=pf,
        number=1/to/50
EOF

    # Renaming the retrieved files 
    for Step in $(seq ${StepS} ${DiscStep} ${StepF}); do
        StepSTR=$(printf %03d ${Step})
        mv "${MainDir_temp}/tp_${BaseDate}_${BaseTimeSTR}_${Step}.grib" "${MainDir_temp}/tp_${BaseDate}_${BaseTimeSTR}_${StepSTR}.grib"
    done

    BaseDate=$(date -d"${BaseDate} + 1 day" +"%Y%m%d")

done