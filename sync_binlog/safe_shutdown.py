# encoding=utf8

import socket
import os
import sys
from sync_binlog.output_log import logger as loging
from sync_binlog.update_post import update_datetime
from sync_conf import write_db
from sync_binlog.analysis_binlog_main import mysql, batch_sql

hostname = socket.gethostname()


def create_pid_file():
    pid = open('%s.pid' % hostname, 'w')
    pid.close()


def safety_shutdown():
    if not os.path.exists('%s.pid' % hostname):
        print("%s未能检测到%s.pid，系统正常退出" % (update_datetime(), hostname))
        obj = batch_sql.analysis_sql
        analysis_sql = obj[:obj.rindex(',')]
        if len(analysis_sql) > 0:
            if write_db:
                loging.debug("Query : %s " % analysis_sql)
                mysql.my_sql(analysis_sql)
        loging.info("未能检测到%s.pid, System shutdown" % hostname)
        sys.exit()
