import os
from datetime import datetime, timedelta
import metview as mv

########################################################################################
# CODE DESCRIPTION
# 10_Plot_ProbFC.py plots a map plot with the forecast probabilities of exceeding a certain rainfall threshold.
# Note: runtime negligible.

# INPUT PARAMETERS DESCRIPTION
# BaseDate (date, in YYYYMMDD format): forecast base date.
# BaseTime (integer, from 0 to 23, in UTC): forecast base time.
# StepF (integer, in hours): step corresponding to end of the accumulation period. 
# Acc (number, in hours): rainfall accumulation to consider.
# Thr (float, in mm): rainfall threshold to consider.
# Operator (string): operator indicating whether the probabilities are computed for tp >= or < Thr.
# SystemFC_list (list of strings): list of the forecasting systems to consider.
# Git_repo (string): repository's local path.
# DirIN (string): relative path containing the forecasts.
# DirOUT (string): relative path of the directory containing the forecast probability's map plots.

# INPUT PARAMETERS
BaseDate = datetime(2021,12,9)
BaseTime = 0
StepF = 48
Acc = 12
Thr = 10
Operator = ">="
SystemFC_list = ["ENS", "ecPoint_MultipleWT", "ecPoint_SingleWT"]
Git_repo = "/ec/vol/ecpoint_dev/mofp/Papers_2_Write/Verif_ecPoint_SingleWT"
DirIN = "Data/Raw/FC"
DirOUT = "Data/Plot/10_ProbFC"
########################################################################################


for SystemFC in SystemFC_list:

      print("Creating and saving the map plot of the probability of tp " + Operator + " " + str(Thr)  + " mm/" + str(Acc) + "h for " + SystemFC)

      # Reading the forecasts
      Base_Date_Time = BaseDate + timedelta(hours=BaseTime)
      StepS = StepF - Acc
      if SystemFC == "ENS":
            tp_S = mv.read(Git_repo + "/" + DirIN + "/" + SystemFC + "/" + Base_Date_Time.strftime("%Y%m%d%H") + "/tp_" + Base_Date_Time.strftime("%Y%m%d") + "_" + Base_Date_Time.strftime("%H") + "_" + f"{StepS:03d}" + ".grib")
            tp_F = mv.read(Git_repo + "/" + DirIN + "/" + SystemFC + "/" + Base_Date_Time.strftime("%Y%m%d%H") + "/tp_" + Base_Date_Time.strftime("%Y%m%d") + "_" + Base_Date_Time.strftime("%H") + "_" + f"{StepF:03d}" + ".grib")
            tp = (tp_F - tp_S) * 1000
      else:
            tp = mv.read(Git_repo + "/" + DirIN + "/" + SystemFC + "/" + Base_Date_Time.strftime("%Y%m%d%H") + "/Pt_BiasCorr_RainPERC/Pt_BC_PERC_" + f"{Acc:03d}" + "_" + Base_Date_Time.strftime("%Y%m%d") + "_" + Base_Date_Time.strftime("%H") + "_" + f"{StepF:03d}" + ".grib")

      # Computing the probabilities
      NumEM = mv.count(tp)
      if Operator == ">=":
            prob = mv.sum(tp >= Thr) / NumEM * 100
      elif Operator == "<":
            prob = mv.sum(tp < Thr) / NumEM * 100

      # Plot the probabilities
      coastlines = mv.mcoast(
            map_coastline_colour = "charcoal",
            map_coastline_thickness = 3,
            map_coastline_resolution = "medium",
            map_boundaries = "on",
            map_boundaries_colour = "charcoal",
            map_boundaries_thickness = 3,
            map_grid_latitude_increment = 30,
            map_grid_longitude_increment = 60,
            map_label_right = "off",
            map_label_top = "off",
            map_label_colour = "charcoal",
            map_grid_thickness = 3,
            map_grid_colour = "grey",
            map_label_height = 3
            )

      contouring = mv.mcont(
            legend = "on",
            contour = "off",
            contour_level_selection_type = "level_list",
            contour_min_level = 0,
            contour_level_list = [0,0.5,1.5,2.5,3.5,4.5,6.5,8.5,10.5,13.5,16.5,20.5,25.5,30.5,35.5,40.5,50.5,60.5,70.5,80.5,90.5,100],
            contour_label = "off",
            contour_shade = "on",
            contour_shade_colour_method = "list",
            contour_shade_method = "area_fill",
            contour_shade_colour_list = ["white","RGB(0.61,0.91,0.95)","RGB(0.091,0.89,0.99)","RGB(0.015,0.7,0.81)","RGB(0.031,0.55,0.62)","RGB(0.025,0.66,0.24)","RGB(0.015,0.81,0.28)","RGB(0.13,0.99,0.42)","RGB(0.8,0.99,0.13)","RGB(0.65,0.83,0.013)","RGB(0.51,0.64,0.026)","RGB(0.78,0.35,0.017)","RGB(0.92,0.4,0.0073)","RGB(0.99,0.5,0.17)","RGB(0.97,0.65,0.41)","RGB(0.96,0.47,0.54)","RGB(0.98,0.0038,0.1)","RGB(0.88,0.45,0.96)","RGB(0.87,0.26,0.98)","RGB(0.7,0.016,0.79)","RGB(0.52,0.032,0.59)"]
            )

      legend = mv.mlegend(
            legend_text_colour = "charcoal",
            legend_text_font = "arial",
            legend_text_font_size = 3,
            legend_entry_plot_direction = "row",
            legend_box_blanking = "on",
            legend_entry_text_width = 50
            )

      VT_S = Base_Date_Time + timedelta(hours=StepS)
      VT_F = Base_Date_Time + timedelta(hours=StepF)
      title_plot1 = "Probability of tp " + Operator + " " + str(Thr) + " mm/" + str(Acc) + "h - " + SystemFC
      title_plot2 = "FC: " + Base_Date_Time.strftime("%d-%m-%Y") + " at " + Base_Date_Time.strftime("%H") + " UTC (t+" + str(StepS) + ",t+" + str(StepF) + ")"
      title_plot3 = "VT: " + VT_S.strftime("%d") + " " + VT_S.strftime("%B") + " " + VT_S.strftime("%Y") + " at " + VT_S.strftime("%H") + " UTC to " + VT_F.strftime("%d") + " " + VT_F.strftime("%B") + " " + VT_F.strftime("%Y") + " at " + VT_F.strftime("%H") + " UTC"
      title = mv.mtext(
            text_line_count = 3,
            text_line_1 = title_plot1,
            text_line_2 = title_plot2,
            text_line_3 = title_plot3,
            text_colour = "charcoal",
            text_font_size = 4
            )

      # Saving the map plot
      MainDirOUT = Git_repo + "/" + DirOUT
      if not os.path.exists(MainDirOUT):
            os.makedirs(MainDirOUT)
      FileOUT = MainDirOUT + "/Prob_" + str(Thr) + "_" +  SystemFC
      png = mv.png_output(output_width = 5000, output_name = FileOUT)
      mv.setoutput(png)
      mv.plot(prob, coastlines, contouring, legend, title)