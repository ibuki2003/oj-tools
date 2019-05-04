import pathlib
import requests
from bs4 import BeautifulSoup
import atcoder_client
import time
ATCODER_TASK_URL = 'https://atcoder.jp/contests/{contest}/tasks/{task}'
ATCODER_TASKS_URL = 'https://atcoder.jp/contests/{contest}/tasks/'
RETRY_COUNT = 3
RETRY_INTERVAL = 1

class Contest:
    def __init__(self, name):
        self.name=name
    def get_all_tasks(self):
        retry = RETRY_COUNT
        atccli = atcoder_client.get_client()
        while retry:
            retry -= 1
            r = atccli.request(ATCODER_TASKS_URL.format(contest=self.name))
            if r.status_code == requests.codes.ok:
                break
            else:
                st=r.status_code
        else:
            raise Exception('Failed to get task list({})'.format(st))
        soup = BeautifulSoup(r.text, 'lxml')
        for row in soup.find('tbody').find_all('tr'):
            link = row.find('td').find('a')
            yield Task(self, link.get('href').split('/')[-1])
    def get_nth_task(self, n):
        return self.get_all_tasks()[n]

class Task:
    def __init__(self, *taskid):
        print(taskid)
        if len(taskid)==2:
            self.contest,self.taskname=taskid
            if not isinstance(self.contest, Contest):
                self.contest=Contest(self.contest)
            return
        taskid=taskid[0]
        if '_' in taskid: # task name contains contest name
            self.contest = taskid.rsplit('_',1)[0].replace('_','-')
            self.taskname=taskid
        else: # search gotten
            for d in pathlib.Path('testcases').glob('*/*'):
                if d.is_dir() and (d.name == taskid or d.name.rsplit('_',1)[-1] == taskid):
                    self.contest, self.taskname = str(d).split('/')[1:]
                    break
            else:
                raise Exception('Task not found.')
        self.contest=Contest(self.contest)
    def get_dir(self):
        return pathlib.Path('testcases/'+self.contest.name+'/'+self.taskname)

    def get(self):
        retry = RETRY_COUNT
        atccli = atcoder_client.get_client()
        while True:
            print('Getting task', self.contest.name, '/', self.taskname, '...', end='', flush=True)
            r = atccli.request(ATCODER_TASK_URL.format(contest=self.contest.name, task=self.taskname))
            if r.status_code == requests.codes.ok:
                print('OK')
                soup=BeautifulSoup(r.text, 'lxml')
                (self.get_dir()/'in').mkdir(parents=True, exist_ok=True)
                (self.get_dir()/'out').mkdir(parents=True, exist_ok=True)

                in_cnt = 1
                out_cnt = 1

                for h3 in soup.find_all('h3'):
                    if '力例' in h3.text:
                        nxt=h3
                        while nxt.name != 'pre':
                            nxt = nxt.next
                        text = nxt.text
                        text = '\n'.join(filter(lambda x: x.strip(), map(lambda x: x.strip(), text.split('\n'))))
                        #print(h3.text, '=====')
                        #print(text)

                    if '入力例' in h3.text:
                        with open('testcases/' + self.contest.name + '/' + self.taskname + '/in/' + str(in_cnt) + '.txt', 'w') as f:
                            f.write(text)
                        in_cnt += 1
                    elif '出力例' in h3.text:
                        with open('testcases/' + self.contest.name + '/' + self.taskname + '/out/' + str(out_cnt) + '.txt', 'w') as f:
                            f.write(text)
                        out_cnt += 1
                return
            print('Failed(',r.status_code,')')
            retry -= 1
            if(retry<=0):
                raise Exception('Failed to get task')
            time.sleep(1)
