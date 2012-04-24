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

''' Time related utilities

'''

from datetime import datetime

class DateTimer:
    ''' Handy timer that reports start time, end time and delta time

        report:(default=True) If True, prints automatically

        Example usage:
        
            from majgis.time import DateTimer
            import time
            
            timer = DateTimer()
            timer.start()
            time.sleep(10)
            timer.stop()
            
        Example output:

            Started: 2012-01-23 14:40:37
            Finished: 2012-01-23 14:40:47 (Elapsed: 0:00:10)

    '''

    NO_START_MSG = "Timer was never started."
    FINISH_MSG = "Finished: {0} (Elapsed: {1})"
    START_MSG = "Started: {0}"

    def __init__(self, report=True):
        """ Initialize """
        
        self.report = report
        self.startDateTime = None
        self.endDateTime = None
        self.deltaTime = None

    def start(self):
        """ Start the timer. """
        self.__init__(self.report)
        self.startDateTime = datetime.now()
        self.endDateTime = None

        if self.report:
            self.printStart()

    def stop(self):
        """ Stop the timer. """
        self.endDateTime = datetime.now()
        if self.startDateTime:
            self.deltaTime = self.endDateTime - self.startDateTime

        if self.report:
            self.printEnd()

    def printStart(self):
        """ Print the start time. """
        
        if self.startDateTime:
            print self.START_MSG.format(self.datetimeToString(self.startDateTime))
        else:
            print self.NO_START_MSG

    def printEnd(self):
        """ Print the end time"""
        
        if self.deltaTime:
            print self.FINISH_MSG.format(self.datetimeToString(self.endDateTime), self.deltaToString(self.deltaTime))
        else:
            print self.NO_START_MSG

    def datetimeToString(self, dateTimeObject):
        """ Convert datetime object to string"""
        
        return str(dateTimeObject).split(".")[0]

    def deltaToString(self, delta):
        """ Convert delta object(elapsed time) to string. """
        return str(delta).split(".")[0]
    
    
    