# -*- coding: utf-8 -*-
import snippet_parser
import subprocess
import os

def init():
    snippet_parser.save_from_snippet_texts([
        'a.cpp',
        'b.cpp',
        'c.cpp',
        'd.cpp',
        'e.cpp',
        'f.cpp',
    ])
