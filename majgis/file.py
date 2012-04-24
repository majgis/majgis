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


class multipleFileWriterWithBuffer(): 
    """ Write lines to multiple files efficiently. 
     
        Maintains a buffer for each file.  
        Writes to disk when length of all strings in buffer exceeds strLen parameter. 
        Creating new strings is inefficient, so buffer is stored as list of strings. 
         
    """ 
    
    def __init__(self, filePaths=[], outDir=None, initialDelete=True, strLen=8092): 
        """ Initializer """ 
 
        # Class level variables 
        self.strLen = strLen 
        self.filePathDict = {} 
        self.outDir = outDir 
        
        if filePaths: 
            self.addFiles(filePaths) 
        
        # Delete files by default, unless default overridden  
        if initialDelete: 
            self.deleteAllFiles(False) 
 
            
    def __del__(self): 
        """ Destructor  
         
            Buffer is flushed when object is destroyed 
        """ 
        
        self.flush() 
 
 
    def __writeToFile(self, filePath, lst): 
        """ Write lines to file 
             
            Write lines joined by the delimiter. 
        """ 
        
        if not self.outDir is None: 
            filePath = os.path.join(self.outDir, filePath) 
        
        open(filePath,'a').writelines(lst) 
        
        
    def writeMultipleFileLines(self, filePaths, liness): 
        """ Write lines to multiple files 
         
            liness: list of lists, one for each filePath 
            Buffer is written to file when buffer exceeds strLen 
            Line separators are not added. 
        """ 
        
        for i,filePath in enumerate(filePaths): 
            self.writeSingleFileLines(filePath,liness[i]) 
            
            
    def writeSingleFileLines(self, filePath, lines):   
        """ Add lines in iterable to buffer 
         
            Buffer is written to file when buffer exceeds strLen 
            Line separators are not added 
        """ 
        
        lenAndBuffer = self.filePathDict[filePath]     
 
        for line in lines: 
            lenAndBuffer[1].append(line) 
            lenAndBuffer[0] = lenAndBuffer[0] + len(line) 
                
        if lenAndBuffer[0] > self.strLen: 
            self.__writeToFile(filePath,lenAndBuffer[1]) 
            lenAndBuffer[0] = 0 # set bytes to zero  
            lenAndBuffer[1] = [] 
    
        
    def writeMultipleFiles(self, filePaths, ss): 
        """ Write strings to multiple files """ 
        
        for i,filePath in enumerate(filePaths): 
            self.writeSingleFileLines(filePath, [ss[i]]) 
 
 
    def writeSingleFile(self, filePath, s): 
        """" Write string to file. """ 
        
        self.writeSingleFileLines(filePath, [s]) 
        
 
    def flush(self, write=True): 
        """ Flush all buffers, writing to files if write parameter is True""" 
 
        for filePath, (_strLen,fileBuffer) in self.filePathDict.items(): 
            if write: 
                self.__writeToFile(filePath, fileBuffer) 
            del fileBuffer[:] 
            
            
    def deleteAllFiles(self, flush=True): 
        """ Delete all files 
         
            Flush buffers if flush parameter is true, the default. 
        """ 
        
        if flush: 
            self.flush(False) 
 
        for filePath in self.filePathDict.keys(): 
            if self.outDir is None: 
                fullPath = filePath 
            else: 
                fullPath = os.path.join(self.outDir,filePath) 
                
            if os.path.exists(fullPath): 
                os.remove(fullPath) 
    
    
    def addFile(self, filePath): 
        """ Add file as file Path 
         
            Files are stored in a dictionary with filePath as key 
            and a list containing [string length integer, list of lines] as the value. 
        """    
        
        self.filePathDict[filePath] = [0,[]] 
            
        
    def addFiles(self, filePaths): 
        """ Add files as iterable of full file paths """ 
        
        for filePath in filePaths: 
            self.addFile(filePath) 