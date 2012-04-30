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
""" Random Python experiments

    Mature utilities are migrated to the majgis Python package.
"""

import sys
import csv
from collections import defaultdict
from xml.etree.ElementTree import Element, ElementTree

CONTENT_TAG = "{content}"
FOLDER_DELIM = ";"
FOLDER_SEPARATOR = "/"
NAME_COLUMN_INDEX = 0
FOLDERS_COLUMN_INDEX = 1


def main(argv):
    """ first function to execute """

    csvPath = r"F:\Projects\NationalAtlas\src\htmGenerate\serviceFolderHierarchy.csv"
    inHtmTemplate = r"F:\Projects\NationalAtlas\src\htmGenerate\index.html"
    outHtm = r"F:\Projects\NationalAtlas\src\NationalAtlas_HTML.git\DataFactSheets\index.html"
    
    rows = csv.reader(open(csvPath, 'rb'), dialect='excel')

    hft = HtmlFolderTree(rows)
    hft.write(open(r'c:\temp\out\out.htm','w'))


class HtmlFolderTree(ElementTree):
    """ Generates html as ul/li tags
    
        rows:  file object, example:  csv.reader(open(csvPath, 'rb'), dialect='excel')
        nameColumn:  Represents names of columns
        
        Attributes set to use collapsible folder example here: http://www.dynamicdrive.com/dynamicindex1/navigate1.htm
        
        Example of usage:
            hft = HtmlFolderTree(rows)
            hft.write(open(r'c:\temp\out\out.htm','w'))
        
    """
    
    PATH_SEPARATOR = "/"
    ROOT_ATTRIB = {"id":"treemenu2", "class":"treeview"}
    ITEM_TAG = "li"
    LIST_TAG = "ul"
    ANCHOR_TAG = "a"
    ANCHOR_TAG_ATTRIBUTES = '''"href":"{0}"'''
    LINK = '''pdf/{0}.pdf'''

    folderPathLookupElement = {}
    
    def __init__(self, rows, nameColumn=0, foldersColumn=1):
        """ Initialize object """
        
        folderItems = self.getFolderList(rows, nameColumn, foldersColumn)
        self.folders = folderItems
        self._setroot(self.newRootElement())
        self.loadFolders(folderItems)
            
    def getFolderList(self, rows, nameColumn=0, foldersColumn=1):
        """ Returns sorted list of folderPath/contents
            
            (('folder/folder/folder', [name, name, name]), ...)
                   
        """
        
        rows.next()# skip field headings
        dd = defaultdict(list)
        
        for row in rows:
            
            name = row[NAME_COLUMN_INDEX].strip()
            folders = row[foldersColumn].split(FOLDER_DELIM)
            #url = row[2].strip()
            
            for folder in folders:
                dd[folder.strip()].append(name)
            
        sortable = []
            
        for folder,itemList in dd.iteritems():
    
            sortable.append((folder,itemList))
            
        sortable.sort()
            
        return sortable        


    def loadFolders(self, folderItems):
                
        for folderPath, files in folderItems:
            self.createFolder(folderPath, files)
            
            
    def createFolder(self, path, fileNames):
        """ Creates and returns element at absolute path.
        
            path:  folder/folder/folder
            files: list of file names
            
        """
        # Dictionary holds existing folder elements
        cursorElement = self.folderPathLookupElement.get(path)
        
        # Folder elements will be created if they do not exist
        if cursorElement is None:
            
            cursorElement = self.getroot()
            
            for folderName, folderPath in self.iterPath(path):
                
                folderElement = self.folderPathLookupElement.get(folderPath)
    
                if folderElement is None:
                    folderElement = self.newFolderElement(folderName)
                    cursorElement.append(folderElement)
                    self.folderPathLookupElement[folderPath] = folderElement[0]
                    
                cursorElement = folderElement[0]
        
        for fileName in fileNames:
            fileElement = self.newFileElement(fileName)
            cursorElement.append(fileElement)


    def iterPath(self, path):
        """ Generator for tuple containing pathName, fullPath
            
            --example--
            path: 'a/b/c/d/e'
            result:
                ('a', 'a')
                ('b', 'a/b')
                ('c', 'a/b/c')
                ('d', 'a/b/c/d')
                ('e', 'a/b/c/d/e')    
        """
        
        pathIndex = 0
        folderNames = path.split(self.PATH_SEPARATOR)
        
        while pathIndex < len(folderNames):
            yield folderNames[pathIndex], self.PATH_SEPARATOR.join(folderNames[0:pathIndex + 1])
            pathIndex += 1
    
    
    def newFolderElement(self,name):
        
        folderElement = Element(self.ITEM_TAG)
        folderElement.text = name
        folderElement.append(self.newContainerElement())
        
        return folderElement
        
        
    def newFileElement(self, name):
        
        fileElement = Element(self.ITEM_TAG)
        link = self.LINK.format(name.replace(" ","_"))
        attributesStr = self.ANCHOR_TAG_ATTRIBUTES.format(link)
        attributes = eval("{" + attributesStr + "}")
        fileSubElement = Element(self.ANCHOR_TAG, attributes)
        fileSubElement.text = name
        fileElement.append(fileSubElement)
        
        return fileElement
    
    
    def newRootElement(self):
        
        rootElement = self.newContainerElement(self.ROOT_ATTRIB)
    
        return rootElement
        

    def newContainerElement(self, attrib={}):
        
        containerElement = Element(self.LIST_TAG, attrib) 
                    
        return  containerElement


if __name__ == '__main__':
    main(sys.argv)
    
    