#!/usr/bin/env python3
from __future__ import print_function
from seedcount.mnemonic import mnemonic
#from mnemonic import Mnemonic


import json
import sys
from binascii import hexlify, unhexlify
from random import choice


def b2h(b):
    h = hexlify(b)
    return h if sys.version < '3' else h.decode('utf8')

lang="english"

mnemo = mnemonic.Mnemonic(lang)

def process(data):
    code = mnemo.to_mnemonic(unhexlify(data))
    return code

def generate():
        data = ''.join(chr(choice(range(0, 256))) for _ in range(32))
        if sys.version >= '3':
            data = data.encode('latin1')
        return process(b2h(data))

def generate_more(n):
    return [generate() for i in range(0,n)]

if __name__ == '__main__':

   print(generate_more(2))

