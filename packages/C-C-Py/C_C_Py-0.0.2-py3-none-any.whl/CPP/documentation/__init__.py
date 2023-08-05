def findfor(str):
    if 'CPP.package' in str:
        print('''
CPP.package is used for importing different CPP librarys heres a list of current
modules:

CPP.package_binary() : imports binary library
CPP.package_vector() : imports vectors!
CPP.package_speech() : imports speech library :) enables speaking  speaking through console!! \n requires gTTS  package
''')
    if str.startswith('CPP.binary_lib'):
        if str.endswith('.encrypt()'):
            print('CPP.binary_lib.encrypt() : encrypts a simple text string!')
            print('Example: CPP.binary_lib.encrypt("hello")')
            print('output/returned value: 8*][2@')
        if str.endswith('decrypt()'):
            print('decrypts encrypted string objects(currently bugged object information may be lost or damaged on decryption)')
        else:
            print(' a cpp class for encryption,data converting and more!')
        
def help():
    print('''
welcome to the C-C-py documentation!!!
enter a function name to get started!
we show examples here on functions and more!
type "exit" to quit
how to search:
<doc> CPP.package
(prints how to import packages)
''')
    s = ''
    while s != 'exit':
        s = input('<doc>')
        findfor(s)
