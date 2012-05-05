''' Error Catching Experiments
'''


import os

###############################
# Using Finally without except
try:
    try:
        os.chdir('fail')
    finally:
        
        print 'This finally block is executed before passing on the exception'
        
    os.chdir("fail") # never executed
    
except Exception, e:
    print "As expected, a 'finally' without an 'except' does not stop the propagation of the exception.\n"
    
###############################################
# Standare error handling
class ATtILA2Exception(Exception):
    """ Custom Exception """
    
errorLookup = {'99999': 'There was an unexpected error'}
    
def printError(e):
    
    msg = str(e)
    
    # Known Error with a custom message based on context
    if isinstance(e, ATtILA2Exception):
        print msg

    # Known Error with a generic message
    else:
        for key in errorLookup:
            if key in msg:
                print errorLookup[key]
                return
    #Unknown error
    print msg

class constants:
    standardPrefix = 'ERROR ATtILA2-'
    id10tError = standardPrefix + "000001:  Custom Message"

try:
    try:
        os.chdir('fail')
    
    except:
        raise ATtILA2Exception(constants.id10tError)
        
    finally:
        print "You can do clean up here"
        
except Exception, e:
    

    

    