import pathlib
import requests
from bs4 import BeautifulSoup
import atcoder_client
import time
import datetime
ATCODER_TASK_URL = 'https://atcoder.jp/contests/{contest}/tasks/{task}'
ATCODER_TASKS_URL = 'https://atcoder.jp/contests/{contest}/tasks/'
ATCODER_CONTEST_URL = 'https://atcoder.jp/contests/{contest}/'
RETRY_COUNT = 3
RETRY_INTERVAL = 1
JST = datetime.timezone(datetime.timedelta(hours=9), name='JST')

class Contest:
    def __init__(self, name):
        self.name=name
    def exists(self):
        retry = RETRY_COUNT
        atccli = atcoder_client.get_client()
        while retry:
            retry -= 1
            r = atccli.request(ATCODER_CONTEST_URL.format(contest=self.name))
            if r.status_code == requests.codes.ok:
                break
            else:
                st=r.status_code
        else:
            return False
        soup = BeautifulSoup(r.text, 'lxml')
        start_time_url = soup.find('small', class_='contest-duration').find('a').get('href')

        found_pos=start_time_url.find('?iso=')
        if found_pos != -1:
            start_time_str = start_time_url[found_pos+5 : found_pos+18]
            start_time=datetime.datetime.strptime(start_time_str, '%Y%m%dT%H%M').replace(tzinfo=JST)
            if start_time > datetime.datetime.now(JST):
                remain_time = (start_time - datetime.datetime.now(JST))
                print('the contest will start in', remain_time)
                print('waiting for contest start.')
                print('terminate to abort')
                time.sleep(remain_time.total_seconds() + 1)
        return True
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

                with open('testcases/'+self.contest.name+'/'+self.taskname+'.html', 'w') as f:
                    f.write(r.text)
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
