#!python
# -*- coding: utf-8 -*-
import atc_getter
import atc_tester
import atcoder_client
import os

import sys

# Force flush
sys.stdout = os.fdopen(sys.stdout.fileno(), 'w', 1)

if len(sys.argv)<2:
    print('usage: atc (get|test|login) args...')
    exit(-1)

try:
    if sys.argv[1]=='get':
        atc_getter.get(sys.argv[2:])
    elif sys.argv[1]=='test':
        atc_tester.test(sys.argv[2:])
    elif sys.argv[1]=='login':
        atcoder_client.AtCoderClient().login()
    else:
        print('unknown param')
        exit(-1)
except Exception as e:
    raise e
    print('ERROR:',e.args[0])

    exit(-1)
