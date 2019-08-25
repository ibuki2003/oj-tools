import os
import glob
import atc_task
import atc_getter
import pathlib
import subprocess
import time
import color

TL = 2  # sec

EXEC_CMD={
    'bin': './{}',
    'python': 'python {}.py',
    'ruby': 'ruby {}.rb'
}

def test(args):
    # arg type
    # - problem
    # - problem, type

    if len(args) == 0:
        raise Exception('Too few arguments')

    if args[-1] not in EXEC_CMD:
        args.append('bin') # exec mode

    task = atc_task.Task(*args[:-1])

    exec_mode = args[-1].lower()

    cmd=EXEC_CMD[exec_mode].format(args[-2])

    taskdir = task.get_dir()

    if not taskdir.exists(): # task is not gotten yet
        print('getting testcases')
        task.get()

    allAC=True
    res_all={}
    for testcase_in in sorted(taskdir.glob('in/*')):
        testcase_out = taskdir / 'out' / testcase_in.name
        print(color.CYAN, 'Running testcase ', testcase_in.name, color.END)
        print('stderr===========', flush=True)
        res = judge(cmd,
                    str(testcase_in),
                    str(testcase_out))
        print('=================', flush=True)
        res_all[testcase_in.name]=res
        if res[0]!='AC':
            allAC=False
    for res in res_all:
        print((color.GREEN if res_all[res][0]=='AC' else color.RED),
            res,'\t:', res_all[res][0], res_all[res][1], 'ms', color.END)
    print('all AC\t:', (color.GREEN if allAC else color.RED), allAC, color.END)


def judge(cmd, in_file, out_file):
    try:
        with open(in_file, 'r') as input_file:
            starttime = time.time()
            p = subprocess.Popen(cmd, shell=True,
                                stdin=input_file,
                                stdout=subprocess.PIPE)
            out = p.communicate(timeout=TL)[0]
            exectime = int((time.time() - starttime) * 1000)
        if p.returncode != 0:
            return ("RE", None)
    except subprocess.TimeoutExpired:
        p.kill()
        return ("TLE", None)
    except subprocess.CalledProcessError:
        return ("RE", None)

    # Execute OK
    with open(out_file, 'r') as ansfile:
        anslist = ansfile.read().split()
    outlist = out.decode('utf-8').split()

    if len(outlist) != len(anslist):
        return ("WA", exectime)
    for i in range(len(outlist)):
        if(outlist[i] != anslist[i]):
            return ("WA", exectime)
    return ("AC", exectime)
