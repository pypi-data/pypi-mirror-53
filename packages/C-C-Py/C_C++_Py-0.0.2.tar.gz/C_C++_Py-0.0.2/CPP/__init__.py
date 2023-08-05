try:
    f = open('settings.h','r')
except Exception:
    f = open('settings.h','w')
    f.write('C:0')
for line in f:
    #print(line)
    if line.startswith('C:') and line.endswith('0'):
        
        try:
            from CPP import _for
            print('impoting cpp.for')
        except Exception as e:
             print('warning cpp.for could not be imported! reason: ' + str(e))
def package_vector():
    try:
        from CPP import vector
    except Exception as e:
        print(e)
def package_speech():
    try:
        from CPP import speech
    except Exception as e:
        print(e)
def package_network_tools():
    try:
        from CPP import Network
    except Exception as e:
        print(e)
def package_server_tools():
    try:
        from CPP import Server
    except Exception as e:
        print(e)
def package_binary():
    try:
        from CPP import binary_lib
    except Exception as e:
        print(e)
def package_app_tools():
    try:
        from CPP import app
    except Exception as e:
        print(e)
f.close()
del f
def RUN(app):
    app()
class TERMINAL:
    def INPUT(space='|',SAVE=False,dump=None):
        f = input('|')
        if SAVE == True:
            dump = f
        return f
    def ACTIVATE(ver=0.1):
        VER = 0.1
        if ver > VER:
            print('that version doesnt exist!')
        else:
            print('type: "shutdown" to exit..')
            while True:
                s = TERMINAL.INPUT()
                if s.startswith('-pyexec'):
                    h = ''
                    while h != 'shutdown':
                        h = input('|-->] ')
                        if h.startswith('$def'):
                            
                            exec(open(h.split(':')[-1],'r').read())
                        else:
                            try:
                                if h == 'help()':
                                    print('this terminal "pyexecutor" works simmilar to the python shell ide! to define a function create a file with the function code and ender\n"$def:<filename/location>" to import the file to define!')
                                else:
                                    exec(h)
                            except Exception as e:
                                print(e)
                            
                    exec(s.split('-pyexec')[-1])
                if s == "{":
                    s = TERMINAL.INPUT(space='    ')
                    if s == '   ':
                        if TERMINAL.INPUT() == '    ':
                            pass
                        
                    
                if 'shutdown' in TERMINAL.INPUT():
                    break
        
def setting(name,value):
    f = open('settings.h','r')
    i = f.read()
    #print(i)
    i = i.replace(name,name.split(':')[0] + ':' + str(value))
    #print(i)
    
def SHUTDOWN_SOURCE():
    quit()
def SHUTDOWN_SCRIPT():
    exit()
