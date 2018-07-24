# encoding=utf8

import logging  # 引入logging模块
from logging.handlers import TimedRotatingFileHandler
from sync_conf import log_bese_path


# 日志


logfile = log_bese_path + '/logs/' + 'binlog_sync.log'
logger = logging.getLogger()
logger.setLevel(logging.INFO)
# 按日分割日志，日志保留7份
fh = TimedRotatingFileHandler(logfile, when='D', interval=1, backupCount=7)
# datefmt = '%Y-%m-%d %H:%M:%S'
format_str = "%(asctime)s - %(filename)s[line:%(lineno)d] - %(levelname)s: %(message)s"
formatter = logging.Formatter(format_str, datefmt=None)
fh.setFormatter(formatter)
logger.addHandler(fh)

