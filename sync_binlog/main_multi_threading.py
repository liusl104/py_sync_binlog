# encoding=utf8

from multiprocessing import Pool
import os, time, random, sys
from sync_conf import databases
from sync_binlog.safe_shutdown import create_pid_file
from sync_binlog.analysis_binlogs import main_binlog


def long_time_task(name):
    if name is None:
        print('Run task %s (%s)...' % ("all databases", os.getpid()))
    else:
        print('Run task %s (%s)...' % (name, os.getpid()))
    start = time.time()
    try:
        main_binlog(name, server_id=random.randint(10000, 90000))
    except:
        sys.exit()
    end = time.time()
    print('Task %s runs %0.2f seconds.' % (name, (end - start)))


def multi_main():
    create_pid_file()
    print('Parent process %s.' % os.getpid())
    if databases is None:
        process = Pool(1)
        process.apply_async(long_time_task, args=(databases,))
        process.join()

    else:
        database = databases
        process = Pool(len(database))
        for i in database:
            process.apply_async(long_time_task, args=(i,))
        print('Waiting for all subprocesses done...')
        process.join()
    print('All subprocesses done.')



