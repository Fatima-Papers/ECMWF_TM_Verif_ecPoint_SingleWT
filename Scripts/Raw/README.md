## Background
The scripts' name in **"Scripts/Raw"** indicate the action computed by the script, as well as the location where the outputs will be stored. The name does not indicate any order which the scripts need to be run with because the scripts can typically be run indipendently.

### Examples

**Retrieve_FC_[DirOUT]** -> This script _retrieves_ forecasts from ECMWF or from the web, and saves it in _"/Data/Raw/FC/[DirOUT]"_. If the forecasts are provided ready to be used, the name of the script contains the sufix _"README.txt"_ and contains only information on the data provider (e.g., **Retrieve_FC_[DirOUT]_README.txt**).

**Retrieve_OBS_[DirOUT]** -> This script _retrieves_ observations from ECMWF or from the web, and saves it in _"/Data/Raw/OBS/[DirOUT]"_. If the observations are provided ready to be used, the name of the script contains the sufix _"README.txt"_ and contains only information on the data provider (e.g., **Retrieve_FC_[DirOUT]_README.txt**).

**Create_[DirOUT]** -> This script _creates_ raw data from scratch, and saves it in _"/Data/Raw/[DirOUT]"_.