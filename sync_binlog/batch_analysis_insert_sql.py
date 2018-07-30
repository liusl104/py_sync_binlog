# encoding=utf8

from sync_binlog.analysis_rows import insert_key_values
from sync_binlog.output_log import logger as loging
from sync_conf import write_db, batch_number
from sync_binlog.update_post import update_binlog_pos
from sync_binlog.global_transaction_insert_batch_id import get_auto_uuid_cnf
from sync_binlog.send_binlog import Mysql
import datetime
from decimal import Decimal

mysql = Mysql("/*!40014 SET FOREIGN_KEY_CHECKS=0*/")


class batch_analysis_sql():
    def __init__(self):
        self.analysis_sql = ''
        self.count_num = 0
        self.db_table_map = ''
        self.batch_number_count = 0
        self.log_position = ''
        self.server_uuid = get_auto_uuid_cnf()

    def cntrast_insert_class_tab(self, info, table_map):
        class_type = info['class']
        if class_type == "WriteRowsEvent" and self.count_num > 0 and table_map != self.db_table_map:
            self.db_table_map = table_map
            self.analysis_sql = self.analysis_sql[:self.analysis_sql.rindex(',')]
            if write_db:
                mysql.my_sql(self.analysis_sql)
                loging.debug("Query : %s " % self.analysis_sql)
                loging.info("批量解析insert id : %s:%d-(%s-%s) 提交处理" % (self.server_uuid, self.batch_number_count,
                                                                    self.log_position, str(info["Log position"])))
                self.batch_number_count += 1
                self.analysis_sql = ''
                self.count_num = 0
                return False
        elif class_type in ("UpdateRowsEvent", "DeleteRowsEvent"):
            if len(self.analysis_sql) == 0:
                return True
            self.analysis_sql = self.analysis_sql[:self.analysis_sql.rindex(',')]
            if write_db:
                loging.debug("Query : %s " % self.analysis_sql)
                mysql.my_sql(self.analysis_sql)
                loging.info("批量解析insert id : %s:%d-(%s-%s) 提交处理" % (self.server_uuid, self.batch_number_count,
                                                                    self.log_position, str(info["Log position"])))
                self.batch_number_count += 1
                self.analysis_sql = ''
                self.count_num = 0
                return False
        elif class_type == "QueryEvent":
            row_values = eval(info["row_values"])
            if row_values["Query"] != "BEGIN" and self.count_num > 0:
                self.analysis_sql = self.analysis_sql[:self.analysis_sql.rindex(',')]
                if write_db:
                    loging.debug("Query : %s " % self.analysis_sql)
                    mysql.my_sql(self.analysis_sql)
                    loging.info("批量解析insert id : %s:%d-(%s-%s) 提交处理" % (self.server_uuid, self.batch_number_count,
                                                                        self.log_position, str(info["Log position"])))
                    self.batch_number_count += 1
                    self.analysis_sql = ''
                    self.count_num = 0
                    return False

    def batch_analysis_insert_binlog(self, info, init_binlog_file_name, table_map):
        analysis_sqls = ''
        values = eval(info["row_values"])["Values"]
        if self.count_num == 0:
            self.log_position = str(info["Log position"])
        else:
            self.log_position = str(info["Log position"])
        if len(values) > 1:
            rows = insert_key_values(values[0]["values"], table_map)
            if len(self.analysis_sql) == 0:
                init_sql = "insert into %s (%s) VALUES \n" % (table_map, rows[0])
            else:
                init_sql = ''
            for v in values:
                rows = insert_key_values(v["values"], table_map)
                sql_values = "(%s), \n" % (rows[1].replace("'None'", 'Null'))
                analysis_sqls += sql_values
                self.count_num += 1
            read_time_position = str(info["Log position"])
            loging.debug("解析日志时间 : %s Position id %s" % (info["Date"], read_time_position))
            loging.info("批量解析insert id : %s:%d-%s" % (self.server_uuid, self.batch_number_count, read_time_position))
            self.analysis_sql += init_sql + analysis_sqls
            # loging.debug("Query : %s " % analysis_sql)
            self.db_table_map = table_map
            # if write_db is True:
            #    mysql.my_sql(analysis_sql)
            update_binlog_pos(pos_id=str(info["Log position"]), binlog_file=init_binlog_file_name)
        else:
            values = eval(info["row_values"])["Values"][0]["values"]
            rows = insert_key_values(values, table_map)
            self.count_num += 1
            if len(self.analysis_sql) == 0:
                self.analysis_sql = "insert into %s (%s) VALUES (%s)," % (table_map, rows[0], rows[1].replace("'None'", 'Null'))
            else:
                self.analysis_sql += "(%s), \n" % rows[1].replace("'None'", 'Null')
            read_time_position = str(info["Log position"])
            loging.debug("解析日志时间 : %s Position id %s " % (info["Date"], read_time_position))
            loging.info("批量解析insert id : %s:%d-%s" % (self.server_uuid, self.batch_number_count, read_time_position))
            # loging.debug("Query : %s " % analysis_sql)
            self.db_table_map = table_map
            # if write_db is True:
            #    mysql.my_sql(analysis_sql)
            update_binlog_pos(pos_id=str(info["Log position"]), binlog_file=init_binlog_file_name)
        if write_db is True and self.count_num >= batch_number:
            self.analysis_sql = self.analysis_sql[:self.analysis_sql.rindex(',')]
            loging.debug("Query : %s " % self.analysis_sql)
            mysql.my_sql(self.analysis_sql)
            loging.info("批量解析insert id : %s:%d-(%s-%s) 提交处理" % (self.server_uuid, self.batch_number_count,
                                                                self.log_position, str(info["Log position"])))
            self.batch_number_count += 1
            self.analysis_sql = ''
            self.count_num = 0
        return self.count_num
