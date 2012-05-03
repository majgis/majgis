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

""" Experiments to validate an xml file against an xsd file
    
    references:
        http://lxml.de/validation.html#xmlschema
      
"""


from lxml import etree
from glob import glob


def main(argv):
    ''' Script to validate '''
    
    xsdPath = argv[1]
    xmlSearch = argv[2]
    
    xmlPaths = glob(xmlSearch)
    
    for xmlPath in xmlPaths:
        validateXmlWithXsd(xsdPath, xmlPath)    
    


def validateXmlWithXsd(xsdPath, xmlPath):
    '''Validate xml file using xsd file '''
    
    xmlFile = open(xmlPath)
    xsdFile = open(xsdPath)
    
    xsd = etree.parse(xsdFile)
    xml = etree.parse(xmlFile)
    
    schema = etree.XMLSchema(xsd)
    
    
    if schema.validate(xml):
        print
        print xmlPath + ' is valid'
    else:
        print
        print xmlPath + ' is INVALID!'
        print schema.error_log.last_error
    
    

if __name__ == "__main__":
    
    xsdPath = "xsd/lcc.xsd"
    xmlSearch = "xml/*.lcc"
    
    argv = [__file__, xsdPath, xmlSearch]
    
    main(argv)
    
    
