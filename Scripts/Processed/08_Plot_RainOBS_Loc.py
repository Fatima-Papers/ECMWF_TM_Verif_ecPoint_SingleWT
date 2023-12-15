import os
from datetime import datetime, timedelta
import metview as mv

########################################################################################
# CODE DESCRIPTION
# 08_Plot_RainOBS_Loc.py plots a map plot with the location of the observations.
# Note: runtime negligible.

# INPUT PARAMETERS DESCRIPTION
# Acc (number, in hours): rainfall accumulation to consider.
# VRE_list (list of floats, from 0 to infinite, in mm): list of verifing rainfall events (VRE).
# CL (integer from 0 to 100, in percent): confidence level for the definition of the confidence intervals.
# SystemFC_list (list of strings): list of names of forecasting systems to consider.
# Colour_SystemFC_list (list of strings): colours used to plot the BSrel values for different forecasting systems.
# Git_repo (string): repository's local path.
# DirIN (string): relative path containing the real and boostrapped BSrel values.
# DirOUT (string): relative path of the directory containing the plots of the real and boostrapped BSrel values.

# INPUT PARAMETERS
TheDate = datetime(2021,12,10)
Acc = 12
StartPeriod_list = [0, 6, 12, 18]
Git_repo = "/ec/vol/ecpoint_dev/mofp/Papers_2_Write/Verif_ecPoint_SingleWT"
DirIN = "Data/Raw/OBS"
DirOUT = "Data/Plot/08_RainOBS_Loc"
########################################################################################


# Plotting the location of the rainfall observations for a specific accumulation period
obs_all = None
for ind_StartPeriod in range(len(StartPeriod_list)):

      StartPeriod = StartPeriod_list[ind_StartPeriod]
      
      # Reading the rainfall observation for a specific date
      TheDateTime = TheDate + timedelta(hours = (StartPeriod+Acc))
      obs = mv.read(Git_repo + "/" + DirIN + "/" + TheDateTime.strftime("%Y%m%d") + "/tp" + f"{Acc:02d}" + "_obs_" + TheDateTime.strftime("%Y%m%d%H") + ".geo")
      obs_all = mv.merge(obs_all, obs)
      print("N. obs for accumulatio period ending at " + str(StartPeriod) + " UTC: " + str(mv.count(obs)))

# Plotting the location of the observations
coastlines = mv.mcoast(
      map_coastline_colour = "grey",
      map_coastline_thickness = 1,
      map_coastline_resolution = "high",
      map_boundaries = "on",
      map_boundaries_colour = "grey",
      map_boundaries_thickness = 1,
      map_grid_latitude_increment = 30,
      map_grid_longitude_increment = 60,
      map_label_right = "off",
      map_label_top = "off",
      map_label_colour = "charcoal",
      map_grid_thickness = 1,
      map_grid_colour = "grey",
      map_label_height = 0.5
      )

obs_symb = mv.psymb(
      symbol_type = "marker",
      symbol_table_mode = "on",
      legend = "off",
      symbol_quality = "high",
      symbol_min_table = [0],
      symbol_max_table = [10000],
      symbol_marker_table = [15],
      symbol_colour_table = ["blue"],
      symbol_height_table = [0.05]
      )

title = mv.mtext(
      text_line_count = 1,
      text_line_1 = "Rain gauge locations",
      text_colour = "charcoal",
      text_font_size = 0.75
      )

# Saving the map plot
print("Saving the map plot ...")
MainDirOUT = Git_repo + "/" + DirOUT
if not os.path.exists(MainDirOUT):
    os.makedirs(MainDirOUT)
FileOUT = MainDirOUT + "/RainOBS_Loc" 
png = mv.png_output(output_name = FileOUT)
mv.setoutput(png)
mv.plot(obs_all, coastlines, obs_symb, title)