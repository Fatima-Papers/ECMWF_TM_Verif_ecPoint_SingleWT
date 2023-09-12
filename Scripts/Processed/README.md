## Background
The scripts' name in **"Scripts/Processed"** indicate the order which the scripts need to be run with, and the location where the outputs will be stored.

### Examples

**01_Compute_[DirOUT]** -> This script is the _first one to run_ as the name starts with _"01"_ (preferibly, start the numbers with a leading zero to maintain the correct order which the scripts need to be run with). The term _"Compute"_ indicates that the outputs of the script are typically numerical (e.g. csv tables, grib files, geopoints, etc), so that they will be saved in the directory _"/Data/Compute/01_[DirOUT]"_.

**02_Plot_[DirOUT]** -> This script is the _second one to run_ as the name starts with _"02"_ (preferibly, start the numbers with a leading zero to maintain the correct order which the scripts need to be run with). The term _"Plot"_ indicates that the outputs of the script are typically graphical (e.g. png, jpeg, ps, svg, etc.), so that they will be saved in the directory _"/Data/Plot/02_[DirOUT]"_.

**03_ComputePlot_[DirOUT]** -> This script is the _third one to run_ as the name starts with _"03"_ (preferibly, start the numbers with a leading zero to maintain the correct order which the scripts need to be run with). The term _"ComputePlot"_ indicates that the outputs of the script are both numerical (e.g. csv tables, grib files, geopoints, etc) and graphical (e.g. png, jpeg, ps, svg, etc.), so that they will be saved in the directories _"/Data/Compute/[DirOUT]"_ and _"/Data/Plot/03_[DirOUT]"_ , respectively.