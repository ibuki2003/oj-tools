# -*- coding: utf-8 -*-
import requests
from bs4 import BeautifulSoup
import time
import os
import atc_task
import atcoder_client

ATCODER_CONTEST_URL = 'https://atcoder.jp/contests/{contest}/'

def get(params):
    atcoder_client.get_client()
    if len(params)==1 and exists_contest(params[0]):
        for task in atc_task.Contest(params[0]).get_all_tasks():
            task.get()
        return

    task=atc_task.Task(*params)
    task.get()

def exists_contest(contest):
    r = atcoder_client.get_client().request(ATCODER_CONTEST_URL.format(contest=contest))
    return r.status_code == requests.codes.ok
