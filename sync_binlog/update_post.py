# encoding=utf8

from sync_conf import binlogfile_Label_file
import sys
import datetime


def get_new_binlog_pos(filename):
    pos_number = open(filename, 'r', encoding="utf-8")
    pos_number = pos_number.readlines()
    if len(pos_number) == 0:
        sys.exit("读取检查点文件错误")
    binlog, pos = pos_number
    return str(binlog).replace('\n', '').strip(), str(pos).strip()


def update_binlog_pos(pos_id=None, binlog_file=None):
    pos_id = pos_id
    binlog_file = binlog_file
    # 仅打开一次文件
    pos_num = open(binlogfile_Label_file, 'w', encoding='utf-8')
    pos_num.writelines([binlog_file, pos_id])


def update_datetime():
    return '%s - ' % datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f')
