#!/usr/bin/env python3
import random
KEY_LENGTH = 16 # 16 char length
ABS_PATH = '/storage/emulated/0/qpython/scripts3/'

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
        for k in range(keyCount, 10):
            state += 1
            setup_csprng(seed, state)
            newKeys += generate_key() + '\n'
        open(ABS_PATH + 'keystore', 'a').write(newKeys)
        open(ABS_PATH + 'state', 'w').write(str(state))

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
    keys = list(map(str.strip, open(storageFile, 'r').readlines()))
    # setup done
    filename = input('Filename to download: ')
    print('https://felixpankratz.de/dl.py?key={}&file={}'.format(keys[0], filename))
    keys.remove(keys[0])
    open(ABS_PATH + 'keystore', 'w').write('\n'.join(keys) + '\n')

if __name__ == '__main__':
    main()