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

def multipleFileReadLines(filePaths): 
    """ Generator for concurrent lines in files from a list of full file paths 
     
        A fileBuffer is loaded for each file, opening and then closing a single file at a time. 
        The position in the file is recorded with each fileBuffer extraction,
        so the next opening of the file will extract lines from the proper position.  
        All files are assumed to have the same number of records, but line length need not be the same 
    """ 
 
    buffers = [] 
    filePositions = [] 
    
    for filePath in filePaths: 
        lines, filePosition= readMultipleFileLinesAndPositions(filePath) 
        buffers.append(lines) 
        filePositions.append(filePosition)  
        
    linesRemaining = True 
 
    while linesRemaining: 
        currentLines = [] 
        for i,fileBuffer in enumerate(buffers): 
            currentLines.append(fileBuffer[0].strip()) 
 
            del fileBuffer[0] 
                
            if ( not(fileBuffer) and linesRemaining): 
                lines, filePosition = readMultipleFileLinesAndPositions(filePaths[i],filePositions[i]) 
                buffers[i] = lines 
                filePositions[i] =  filePosition 
                linesRemaining = bool(lines) 
 
        yield currentLines 
 
 
def readMultipleFileLinesAndPositions(filePath,startPosition=None, bytesToRead=1): 
    """ Extracts lines from file, starting at the specified startPosition. 
     
        The file-object's readlines() method is used to extract lines,  
        and the tell() method is used to return the position of the next line in the file. 
        The bytesToRead value is passed as an argument to readlines().  The default bytesToRead value is set to 1  
        so that readlines() uses its own default buffer size (somewhere near 8359 bytesToRead) 
     
    """ 
    
    f = open(filePath, 'rb') 
    
    if not startPosition is None: 
        f.seek(startPosition) 
    
    lines = f.readlines(bytesToRead) 
    position = f.tell() 
    
    f.close() 
    
    return lines, position 

