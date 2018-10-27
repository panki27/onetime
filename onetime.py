#!/usr/bin/env python3
#import cgi
import random
KEY_LENGTH = 16 # 16 char length

def get_rng_parameters():
    state = open('state', 'r').read()
    seed = open('seed', 'rb').read()
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
    seed, state = get_rng_parameters()
    setup_csprng(seed, state)

    for i in range(100):
        print(generate_key())
        state += 1
        setup_csprng(seed, state)

if __name__ == '__main__':
    main()