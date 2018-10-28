#!/usr/bin/env python3
import cgi
import random
KEY_LENGTH = 16 # 16 char length
ABS_PATH = '/onetime/'#'/storage/emulated/0/qpython/scripts3/'
FILE_STORAGE = ABS_PATH + 'files/'

def files_check():
    import os
    keystore = ABS_PATH + 'keystore'
    seed = ABS_PATH + 'seed'
    state = ABS_PATH + 'state'
    if not os.path.isfile(seed):
        import sys
        #print('ERROR: seed missing!')
        sys.exit(1)
    if not os.path.isfile(state):
        #print('state file not found, initializing.')
        open(state, 'wb').write(b'0')
    if not os.path.isfile(keystore):
        #print('keystore not found, creating.')
        open(keystore, 'w').write('')

def get_rng_parameters():
    state = open(ABS_PATH + 'state', 'r').read()
    seed = open(ABS_PATH + 'seed', 'rb').read()
    return seed, int(state)

def setup_csprng(seed, timesRan):
    hashValue = hash(timesRan)
    instanceSeed = int.from_bytes(seed, 'big') ^ hashValue 
    random.seed(instanceSeed)

def populate_keystore(keyCount, state, seed):
    needToGenerate = 10-keyCount > 0
    if needToGenerate:
        newKeys = ''
        for k in range(keyCount, 10):
            state += 1
            setup_csprng(seed, state)
            newKeys += generate_key() + '\n'
        open(ABS_PATH + 'keystore', 'a').write(newKeys)
        open(ABS_PATH + 'state', 'w').write(str(state))

def print_html_head():
    print ("Content-type:text/html\r\n\r\n")
    print ("<html>")
    print ("<head>")
    print ("<title>Download access</title>")
    print ("</head>")
    print ("<body>")
    
def print_html_bottom():
    print ("</body>")
    print ("</html>")
    

def generate_key():
    import string
    chars = string.ascii_letters + string.digits
    return ''.join(random.choice(chars) for i in range(KEY_LENGTH))

def send_download(file):
    from shutil import copyfileobj
    import sys
    print("Content-type: application/octet-stream")
    print("Content-Disposition: attachment; filename=%s" %(file))
    print()
    sys.stdout.flush()
    with open(FILE_STORAGE + file, 'rb') as f:
        copyfileobj(f, sys.stdout.buffer)
    f.close()


def main():
    # begin setup
    files_check()
    seed, state = get_rng_parameters()
    storageFile = ABS_PATH + 'keystore'
    keyCount = len(open(storageFile, 'r').readlines())
    populate_keystore(keyCount, state, seed)
    keys = list(map(str.strip, open(storageFile, 'r').readlines()))
    # setup done

    form = cgi.FieldStorage()
    suppliedKey = form.getvalue('key')
    requestedFile = form.getvalue('file')
    if suppliedKey in keys:
        import os
        if requestedFile != None:
            if '..' not in requesedFile:
                if os.path.isfile(FILE_STORAGE + requestedFile):
                    send_download(requestedFile)
                else:
                    print_html_head()
                    print("<h2>Sorry! The requested file could not be found.</h2>")
                    print_html_bottom()
                keys.remove(suppliedKey)
                open(ABS_PATH + 'keystore', 'w').write('\n'.join(keys) + '\n')
        else:
            print_html_head()
            print("<h2>Get the fuck out.</h2>")
            print_html_bottom()  
    else:
        print_html_head()
        print("<h2>Sorry! The supplied downloadkey is INVALID!</h2>")
        print_html_bottom()

if __name__ == '__main__':
    main()