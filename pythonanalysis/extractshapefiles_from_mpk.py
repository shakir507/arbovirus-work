import arcpy
import os

arcpy.env.overwriteOutput = True
# Set folder that contains packages to extract
arcpy.env.workspace = "C:/geoprocessing/mpks"  # Change the path to your .mpk files
wrksp = arcpy.env.workspace

for mpk in arcpy.ListFiles("*.mpk"):
    print("Extracting... " + mpk)
    arcpy.ExtractPackage_management(mpk, os.path.splitext(mpk)[0])
print("Done")