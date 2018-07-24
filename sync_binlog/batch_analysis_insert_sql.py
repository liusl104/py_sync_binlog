# encoding=utf8

from sync_binlog.analysis_binlog_main import mysql
from sync_binlog.analysis_rows import insert_key_values
from sync_binlog.output_log import logger as loging
from sync_conf import write_db, batch_number
from sync_binlog.update_post import update_binlog_pos
from sync_binlog.global_transaction_insert_batch_id import get_auto_uuid_cnf

analysis_sql = ''
count_num = 0
db_table_map = ''
batch_number_count = 0
log_position = ''
server_uuid = get_auto_uuid_cnf()


def cntrast_insert_class_tab(info, table_map):
    global analysis_sql
    global count_num
    global db_table_map
    global log_position
    global batch_number_count
    class_type = info['class']
    if class_type == "WriteRowsEvent" and count_num > 0 and table_map != db_table_map:
        db_table_map = table_map
        analysis_sql = analysis_sql[:analysis_sql.rindex(',')]
        if write_db:
            mysql.my_sql(analysis_sql)
            loging.debug("Query : %s " % analysis_sql)
            loging.info("批量解析insert id : %s:%d-(%s-%s) 提交处理" % (server_uuid, batch_number_count,
                                                                log_position, str(info["Log position"])))
            batch_number_count += 1
            analysis_sql = ''
            count_num = 0
            return False
    elif class_type in ("UpdateRowsEvent", "DeleteRowsEvent"):
        analysis_sql = analysis_sql[:analysis_sql.rindex(',')]
        if write_db:
            loging.debug("Query : %s " % analysis_sql)
            mysql.my_sql(analysis_sql)
            loging.info("批量解析insert id : %s:%d-(%s-%s) 提交处理" % (server_uuid, batch_number_count,
                                                                log_position, str(info["Log position"])))
            batch_number_count += 1
            analysis_sql = ''
            count_num = 0
            return False
    elif class_type == "QueryEvent":
        row_values = eval(info["row_values"])
        if row_values["Query"] != "BEGIN" and count_num > 0:
            analysis_sql = analysis_sql[:analysis_sql.rindex(',')]
            if write_db:
                loging.debug("Query : %s " % analysis_sql)
                mysql.my_sql(analysis_sql)
                loging.info("批量解析insert id : %s:%d-(%s-%s) 提交处理" % (server_uuid, batch_number_count,
                                                                    log_position, str(info["Log position"])))
                batch_number_count += 1
                analysis_sql = ''
                count_num = 0
                return False


def batch_analysis_insert_binlog(info, init_binlog_file_name, table_map):
    global analysis_sql
    global count_num
    global db_table_map
    global log_position
    global batch_number_count
    analysis_sqls = ''
    values = eval(info["row_values"])["Values"]
    if count_num == 0:
        log_position = str(info["Log position"])
    if len(values) > 1:
        rows = insert_key_values(values[0]["values"], table_map)
        if len(analysis_sql) == 0:
            init_sql = "insert into %s (%s) VALUES \n" % (table_map, rows[0])
        else:
            init_sql = ''
        for v in values:
            rows = insert_key_values(v["values"], table_map)
            sql_values = "(%s), \n" % (rows[1].replace("'None'", 'Null'))
            analysis_sqls += sql_values
            count_num += 1
        loging.info("解析日志时间 : %s Position id %s" % (info["Date"], str(info["Log position"])))
        loging.info("批量解析insert id : %s:%d-%s" % (server_uuid, batch_number_count, str(info["Log position"])))
        analysis_sql += init_sql + analysis_sqls
        # loging.debug("Query : %s " % analysis_sql)
        db_table_map = table_map
        # if write_db is True:
        #    mysql.my_sql(analysis_sql)
        update_binlog_pos(pos_id=str(info["Log position"]), binlog_file=init_binlog_file_name)
    else:
        values = eval(info["row_values"])["Values"][0]["values"]
        rows = insert_key_values(values, table_map)
        count_num += 1
        if len(analysis_sql) == 0:
            analysis_sql = "insert into %s (%s) VALUES (%s)," % (table_map, rows[0], rows[1].replace("'None'", 'Null'))
        else:
            analysis_sql += "(%s), \n" % rows[1].replace("'None'", 'Null')
        loging.info("解析日志时间 : %s Position id %s " % (info["Date"], str(info["Log position"])))
        loging.info("批量解析insert id : %s:%d-%s" % (server_uuid, batch_number_count, str(info["Log position"])))
        # loging.debug("Query : %s " % analysis_sql)
        db_table_map = table_map
        # if write_db is True:
        #    mysql.my_sql(analysis_sql)
        update_binlog_pos(pos_id=str(info["Log position"]), binlog_file=init_binlog_file_name)
    if write_db is True and count_num >= batch_number:
        analysis_sql = analysis_sql[:analysis_sql.rindex(',')]
        loging.debug("Query : %s " % analysis_sql)
        mysql.my_sql(analysis_sql)
        loging.info("批量解析insert id : %s:%d-(%s-%s) 提交处理" % (server_uuid, batch_number_count, log_position,
                                                            str(info["Log position"])))
        batch_number_count += 1
        analysis_sql = ''
        count_num = 0
    return count_num
