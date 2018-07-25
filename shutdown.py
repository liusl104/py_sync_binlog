# encoding=utf8

import os
import socket
from sync_binlog.output_log import logger as loging
import time
import sys
from sync_binlog.update_post import update_datetime

try:
    import psutil
except ImportError:
    print("psutil 模块不存在,请使用 pip install psutil 安装")
    sys.exit(0)


def shutdown_program():
    hostname = socket.gethostname()
    if os.path.exists('%s.pid' % hostname):
        os.remove('%s.pid' % hostname)
        loging.info("Starting shutdown...")
    else:
        print('%s%s.pid 文件不存在' % (update_datetime(), hostname))
        loging.warn('%s.pid 文件不存在' % hostname)


def judgeprocess(processname):
    pl = psutil.pids()
    for pid in pl:
        try:
            cmdlines = psutil.Process(pid).cmdline()
        except Exception:
            continue
        for cmdline in cmdlines:
            if processname in cmdline:
                return pid

    else:
        return False
# Shutdown complete


if __name__ == "__main__":
    print("%sStarting shutdown..." % update_datetime())
    shutdown_program()
    time.sleep(3)
    process_id = judgeprocess('startup.py')
    if process_id is not False:
        psutil.Process(process_id).kill()
        print("%sShutdown complete" % update_datetime())
        loging.info("Shutdown complete")
    else:
        print("%s程序自动关闭，请手工检查" % update_datetime())
        loging.info("程序自动关闭，请手工检查")
