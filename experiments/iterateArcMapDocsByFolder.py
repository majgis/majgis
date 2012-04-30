#   Copyright 2012 majgis Contributors
#    
#   Individuals comprising majgis Contributors are identified in 
#   the NOTICE file found in the root directory of this project.
#
#   Licensed under the Apache License, Version 2.0 (the "License");
#   you may not use this file except in compliance with the License.
#   You may obtain a copy of the License at
#
#       http://www.apache.org/licenses/LICENSE-2.0
#         or
#       in the file named LICENSE in the root directory of this project.
#
#   Unless required by applicable law or agreed to in writing, software
#   distributed under the License is distributed on an "AS IS" BASIS,
#   WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#   See the License for the specific language governing permissions and
#   limitations under the License.
""" From a list of folders, export msd documents from existing mxds, ArcGIS 10

"""

import os
from glob import glob
from arcpy import mapping
from symbologyFromArcMapDoc import MxdExtras


folders = [r'F:\Projects\NationalAtlas\ArcGIS_Server\Server', r'F:\Projects\NationalAtlas\ArcGIS_Server\Server\biodiversity']
searchPattern = '*.mxd'
ignores = ['Overlap']
tempMsg = "{0:>90}  ->  {1}"
newMsg =   "TABLE: {0}  FIELD: {1}"
mxdSuffix = ".mxd"
msdSuffix = ".msd"

for folder in folders:
    mxdPaths = glob(os.path.join(folder, searchPattern))
    
    for mxdPath in mxdPaths:
        
        mxd = mapping.MapDocument(mxdPath)
        lyrs = mapping.ListLayers(mxd)
        mxde = MxdExtras(mxdPath)
        
        msdPath = mxdPath.replace(mxdSuffix, msdSuffix)
        
        for lyr in lyrs:
            
            lyre = mxde[lyr.name]
            
            joinTable = lyre.joinedTableName
            joinField = lyre.symbologyShortFieldName
            
            if joinTable:
                newName = newMsg.format(joinTable, joinField)
            else:
                newName = lyr.name
                
            #print  tempMsg.format(lyr.name, newName)
            lyr.name = newName
            
        mxd.save()
        
        #delete existing msd
        if os.path.exists(msdPath):
            os.remove(msdPath)
            
        
        #export msd
        mapping.ConvertToMSD(mxd,msdPath)
        print msdPath
        
        


        