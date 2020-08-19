# -*- coding: utf-8 -*-
import snippet_parser
import subprocess
import os

BITS_STDCXX_PATH = '/usr/include/c++/10.1.0/x86_64-pc-linux-gnu/bits/stdc++.h'

def init():
    snippet_parser.save_from_snippet_texts([
        'a.cpp',
        'b.cpp',
        'c.cpp',
        'd.cpp',
        'e.cpp',
        'f.cpp',
    ])
    compile_bits_stdcxx()

def compile_bits_stdcxx():
    print("compiling bits/stdc++.h.gch")
    try:
        os.mkdir('bits')
    except FileExistsError:
        pass
    subprocess.run(['g++', BITS_STDCXX_PATH, '-o', 'bits/stdc++.h.gch'])
