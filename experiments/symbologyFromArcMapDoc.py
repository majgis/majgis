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
""" Exposes extra MXD details by raiding an exported msd

    Must have write access to MXD directory (creates temporary msd file)
    
    
    !!INCOMPLETE:  Working only for a single type of symbology, some layers are skipped
    
"""    

import zipfile
from arcpy import mapping
import os
from xml.dom.minidom import parse



class LayerExtras(object):
    
    name = "" # name of layer in msd; will match name in mxd was basis for dictionary key
    symbologyShortFieldName = "" # If joined table, table name prefix is excluded
    symbologyFullFieldName = "" # keeps table name prefix
    joinedTableName = "" # name of joined table providing field


class MxdExtras(dict):
    """ Exposes extra MXD details by raiding an exported msd
    
        Must have write access to MXD directory (creates temporary msd file)
        
        
        !!INCOMPLETE:  Working only for a single type of symbology, some layers are skipped
        
    """    
    
    LYR_NAME_NODE = "Name"
    LYR_SYMBOL_NODE = "Symbolizer"
    LYR_FIELD_NODE = "Field"
    MSD_SUFFIX = "_MxdExtrasTemp.msd"
    MXD_SUFFIX = ".mxd"
    EXCLUDED_FILE_NAMES = ["DocumentInfo.xml", "layers/layers.xml"]
    JOIN_TABLE_DELIM = "."
    mxdPath = ""
    
    def __init__(self, mxdPath):
        
        self.loadMxdPath(mxdPath)
        
  
    def loadMxdPath(self, mxdPath):
        
        self.mxdPath = mxdPath.lower()
        mxd = mapping.MapDocument(self.mxdPath)
        
        msdPath = self.mxdPath.replace(self.MXD_SUFFIX, self.MSD_SUFFIX) 
        
        # Delete temporary msd if it exists
        if os.path.exists(msdPath):
            os.remove(msdPath)
            
        mapping.ConvertToMSD(mxd,msdPath)
        
        zz = zipfile.ZipFile(msdPath)

        for fileName in (fileName for fileName in zz.namelist() if not fileName in self.EXCLUDED_FILE_NAMES):
            dom = parse(zz.open(fileName))
            name, lyr = self.loadMsdLayerDom(dom)
            self[name] = lyr
        del zz
        
        os.remove(msdPath)
        

    def loadMsdLayerDom(self, dom):
        
        lyr = LayerExtras()  
        
        try:
            
            # Layer name
            lyr.name = dom.getElementsByTagName(self.LYR_NAME_NODE)[0].childNodes[0].nodeValue
            
            # Symbology full field name
            symbologyElement = dom.getElementsByTagName(self.LYR_SYMBOL_NODE)[0]
            lyr.symbologyFullFieldName = symbologyElement.getElementsByTagName(self.LYR_FIELD_NODE)[0].childNodes[0].nodeValue
            
            fieldSplit = lyr.symbologyFullFieldName.split(self.JOIN_TABLE_DELIM)

            # Symbology short field name
            if len(fieldSplit) > 1:
                lyr.joinedTableName = fieldSplit[0]
                lyr.symbologyShortFieldName = fieldSplit[1]
            else:
                lyr.symbologyShortFieldName = fieldSplit[0]
                
            
            
        except:
            pass
        
        return lyr.name, lyr
        
    

