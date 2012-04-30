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
""" Element tree testing

    
"""



from xml.etree.ElementTree import Element, ElementTree



class FolderTree(ElementTree):
    """Element whith extra find or create method to create subelement from path if it doesn't exist"""
    
    PATH_SEPARATOR = "/"
    FOLDER_TAG = "folder"
    ROOT_TAG = "root"
    FILE_TAG = "file"
    
    def __init__(self, folderItems):
        """ Initialize object """
        
        self.folders = folderItems
        
        root = Element(self.ROOT_TAG)
        self._setroot(root)
        

              
if __name__ == "__main__":
    
    ft = FolderTree([])
    print ft.getroot()
    
    
    
    
