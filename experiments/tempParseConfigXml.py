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
""" 
"""

inFilePath = r"c:\temp\layers.txt"
outFilePath = r"c:\temp\layers.csv"
DELIM = ", "
output = []

for line in open(inFilePath):

    if "label=" in line:
        output.append(line.split('"')[1].replace(",", " -") + DELIM)
    if "url=" in line:
        output.append(line.split('"')[1])
        output.append("\n")
        
open(outFilePath, 'w').writelines(output)
