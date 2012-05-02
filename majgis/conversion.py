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
""" Conversion utilities
"""

def dmsToDecimalDegrees(degrees, minutes=0, seconds=0):
	"""  Convert degrees, minutes and seconds  to decimal degrees
	
	*Description:*
	
		This function accepts degrees, minutes or seconds as string, integer or float, to convert to decimal degrees 
		based on the following conditions:
		
		* Strings will be converted to floating point.  If the conversion fails, zero is used for that value
		* Any argument can be passed as a floating point.  For example, degrees=170 and minutes=25.231 will work.
		
	*Arguments:*
		
		* *degrees* - Degrees as a string, int or float
		* *minutes* - Minutes as a string, int or float
		* *seconds* - Seconds as a string, int or float
		
	*Returns:*
		
		* float - represents decimal degrees
	
	"""

	# If degrees are a string, convert to float
	if isinstance(degrees, str):
		try:
			degrees = float(degrees)
		except:
			degrees = 0
	
	# If minutes are a string, convert to float
	if isinstance(minutes, str):
		try:
			minutes = float(minutes)
		except:
			minutes = 0
	
	# If seconds are a string, convert to float
	if isinstance(seconds, str):
		try:
			seconds = float(seconds)
		except:
			seconds = 0	
	
	return degrees + minutes/60.0 + seconds/3600.0

