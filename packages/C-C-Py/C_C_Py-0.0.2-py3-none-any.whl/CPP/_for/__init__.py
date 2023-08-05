def _for_(min=0,max=0,functions=[]):
    for x in range(min,max):
        for i in functions:
            que_funct(i)
            processes.function()
class processes:
    functions = []
    def __init__(self,funct):
        function = funct
        processes.functions.append(self)
    
        

def que_funct(function):
    '''do not call function in execute_function values'''
    processes.function = function
def kick_funct(function):
    del function
        
