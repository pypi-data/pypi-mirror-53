class data_type:
    class int:
        def __init__(self,space,value=None):
            self.vector = []
            for x in range(0,space + 1):
                if value == None:
                    self.vector.append(x)
                else:
                    self.vector.append(value)
        def popback(self,num=1):
            for x in range(0,num):
                self.vector.pop(self.vector.index(self.vector[-1]))
        def size(self):
            return(len(self.vector))
        def pushback(self,data):
            temp = self.vector
            self.vector = []
            self.vector.append(int(data))
            for x in temp:
                #print(x)
                self.vector.append(x)
            return self.vector
        def redefine(self,element,data):
            self.vector[element] = int(data)
        def Vector(self):
            return self.vector
        
    class string:
        def __init__(self,space,value=None):
            self.vector = []
            for x in range(0,space):
                if value == None:
                    self.vector.append(str(x))
                else:
                    self.vector.append(value)
        def popback(self,num=1):
            for x in range(0,num):
                self.vector.pop(self.vector.index(self.vector[-1]))
        def size(self):
            return(len(self.vector))
        def pushback(self,data):
            temp = self.vector
            self.vector = []
            self.vector.append(str(data))
            for x in temp:
                #print(x)
                self.vector.append(x)
            return self.vector
        def redefine(self,element,data):
            self.vector[element] = str(data)
    class float:
        def __init__(self,space,value=None):
            self.vector = []
            for x in range(0,space + 1):
                if value == None:
                    self.vector.append(float(x))
                else:
                    self.vector.append(value)
        def popback(self,num=1):
            for x in range(0,num):
                self.vector.pop(self.vector.index(self.vector[-1]))
        def size(self):
            return(len(self.vector))
        def pushback(self,data):
            temp = self.vector
            self.vector = []
            self.vector.append(float(data))
            for x in temp:
                #print(x)
                self.vector.append(x)
            return self.vector
        def redefine(self,element,data):
            self.vector[element] = float(data)
    class char:
        def __init__(self,space,value=None):
            self.vector = []
            for x in range(0,space):
                if value == '0':
                    self.vector.append(float(x))
                else:
                    self.vector.append(chr(value + x))
##                for x in self.vector:
##                    x = chr(x)
        
                
        def popback(self,num=1):
            for x in range(0,num):
                self.vector.pop(self.vector.index(self.vector[-1]))
        def size(self):
            return(len(self.vector))
        def pushback(self,data):
            temp = self.vector
            self.vector = []
            self.vector.append(chr(data))
            for x in temp:
                #print(x)
                self.vector.append(x)
            return self.vector
        def redefine(self,element,data):
            self.vector[element] = chr(data)
    class objclass:
        def __init__(self,obj_class,space):
            self.vector = []
            for x in range(0,space):
               self.vector.append(obj_class)
        
                
        def popback(self,num=1):
            for x in range(0,num):
                self.vector.pop(self.vector.index(self.vector[-1]))
        def size(self):
            return(len(self.vector))
        def pushback(self,data):
            temp = self.vector
            self.vector = []
            self.vector.append(data)
            for x in temp:
                #print(x)
                self.vector.append(x)
            return self.vector
        def redefine(self,element,data):
            self.vector[element] = data
            
##class vect:
##    class make:
##        def int(size,variable):
##            variable = []
##            for x in range(0,size):
##                variable.append(x)        
