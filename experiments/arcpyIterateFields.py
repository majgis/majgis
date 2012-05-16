''' iterate arcpy fields
'''

import arcpy
import os

shpPath = r"C:\MyFiles\pocosin\HYSPLIT\merged\Daily_Ave.shp"
wildCard = "pm*m"
outDir = r"C:\MyFiles\pocosin\HYSPLIT\animation"
outName = "idw_{0}"
cellSize = 0.03
power = 3
searchRadius = 20

processFields = arcpy.ListFields(shpPath, wildCard) 

for processField in processFields:
    outIdw = arcpy.sa.Idw(shpPath, processField, cellSize, power, searchRadius)
    
    processNumber = processField.replace('pm', '').replace('m','')
    outFilePath = os.path.join(outDir, outName.format(processNumber))
    outIdw.save(outFilePath)