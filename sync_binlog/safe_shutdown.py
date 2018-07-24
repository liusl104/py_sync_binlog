# encoding=utf8

import socket
import os
import sys
from sync_binlog.output_log import logger as loging
from sync_binlog.update_post import update_datetime
from sync_binlog.batch_analysis_insert_sql import analysis_sql
from sync_conf import write_db
from sync_binlog.analysis_binlog_main import mysql

hostname = socket.gethostname()


def create_pid_file():
    pid = open('%s.pid' % hostname, 'w')
    pid.close()


def safety_shutdown(obj=analysis_sql):
    if not os.path.exists('%s.pid' % hostname):
        print("%s未能检测到%s.pid，系统正常退出" % (update_datetime(), hostname))
        if len(obj) > 0:
            if write_db:
                loging.debug("Query : %s " % obj)
                mysql.my_sql(obj)
                return False
        loging.info("未能检测到%s.pid, System shutdown" % hostname)
        sys.exit()
