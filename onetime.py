#!/usr/bin/env python3
import cgi
import random
KEY_LENGTH = 16 # 16 char length
ABS_PATH = '/onetime/'#'/storage/emulated/0/qpython/scripts3/'

def files_check():
    import os
    keystore = ABS_PATH + 'keystore'
    seed = ABS_PATH + 'seed'
    state = ABS_PATH + 'state'
    if not os.path.isfile(seed):
        import sys
        print('ERROR: seed missing!')
        sys.exit(1)
    if not os.path.isfile(state):
        print('state file not found, initializing.')
        open(state, 'wb').write(b'0')
    if not os.path.isfile(keystore):
        print('keystore not found, creating.')
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
        #print('Generating {} new keys.'.format(10-keyCount))
        for k in range(keyCount, 10):
            state += 1
            setup_csprng(seed, state)
            newKeys += generate_key() + '\n'
        open(ABS_PATH + 'keystore', 'a').write(newKeys)

def generate_key():
    import string
    chars = string.ascii_letters + string.digits
    return ''.join(random.choice(chars) for i in range(KEY_LENGTH))

def main():
    # begin setup
    files_check()
    seed, state = get_rng_parameters()
    storageFile = ABS_PATH + 'keystore'
    keyCount = len(open(storageFile, 'r').readlines())
    populate_keystore(keyCount, state, seed)
    keys = map(str.strip, open(storageFile, 'r').readlines())
    # setup done
    #print(*keys)

    form = cgi.FieldStorage()
    suppliedKey = form.getvalue('key')
    print ("Content-type:text/html\r\n\r\n")
    print ("<html>")
    print ("<head>")
    print ("<title>Hello - Second CGI Program</title>")
    print ("</head>")
    print ("<body>")
    print ("<h2>Your key: %s</h2>" % (suppliedKey))
    if suppliedKey in keys:
        print("<h1> is VALID!</h1>")
    else:
        print("<h1> is INVALID!</h1>")
    print ("</body>")
    print ("</html>")

if __name__ == '__main__':
    main()