''' Class Properties
'''

class Example(object):
    myattr = ''
    
    def __init__(self):
        self.myattr = property(self.getmyattr)
    
    def getmyattr(self):
        return 'test'
    
    
x = Example()

print x.myattr.