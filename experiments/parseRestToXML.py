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
''' Creates text file with content for Flex Viewer config.xml using REST url
'''

import sys
import os
import arcpy
import re
import json
import urllib

def main(argv):
    """ Start of execution. """

    xmlSnippit = \
    """
            <layer
                label="{0}"
                type="dynamic"
                visible="false"
                alpha="0.8"
                url="{1}"
            />
    """

    serviceUrl = arcpy.GetParameterAsText(0).replace("'","").replace('"','').strip()
    outTextFilePath = arcpy.GetParameterAsText(1).replace("'","")
    reverseOrder = bool(arcpy.GetParameterAsText(2))
    startFile = bool(arcpy.GetParameterAsText(3))

    outFile = open(outTextFilePath, "w")

    jsonUrl = serviceUrl.split("?")[0] + "?f=json"
    services = convertJsonUrlToObject(jsonUrl)["services"]
    serviceNames = serviceNamesFromServices(services)

    if reverseOrder:
        for serviceNamesIndex in xrange(len(serviceNames)-1, -1, -1):
            serviceName = serviceNames[serviceNamesIndex]
            url = serviceUrl + "/" + serviceName + "/MapServer"
            name = parseMapServerName(serviceName)

            outFile.write(xmlSnippit.format(name, url))
    else:
        for serviceName in serviceNames:
            url = serviceUrl + "/" + serviceName + "/MapServer"
            name = parseMapServerName(serviceName)

            outFile.write(xmlSnippit.format(name, url))

    if startFile:
        os.startfile(outTextFilePath)


def serviceNamesFromServices(services):
    """ Extract service names from services"""

    return [str(service["name"]).split("/")[1] for service in services]


def parseMapServerName(serviceName):
    """  Convert map service name to normally spaced name.

         Underscore replaced with " - "
         Of replaced with of
         The replaced with the

         serviceName: Map service name
    """

    underScoreSplit = serviceName.split("_")

    for i,underScore in enumerate(underScoreSplit):
        underScore = spaceOutCamelCase(underScore)
        underScore = underScore.replace("Of ", "of ").replace("The ","the ")
        underScoreSplit[i] = underScore

    return " - ".join(underScoreSplit)


def convertJsonUrlToObject(serviceUrl):
    """ Convert json object from url to Python object. """


    restResponseFp = urllib.urlopen(serviceUrl) # file pointer

    return json.load(restResponseFp)


def spaceOutCamelCase(s):
    """ Adds spaces to a camel case string.

        Failure to space out string returns the original string.

        References:
          http://refactormycode.com/codes/675-camelcase-to-camel-case-python-newbie
    """

    return re.sub('((?=[A-Z1-9][a-z])|(?<=[a-z])(?=[A-Z1-9]))', ' ', s).strip()


if __name__ == '__main__':
    main(sys.argv)