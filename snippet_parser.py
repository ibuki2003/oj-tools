# -*- coding: utf-8 -*-

import json
from jsoncomment import JsonComment

SNIPPETS_PATH = '/home/fuwa/.config/Code/User/snippets/cpp.json'
SNIPPET_KEY = '競プロテンプレ'

def get_snippet_text():
    parser = JsonComment(json)
    with open(SNIPPETS_PATH) as f:
        data = parser.load(f)
        body = '\n'.join(data[SNIPPET_KEY]['body'])
        body = body.replace('$0', '')
        return body

def save_from_snippet_texts(filenames):
    body = get_snippet_text()
    for fn in filenames:
        with open(fn, 'w') as f:
            f.write(body)
