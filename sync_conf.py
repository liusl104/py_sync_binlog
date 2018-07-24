# encoding=utf8

# 链接数据库的参数 因为 pymysqlreplication 底层使用的是 python-mysql

import os
from random import randint


# binlog 检查点配置
binlogfile_Label_file = "%s/%s" % (os.getcwd(), "checkpoint")

# target server db config

target_ip = '10.20.10.1'
target_port = 3306
target_user = 'slave'
target_passwd = '6852639a881f5569731ca40331ada083'


# MySQL服务id

mysql_settings = {
    'host': '10.20.10.2',
    'port': 3306,
    'user': 'slave',
    'passwd': '6852639a881f5569731ca40331ada083'
}

server_id = randint(10000, 50000)
blocking = True
resume_stream = True
only_events = None
ignored_events = None
auto_position = None
ignored_tables = None
ignored_schemas = None
only_schemas = ['test']
only_tables = None

"""  Attributes:
            ctl_connection_settings: Connection settings for cluster holding schema information
            resume_stream: Start for event from position or the latest event of
                           binlog or from older available event
            blocking: Read on stream is blocking
            only_events: Array of allowed events
            ignored_events: Array of ignored events
            log_file: Set replication start log file
            log_pos: Set replication start log pos (resume_stream should be true)
            auto_position: Use master_auto_position gtid to set position
            only_tables: An array with the tables you want to watch (only works
                         in binlog_format ROW)
            ignored_tables: An array with the tables you want to skip
            only_schemas: An array with the schemas you want to watch
            ignored_schemas: An array with the schemas you want to skip
            freeze_schema: If true do not support ALTER TABLE. It's faster.
            skip_to_timestamp: Ignore all events until reaching specified timestamp.
            report_slave: Report slave in SHOW SLAVE HOSTS.
            slave_uuid: Report slave_uuid in SHOW SLAVE HOSTS.
            fail_on_table_metadata_unavailable: Should raise exception if we can't get
                                                table information on row_events
            slave_heartbeat: (seconds) Should master actively send heartbeat on
                             connection. This also reduces traffic in GTID replication
                             on replication resumption (in case many event to skip in
                             binlog). See MASTER_HEARTBEAT_PERIOD in mysql documentation
                             for semantics
        """
# log
log_bese_path = os.getcwd()

# 设置根据库多进程同步,需要指定schemas,几个库就几个进程
databases = None

# 设置合并数据库,注意区分大小写
merge_db_table = False
merge_table_rule = {"database": [{"test": "test"}],
                    "table_map": [{"tb1": "tb"}, {"tb2": "tb"}, {"tb3": "tb"}]}
# 设置是否写库
write_db = True
write_ddl = False

# 设置insert批次大小,需要根据数据量大小设定，不宜太大，建议控制在2000以内,如果可以确定每行数据比较小可以适量增加
batch_number = 100

# 设置跳过错误代码:(默认不跳过 None), 必须是数组
# 1062 重复主键  HA_ERR_FOUND_DUPP_KEY
# 1032 无匹配数据 HA_ERR_KEY_NOT_FOUND
# all 全部跳过

skip_err_code = None

# 加密字符串标识
encryption_strings = 'abcd'
# 123456789abcdefg
# 123456789abcdefg
# key和iv值可以不一样
key = "f955a02d44e9c05abfb0d1b82e0e107e"
iv = "9540759180d6135144782770a8d81f9c"

# 加密表和列

encryption_column = False
# 库表列统一小写,如果MySQL中有大写，则区分大小写，key是表名，value是列名用逗号隔开
encryption_db_column = {"database": ["test"],"table_column_map": {"tb1": "cr_no, passwd"}}

