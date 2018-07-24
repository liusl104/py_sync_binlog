# encoding=utf8

from sync_binlog.safe_shutdown import create_pid_file
from sync_binlog.analysis_binlogs import main_binlog

if __name__ == "__main__":
    create_pid_file()
    main_binlog()
