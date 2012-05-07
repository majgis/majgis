''' Convert degrees, minutes seconds (DMS) to decimal degrees (DD)

    values are a string in a single cell within an excel spreadsheet (.xlsx
'''


import sys
from openpyxl import load_workbook

def main(argv):
    """ Start of execution"""
    
    filePath = argv[1]
    
    
    
    wb = load_workbook(filePath)
    ws = wb.get_active_sheet()
      
    
    for i, row in enumerate(ws.rows):
        
        #skip first row
        if not i:
            continue
        
        cellValue = row[1].value
        
        if cellValue:
            print i
            latDMS, lonDMS = makeReplacements(cellValue)
            print latDMS
            print lonDMS
            lat = dmsToDecimalDegrees(*latDMS)
            lon = dmsToDecimalDegrees(*lonDMS)
            
            
            row[2].value = latDMS[0]
            row[3].value = latDMS[1]
            row[4].value = latDMS[2]
            row[5].value = lat
            
            row[6].value = lonDMS[0]
            row[7].value = lonDMS[1]
            row[8].value = lonDMS[2]
            row[9].value = -lon
            
            
    wb.save(filePath)

def makeReplacements(value):
    value = value.strip()
    replacements = [(u'\u02da', 'd'), 
                    ('o', 'd'),
                    ('N', ' '),
                    ('M', ' '),
                    ('l', ''),
                    ('*', 'd'),
                    ('w', 'W')]
    
    for find, replace in replacements:
        value = value.replace(find, replace)
    


    split = value.split('-')
    
    if len(split) == 1 or split[1]=='':
        split = value.split('\n')
    if len(split) == 1 or split[1] =='':
        split = value.split('"')
    if len(split) == 1 or split[1]=='':
        split = value.split('W')
    if len(split) == 1 or split[1]=='':
        split = value.split('  ')
    if len(split) == 1 :
        split.append('')
    
    lat = split[0].strip().strip('W').strip()
    lon = split[1].strip().strip('W').strip()
    
    return parseToDMS(lat), parseToDMS(lon)
           
           
def parseToDMS(value):   
           
    dms = []
    split = value.split('d')
    
    if len(split) > 1:

        dms.append(split[0].replace(" ",""))

        split2 = split[1].split("'")
        try:
            dms.append(split2[0])
            
        except:
            dms.append('')
        try:
            dms.append(split2[1])
        except:
            dms.append('')
    
    else:
        split = value.split("'")
        
        if len(split) > 1:
            seconds = split[1].strip().strip('"').strip()
            try:
                degrees,minutes = split[0].split(' ')
            except:
                degrees = ''
                minutes = split[0]
            
            dms = [degrees, minutes, seconds]
        else:
            dms = [value, '', '']
    
    dms[2] = dms[2].strip('"')
        
    return dms
    
    
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
    if isinstance(degrees, str) or isinstance(degrees, unicode):
        try:
            degrees = float(degrees)
        except:
            degrees = 0
    
    # If minutes are a string, convert to float
    if isinstance(minutes, str) or isinstance(minutes, unicode):
        try:
            minutes = float(minutes)
        except:
            minutes = 0
    
    # If seconds are a string, convert to float
    if isinstance(seconds, str) or isinstance(seconds, unicode):
        try:
            seconds = float(seconds)
        except:
            seconds = 0    
    
    return degrees + minutes/60.0 + seconds/3600.0    

   
if __name__ == "__main__":
    
    filePath = "C:\Temp\LatLongCleanup.xlsx"
    sys.argv.append(filePath)    
    main(sys.argv)
    
    
    