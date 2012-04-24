#   Copyright 2012 Michael A. Jackson and majgis Contributors
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

''' File related utilities.

'''

import os

def getLastLine(f, blockSize=3072): 
    """Return the last line of a file 
    
       If the last line is an empty string, the second to last line is returned.
    
    """ 
    
    f.seek(0,os.SEEK_END) 
    
    totalBytes = f.tell() 
    
    if totalBytes > blockSize: 
        f.seek(-blockSize,os.SEEK_END) 
    else: 
        f.seek(0) 
        
    lastLines = f.readlines() 
    lastLine = lastLines[-1] 
    
    if lastLine =='': 
        lastLine = lastLines[-2] 
    
    return lastLine 
