import pickle
def INT_BIN(int):
    return bin(int)
def BIN_INT(bin):
    return int(bin)
def FLOAT_BIN(float):
    return bin(float)
def BIN_FLOAT(bin):
    return float(bin)
DKEY = ['a','b','c','d','e','f','g','h','i','j','k','l'\
        ,'m','n','o','p','q','r','s','t','u','v','w','x','y','z',' ']
KEY = {
    ' ':'&',
'a':'1',
'b':'2',
'c':'3',
'd':'4',
'e':'5',
'f':'6',
'g':'7',
'h':'?',
'i':'8',
'j':'9',
'k':'^',
'l':'/',
'm':'Ϗ',
'n':'[',
'o':'-',
'p':',',
'q':'=',
'r':'+',
's':'*',
't':'@',
'u':'ʨ',
'v':'~',
'w':'`',
'x':'#',
'y':'$',
'z':'%'
    }
sKEY ='''
a:1
b:2
c:3
d:4
e:5
f:6
g:7
h:7
i:8
j:9
k:/p
l:/.
m:k]
n:[
o:e-
p:,
q:=
r:+
s:*
t:@
u:!
v:~
w:`
x:#
y:$
z:%
'''
def encrypt(str,out=False):
    f = ''
    for line in str:
        #print(line)
        try:
            line = KEY[line]
            f += line
            #f.append(line)
        except Exception as e:
            f += line
            if not out:
                print(e)
             
##    for line in str:
##        for letter in str:
##            print(letter)
##            for lineh in KEY:
##                try:
##                    
##                    
##                    line = lineh[letter]
##                    print('matched')
##                except Exception as e:
##                    print(e)
##
####                print(lineh)
####                if letter.startswith(lineh):
####                    line.replace(letter,lineh.split(':')[-1])
        
    return f
def GET_RAW(str):
    '''bytes only'''
    return pickle.dumps(str)
def GET_LOAD(str):
    '''bytes only'''
    return pickle.loads(str)
def decrypt(str):
    s = ''
    for line in str:
        try:
            for x in DKEY:
                if line == KEY[x]:
                    s += x
        except Exception:
            s += line
    return s
            
