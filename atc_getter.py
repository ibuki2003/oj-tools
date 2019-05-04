# -*- coding: utf-8 -*-
import requests
from bs4 import BeautifulSoup
import time
import os
import atc_task
import atcoder_client

def get(params):
    atcoder_client.get_client()
    if len(params)==1:
        contest=atc_task.Contest(params[0])
        if contest.exists():
            for task in contest.get_all_tasks():
                task.get()
        return

    task=atc_task.Task(*params)
    task.get()
