#!/usr/bin/env python3
#import cgi
import random
KEY_LENGTH = 16 # 16 char length
ABS_PATH = ''#'/storage/emulated/0/qpython/scripts3/'

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


def generate_key():
    import string
    chars = string.ascii_letters + string.digits
    return ''.join(random.choice(chars) for i in range(KEY_LENGTH))

def main():
    files_check()
    seed, state = get_rng_parameters()
    #setup_csprng(seed, state)
    storageFile = 'keystore'
    keyCount = len(open(storageFile, 'r').readlines())
    newKeys = ''
    needToGenerate = 10-keyCount > 0
    if needToGenerate:
        print('Generating {} new keys.'.format(10-keyCount))
        for k in range(keyCount, 10):
            state += 1
            setup_csprng(seed, state)
            newKeys += generate_key() + '\n'
        open(ABS_PATH + 'keystore', 'a').write(newKeys)
if __name__ == '__main__':
    main()